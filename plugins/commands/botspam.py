from plugins.common import *
import requests
import time
import threading

def botspam(server, message, delay=1, target='all'):
    try:
        if ':' in server:
            host, port = server.split(':')
        else:
            host, port = server, 25565

        delay = float(delay)

        status = requests.get('http://localhost:6767/status').json()
        key = f"{host}:{port}"

        if key not in status:
            logging.error('No bots connected to this server')
            return

        bots = status[key]
        connected_bots = {u: v for u, v in bots.items() if v.get('connected') == True}

        if not connected_bots:
            logging.error('No active bots connected to this server')
            return

        if target == 'all':
            targets = list(connected_bots.keys())
        else:
            if target not in connected_bots:
                logging.error(f'Bot {target} is not connected')
                return
            targets = [target]

        logging.info(f'Spamming {len(targets)} bot(s) | delay {delay}s | Ctrl+C to stop')

        stop_event = threading.Event()
        count = [0]

        def spam():
            while not stop_event.is_set():
                for u in targets:
                    if stop_event.is_set():
                        break
                    r = requests.post('http://localhost:6767/send', json={
                        "host": host,
                        "port": int(port),
                        "username": u,
                        "message": message
                    })
                    if r.status_code == 200:
                        count[0] += 1
                        logging.success(f'[{count[0]}] {u} > {message}')
                    else:
                        logging.error(f'{u} failed: {r.status_code}')
                    time.sleep(delay)

        t = threading.Thread(target=spam, daemon=True)
        t.start()

        while not stop_event.is_set():
            time.sleep(0.1)

    except KeyboardInterrupt:
        stop_event.set()
        logging.success(f'Stopped | Total sent: {count[0]}')
    except Exception as e:
        logging.error(e)