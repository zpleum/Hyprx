from plugins.common import *
import requests
import time
import random
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

def ogmur(userfile, server, cmdfile, keep, count=1, proxy=None, delay=5):
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

        if proxy == 'auto' and not load_proxies():
            return

        if userfile.endswith('.txt'):
            with open(userfile, 'r') as f:
                usernames = [line.strip() for line in f if line.strip()]
        else:
            usernames = [random_name() for _ in range(int(count))]

        for i, username in enumerate(usernames):
            connected = False

            if proxy == 'auto':
                current_proxy = PROXIES[i % len(PROXIES)]
            elif proxy is not None:
                current_proxy = proxy
            else:
                current_proxy = None

            payload = {"host": server, "port": port, "username": username}
            if current_proxy is not None:
                payload["proxy"] = current_proxy

            logging.info(f'Connecting {username}' + (f' via {current_proxy}' if current_proxy else ''))
            response = requests.post('http://localhost:6767/connect', json=payload)

            if response.status_code != 200 and response.status_code != 400:
                logging.error(f'Failed to connect [{response.status_code}]')
                return

            for _ in range(15):
                try:
                    status = requests.get('http://localhost:6767/status').json()
                    key = server + ':' + str(port)
                    if key in status and username in status[key]:
                        if status[key][username]['connected']:
                            connected = True
                            break
                except:
                    pass
                logging.info('Waiting for connection...')
                time.sleep(2)

            if not connected:
                logging.error(f'Failed to connect {username} (timeout)')
                continue

            logging.success(f'Connected {username}')

            time.sleep(3)
            with open(cmdfile, 'r') as commands_file:
                commands = [line.strip() for line in commands_file if line.strip()]

            for command in commands:
                r = requests.post('http://localhost:6767/send', json={
                    "host": server,
                    "port": port,
                    "username": username,
                    "message": command
                })
                if r.status_code != 200:
                    logging.error(f'Failed to send message. (BOT LIKELY DISCONNECTED) {r.status_code}')
                    break

                logging.success(f'Sent: {command}')
                time.sleep(0.5)

            logging.success(f'All commands have been sent for {username}')

            if keep == 'false':
                requests.post('http://localhost:6767/disconnect', json={
                    "host": server,
                    "port": port,
                    "username": username
                })
                logging.success(f'{username} has been disconnected')

            if i < len(usernames) - 1:
                logging.info(f'Waiting {delay}s before next bot...')
                time.sleep(delay)

    except KeyboardInterrupt:
        logging.info('Interrupted')
        return
    except Exception as e:
        logging.error(e)