from plugins.common import *
import requests

def geoip(ip):
    try:
        if ':' in ip:
            ip = ip.split(':')[0]

        ip = ip.strip()

        logging.info(f'Looking up {ip}')

        r = requests.get(f'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query', timeout=10)
        data = r.json()

        if data.get('status') != 'success':
            logging.error(f'Lookup failed: {data.get("message", "unknown error")}')
            return

        fields = [
            ('IP',          data.get('query', 'N/A')),
            ('Country',     f"{data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})"),
            ('Region',      data.get('regionName', 'N/A')),
            ('City',        data.get('city', 'N/A')),
            ('ZIP',         data.get('zip', 'N/A')),
            ('Coordinates', f"{data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}"),
            ('Timezone',    data.get('timezone', 'N/A')),
            ('ISP',         data.get('isp', 'N/A')),
            ('Org',         data.get('org', 'N/A')),
            ('AS',          data.get('as', 'N/A')),
            ('AS Name',     data.get('asname', 'N/A')),
            ('Reverse DNS', data.get('reverse', 'N/A')),
            ('Mobile',      str(data.get('mobile', False))),
            ('Proxy/VPN',   str(data.get('proxy', False))),
            ('Hosting',     str(data.get('hosting', False))),
        ]

        print()
        for label, value in fields:
            if value in ('N/A', '', 'None', 'False', 'True'):
                color = gray if value in ('N/A', '', 'None') else (green if value == 'True' else gray)
            else:
                color = white
            logging.success(f'{label+":":<15} {value}')
        print()

    except Exception as e:
        logging.error(e)