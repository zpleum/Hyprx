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
        connected = False

        payload = {"host": server, "port": port, "username": username, "version": version}
        if current_proxy is not None:
            payload["proxy"] = current_proxy

        logging.info(f'Connecting {username}' + (f' via {current_proxy}' if current_proxy else ''))
        response = requests.post('http://localhost:6767/connect', json=payload)

        if response.status_code != 200 and response.status_code != 400:
            logging.error(f'Failed to connect {username} [{response.status_code}]')
            return

        for i in range(10):
            try:
                status = requests.get('http://localhost:6767/status').json()
                key = server + ':' + str(port)
                if key in status and username in status[key]:
                    if status[key][username]['connected']:
                        connected = True
                        break
            except:
                pass
            time.sleep(2)

        if not connected:
            logging.error(f'Failed to connect {username} (timeout)')
            return

        logging.success(f'Connected {username}')

        time.sleep(3)
        with open(cmdfile, 'r') as f:
            commands = [line.strip() for line in f if line.strip()]

        for command in commands:
            r = requests.post('http://localhost:6767/send', json={
                "host": server, "port": port, "username": username, "message": command
            })
            if r.status_code != 200:
                logging.error(f'Failed to send [{username}] {r.status_code}')
                break
            logging.success(f'[{username}] Sent: {command}')
            time.sleep(0.1)

        logging.success(f'All commands sent for {username}')

        if keep == 'false':
            requests.post('http://localhost:6767/disconnect', json={
                "host": server, "port": port, "username": username
            })
            logging.success(f'{username} disconnected')

    except Exception as e:
        logging.error(f'[{username}] {e}')

def ogv2(userfile, server, cmdfile, keep, count=1, proxy=None, version='1.21.4'):
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
            time.sleep(0)

        for t in threads:
            t.join()

    except KeyboardInterrupt:
        logging.info('Interrupted')
        return
    except Exception as e:
        logging.error(e)