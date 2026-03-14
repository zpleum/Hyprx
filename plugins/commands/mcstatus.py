from plugins.common import *
import requests
import socket

def mcstatus(server):
    try:
        if ':' in server:
            host, port = server.split(':')
            port = int(port)
        else:
            host, port = server, 25565

        # resolve IP
        try:
            ip = socket.gethostbyname(host)
        except:
            ip = 'N/A'

        logging.info(f'Querying {host}:{port}')

        r = requests.get(
            f'https://api.mcsrvstat.us/3/{host}:{port}',
            timeout=10,
            headers={'User-Agent': 'Hyprx/1.0 Minecraft Tool'}
        )
        data = r.json()

        print()

        if not data.get('online'):
            r2 = requests.get(
                f'https://api.mcstatus.io/v2/status/java/{host}:{port}',
                timeout=10
            )
            data2 = r2.json()
            if data2.get('online'):
                data = {
                    'online': True,
                    'version': data2.get('version', {}).get('name_clean', 'N/A'),
                    'players': {
                        'online': data2.get('players', {}).get('online', 0),
                        'max': data2.get('players', {}).get('max', 0),
                        'list': [{'name': p['name_clean'], 'uuid': p['uuid']} for p in data2.get('players', {}).get('list', [])]
                    },
                    'motd': {'clean': [data2.get('motd', {}).get('clean', '')]},
                    'software': data2.get('software', None),
                }
            else:
                logging.error(f'Server is offline or unreachable')
                return

        # basic info
        logging.success(f'Host:       {host}')
        logging.success(f'IP:         {ip}')
        logging.success(f'Port:       {port}')
        logging.success(f'Status:     Online')
        logging.success(f'Version:    {data.get("version", "N/A")}')

        # players
        players = data.get('players', {})
        online  = players.get('online', 0)
        maximum = players.get('max', 0)
        logging.success(f'Players:    {online}/{maximum}')

        # player list
        player_list = players.get('list', [])
        if player_list:
            logging.success(f'Online:')
            for p in player_list:
                name = p.get('name', p) if isinstance(p, dict) else p
                print(f'            - {name}')

        # motd
        motd = data.get('motd', {})
        motd_clean = motd.get('clean', [])
        if motd_clean:
            logging.success(f'MOTD:')
            for line in motd_clean:
                if line.strip():
                    print(f'            {line.strip()}')

        # software + protocol
        software = data.get('software', None)
        protocol = data.get('protocol', {})
        if software:
            logging.success(f'Software:   {software}')
        if protocol:
            logging.success(f'Protocol:   {protocol.get("version", "N/A")} ({protocol.get("name", "N/A")})')

        # plugins
        plugins = data.get('plugins', [])
        if plugins:
            logging.success(f'Plugins:    {len(plugins)}')
            for p in plugins[:10]:
                name = p.get('name', p) if isinstance(p, dict) else p
                ver  = p.get('version', '') if isinstance(p, dict) else ''
                print(f'            - {name}{f" {ver}" if ver else ""}')
            if len(plugins) > 10:
                print(f'            ... and {len(plugins) - 10} more')

        # mods
        mods = data.get('mods', [])
        if mods:
            logging.success(f'Mods:       {len(mods)}')
            for m in mods[:5]:
                name = m.get('name', m) if isinstance(m, dict) else m
                print(f'            - {name}')
            if len(mods) > 5:
                print(f'            ... and {len(mods) - 5} more')

        # icon
        if data.get('icon'):
            logging.success(f'Icon:       Yes')

        # srv record
        srv = data.get('srv', False)
        if srv:
            logging.success(f'SRV:        Yes')

        print()

    except Exception as e:
        logging.error(e)