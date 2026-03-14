from plugins.common import *
import requests
import time

def botchat(server, message_and_target):
    parts = message_and_target.split()
    last = parts[-1]
    
    if ':' in server:
        host, port = server.split(':')
    else:
        host, port = server, 25565

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

    if last == 'all' or last in connected_bots:
        username = last
        message = ' '.join(parts[:-1])
    else:
        username = 'all'
        message = ' '.join(parts)

    if username == 'all':
        targets = list(connected_bots.keys())
    else:
        if username not in connected_bots:
            logging.error(f'Bot {username} is not connected')
            return
        targets = [username]

    logging.info(f'Sending to {len(targets)} bot(s)')

    for u in targets:
        r = requests.post('http://localhost:6767/send', json={
            "host": host,
            "port": int(port),
            "username": u,
            "message": message
        })
        if r.status_code == 200:
            logging.success(f'{u} > {message}')
        else:
            logging.error(f'{u} failed: {r.status_code}')
        time.sleep(0.1)