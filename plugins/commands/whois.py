from plugins.common import *
import socket
import re

WHOIS_SERVERS = {
    'com': 'whois.verisign-grs.com',
    'net': 'whois.verisign-grs.com',
    'org': 'whois.pir.org',
    'io': 'whois.nic.io',
    'co': 'whois.nic.co',
    'th': 'whois.thnic.co.th',
    'uk': 'whois.nic.uk',
    'de': 'whois.denic.de',
    'ru': 'whois.tcinet.ru',
    'cn': 'whois.cnnic.cn',
}

def query_whois(server, domain):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((server, 43))
        s.send((domain + '\r\n').encode())
        result = b''
        while True:
            data = s.recv(4096)
            if not data:
                break
            result += data
        s.close()
        return result.decode(errors='ignore')
    except Exception as e:
        return None

def parse_whois(raw):
    fields = {
        'Registrar':        r'(?i)registrar:\s*(.+)',
        'Registered':       r'(?i)(?:creation date|created|registered):\s*(.+)',
        'Expiry':           r'(?i)(?:expir(?:y|ation) date|expires):\s*(.+)',
        'Updated':          r'(?i)(?:updated date|last modified|changed):\s*(.+)',
        'Name Servers':     r'(?i)name server:\s*(.+)',
        'Status':           r'(?i)(?:domain status|status):\s*(.+)',
        'Registrant':       r'(?i)registrant(?:\s+name)?:\s*(.+)',
        'Registrant Email': r'(?i)registrant(?:\s+email)?:\s*(.+@.+)',
        'Registrant Org':   r'(?i)registrant(?:\s+organization)?:\s*(.+)',
    }

    parsed = {}
    for label, pattern in fields.items():
        matches = re.findall(pattern, raw)
        if matches:
            unique = list(dict.fromkeys([m.strip() for m in matches]))
            parsed[label] = unique if len(unique) > 1 else unique[0]
    return parsed

def whois(domain):
    try:
        if ':' in domain:
            domain = domain.split(':')[0]

        domain = domain.strip().lower()
        domain = re.sub(r'^https?://', '', domain)
        domain = domain.split('/')[0]

        tld = domain.split('.')[-1]
        whois_server = WHOIS_SERVERS.get(tld, f'whois.nic.{tld}')

        logging.info(f'Querying {whois_server} for {domain}')

        raw = query_whois(whois_server, domain)
        if not raw:
            raw = query_whois('whois.iana.org', domain)
        if not raw:
            logging.error('No response from whois server')
            return

        parsed = parse_whois(raw)

        if not parsed:
            logging.error('No data found — domain may not exist or whois is restricted')
            return

        print()
        for label, value in parsed.items():
            if isinstance(value, list):
                logging.success(f'{label}:')
                for v in value:
                    print(f'         {v}')
            else:
                logging.success(f'{label}: {value}')
        print()

    except Exception as e:
        logging.error(e)