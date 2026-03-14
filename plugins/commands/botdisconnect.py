from plugins.common import *
import requests

def botdisconnect(server, target='all'):
    try:
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

        if target == 'all':
            targets = list(connected_bots.keys())
        else:
            if target not in connected_bots:
                logging.error(f'Bot {target} is not connected')
                return
            targets = [target]

        logging.info(f'Disconnecting {len(targets)} bot(s)...')

        success = 0
        failed = 0

        for u in targets:
            r = requests.post('http://localhost:6767/disconnect', json={
                "host": host,
                "port": int(port),
                "username": u
            })
            if r.status_code == 200:
                logging.success(f'{u} disconnected')
                success += 1
            else:
                logging.error(f'{u} failed: {r.status_code}')
                failed += 1

        print()
        logging.success(f'Done | Disconnected: {success} | Failed: {failed}')
        print()

    except Exception as e:
        logging.error(e)