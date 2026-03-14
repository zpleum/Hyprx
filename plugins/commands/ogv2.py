from plugins.common import *
import requests
import time
import random
import threading
import os

FIRST = ["Alex","Sam","Jordan","Taylor","Morgan","Casey","Riley","Jamie","Drew","Quinn","Avery","Blake","Cameron","Dakota","Emery","Finley","Hayden","Hunter","Kendall","Logan"]
LAST = ["xD","YT","HD","GG","Pro","PvP","MC","Gaming","Plays","123","2025","007","404","999"]

PROXIES = []

def load_proxies():
    global PROXIES
    path = os.path.join(os.path.dirname(__file__), '..', 'default_proxies.txt')
    if not os.path.exists(path):
        logging.error('default_proxies.txt not found')
        return False
    with open(path, 'r') as f:
        PROXIES = [line.strip() for line in f if line.strip()]
    if not PROXIES:
        logging.error('default_proxies.txt is empty')
        return False
    logging.info(f'Loaded {len(PROXIES)} proxies')
    return True

def random_name():
    return f"{random.choice(FIRST)}{random.choice(LAST)}{random.randint(0,99)}"

def handle_bot(username, server, port, cmdfile, keep, current_proxy, version):
    try:
        payload = {"host": server, "port": port, "username": username, "version": version}
        if current_proxy is not None:
            payload["proxy"] = current_proxy

        logging.info(f'Connecting {username}' + (f' via {current_proxy}' if current_proxy else ''))
        response = requests.post('http://localhost:6767/connect', json=payload)

        if response.status_code != 200 and response.status_code != 400:
            logging.error(f'Failed to connect {username} [{response.status_code}]')
            return

        def wait_connected(timeout=60):
            for _ in range(timeout // 2):
                try:
                    status = requests.get('http://localhost:6767/status').json()
                    key = server + ':' + str(port)
                    if key in status and username in status[key]:
                        if status[key][username]['connected']:
                            return True
                except:
                    pass
                time.sleep(2)
            return False

        def send_commands():
            with open(cmdfile, 'r') as f:
                commands = [line.strip() for line in f if line.strip()]
            for command in commands:
                r = requests.post('http://localhost:6767/send', json={
                    "host": server, "port": port, "username": username, "message": command
                })
                if r.status_code != 200:
                    logging.error(f'Failed to send [{username}] {r.status_code}')
                    return False
                logging.success(f'[{username}] Sent: {command}')
                time.sleep(0.5)
            return True

        if not wait_connected(60):
            logging.error(f'Failed to connect {username} (timeout)')
            return

        logging.success(f'Connected {username}')
        time.sleep(3)

        max_attempts = 4
        for attempt in range(max_attempts):
            ok = send_commands()
            if ok:
                logging.success(f'All commands sent for {username}')
                break
            else:
                if attempt < max_attempts - 1:
                    logging.info(f'[{username}] Waiting for rejoin... ({attempt+1}/{max_attempts-1})')
                    time.sleep(5)
                    if wait_connected(60):
                        logging.success(f'[{username}] Rejoined — retrying commands')
                        time.sleep(3)
                    else:
                        logging.error(f'[{username}] Rejoin timeout')
                        break
                else:
                    logging.error(f'[{username}] Max cmd attempts reached')

        if keep == 'false':
            requests.post('http://localhost:6767/disconnect', json={
                "host": server, "port": port, "username": username
            })
            logging.success(f'{username} disconnected')

    except Exception as e:
        logging.error(f'[{username}] {e}')

def ogv2(userfile, server, cmdfile, keep, count=1, proxy=None, version='1.21.8'):
    try:
        if keep not in ['true', 'false']:
            logging.error('Please enter a valid value: true/false')
            return

        if ':' in server:
            server, port = str(server).split(':')
        else:
            port = 25565

        if not checkserver(server):
            logging.error('Please input a real domain or server')
            return

        if proxy in ['none', 'null', '-', '']:
            proxy = None

        if proxy and proxy.endswith('.txt'):
            path = proxy
            if not os.path.exists(path):
                logging.error(f'Proxy file not found: {path}')
                return
            with open(path, 'r') as f:
                PROXIES[:] = [line.strip() for line in f if line.strip()]
            if not PROXIES:
                logging.error(f'Proxy file is empty: {path}')
                return
            logging.info(f'Loaded {len(PROXIES)} proxies from {path}')
            proxy = 'auto'

        if proxy == 'auto' and not load_proxies():
            return

        if userfile.endswith('.txt'):
            with open(userfile, 'r') as f:
                usernames = [line.strip() for line in f if line.strip()]
        else:
            usernames = [random_name() for _ in range(int(count))]

        threads = []
        for idx, username in enumerate(usernames):
            if proxy == 'auto':
                current_proxy = PROXIES[idx % len(PROXIES)]
            elif proxy is not None:
                current_proxy = proxy
            else:
                current_proxy = None

            t = threading.Thread(target=handle_bot, args=(username, server, port, cmdfile, keep, current_proxy, version))
            t.daemon = True
            t.start()
            threads.append(t)
            time.sleep(0.5)

        for t in threads:
            t.join()

    except KeyboardInterrupt:
        logging.info('Interrupted')
        return
    except Exception as e:
        logging.error(e)