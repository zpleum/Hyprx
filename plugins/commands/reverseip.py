from plugins.common import *
import requests

def reverseip(ip):
    try:
        if ':' in ip:
            ip = ip.split(':')[0]
        ip = ip.strip()

        logging.info(f'Looking up domains for {ip}')

        r = requests.get(f'https://api.hackertarget.com/reverseiplookup/?q={ip}', timeout=10)

        if 'error' in r.text.lower() or 'no records' in r.text.lower():
            logging.error(f'No domains found for {ip}')
            return

        domains = [line.strip() for line in r.text.splitlines() if line.strip()]

        if not domains:
            logging.error('No domains found')
            return

        print()
        logging.success(f'IP:      {ip}')
        logging.success(f'Domains: {len(domains)}')
        print()
        for domain in domains:
            logging.success(f'  {domain}')
        print()

    except Exception as e:
        logging.error(e)