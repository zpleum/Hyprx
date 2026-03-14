from plugins.common import *
import requests
import time

def connect(username, server, version='1.21.4', proxy=None):
    try:
        connected = False
        if not checkserver(server):
            logging.error('Please input a real domain or server')
            return
        if ':' in server:
            server, port = str(server).split(':')
        else:
            port = 25565

        payload = {"host": server, "port": port, "username": username, "version": version}
        if proxy is not None:
            payload["proxy"] = proxy

        logging.info(f'Connecting {username} -> {server}:{port} [{version}]')
        response = requests.post('http://localhost:6767/connect', json=payload)

        if response.status_code != 200 and response.status_code != 400:
            return logging.error(f'Failed to connect [{response.status_code}]')

        for i in range(10):
            try:
                r = requests.get('http://localhost:6767/status').json()[server + ':' + str(port)][username]['connected']
                if r:
                    connected = True
                    break
            except:
                pass
            logging.info('Waiting for connection...')
            time.sleep(2)

        if not connected:
            logging.error(f'Failed to connect {username} (timeout)')
            return

        logging.success(f'Connected {username}')
        logging.info(f'Type "exit" to disconnect')

        while True:
            msg = input('> ').strip()
            if msg.lower() == "exit":
                try:
                    if requests.get('http://localhost:6767/status').json()[server + ':' + str(port)][username]['connected']:
                        requests.post('http://localhost:6767/disconnect', json={"host": server, "port": port, "username": username})
                        logging.info('Bot disconnected')
                    else:
                        logging.info('Bot already disconnected')
                except:
                    pass
                return

            r = requests.post('http://localhost:6767/send', json={"host": server, "port": port, "username": username, "message": msg})
            if r.status_code != 200:
                logging.error(f'Failed to send — bot may be disconnected [{r.status_code}]')
                return

    except KeyboardInterrupt:
        try:
            requests.post('http://localhost:6767/disconnect', json={"host": server, "port": port, "username": username})
        except:
            pass
    except Exception as e:
        logging.error(e)