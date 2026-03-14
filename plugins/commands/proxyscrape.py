from plugins.common import *
import requests
import os

SOURCES = {
    'socks5': [
        'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt',
        'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt',
        'https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
    ],
    'socks4': [
        'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt',
        'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt',
        'https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt',
    ],
    'http': [
        'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
        'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt',
        'https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    ],
}

def proxyscrape(ptype, output=None):
    try:
        ptype = ptype.lower()

        if ptype not in SOURCES:
            logging.error(f'Unknown type: {ptype} — use socks5, socks4, http')
            return

        if output is None:
            output = f'{ptype}.txt'

        sources = SOURCES[ptype]
        proxies = set()

        logging.info(f'Scraping {ptype} proxies from {len(sources)} sources...')

        for i, url in enumerate(sources):
            try:
                r = requests.get(url, timeout=10)
                lines = r.text.splitlines()
                count = 0
                for line in lines:
                    line = line.strip()
                    if not line or ' ' in line:
                        continue
                    # strip protocol prefix if present
                    if '://' in line:
                        line = line.split('://', 1)[1]
                    # validate ip:port format
                    if ':' in line:
                        parts = line.split(':')
                        if len(parts) == 2:
                            proxies.add(f'{ptype}://{line}')
                            count += 1
                logging.success(f'[{i+1}/{len(sources)}] {url.split("/")[4]}/{url.split("/")[5]} — {count} proxies')
            except Exception as e:
                logging.error(f'[{i+1}/{len(sources)}] Failed: {url.split("/")[2]} — {e}')

        if not proxies:
            logging.error('No proxies found')
            return

        with open(output, 'w') as f:
            for proxy in sorted(proxies):
                f.write(proxy + '\n')

        print()
        logging.success(f'Total: {len(proxies)} unique {ptype} proxies')
        logging.success(f'Saved to: {output}')
        print()

    except KeyboardInterrupt:
        logging.info('Stopped')
    except Exception as e:
        logging.error(e)