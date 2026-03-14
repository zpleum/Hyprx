from plugins.common import *
import requests
import socket

def playerlist(server):
    try:
        if ':' in server:
            host, port = server.split(':')
            port = int(port)
        else:
            host, port = server, 25565

        try:
            ip = socket.gethostbyname(host)
        except:
            ip = 'N/A'

        logging.info(f'Fetching player list for {host}:{port}')

        r = requests.get(f'https://api.mcsrvstat.us/3/{host}:{port}', timeout=10)
        data = r.json()

        print()

        if not data.get('online'):
            logging.error(f'Server is offline or unreachable')
            return

        players = data.get('players', {})
        online  = players.get('online', 0)
        maximum = players.get('max', 0)
        player_list = players.get('list', [])

        logging.success(f'Host:     {host}:{port}')
        logging.success(f'IP:       {ip}')
        logging.success(f'Players:  {online}/{maximum}')
        print()

        if not player_list:
            logging.error('No player list available (server may have it hidden)')
            print()
            return

        logging.success(f'Online players ({len(player_list)}):')
        for p in player_list:
            if isinstance(p, dict):
                name = p.get('name', 'N/A')
                uuid = p.get('uuid', 'N/A')
                logging.success(f'  {name:<24} {uuid}')
            else:
                logging.success(f'  {p}')

        print()

    except Exception as e:
        logging.error(e)