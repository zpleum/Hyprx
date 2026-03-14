from plugins.common import *
import requests
import threading
import time
import os

def check_proxy(proxy, results, lock):
    try:
        proxies = {
            'http': proxy,
            'https': proxy
        }
        r = requests.get('http://ip-api.com/json', proxies=proxies, timeout=8)
        data = r.json()
        if data.get('status') == 'success':
            ip = data.get('query', 'N/A')
            country = data.get('country', 'N/A')
            with lock:
                results['alive'].append((proxy, ip, country))
        else:
            with lock:
                results['dead'].append(proxy)
    except:
        with lock:
            results['dead'].append(proxy)

def proxycheck(file, threads=50):
    try:
        threads = int(threads)

        if not os.path.exists(file):
            logging.error(f'File not found: {file}')
            return

        with open(file, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]

        if not proxies:
            logging.error('No proxies found in file')
            return

        logging.info(f'Checking {len(proxies)} proxies | {threads} threads')

        results = {'alive': [], 'dead': []}
        lock = threading.Lock()
        pool = []
        done = [0]

        def worker(proxy):
            check_proxy(proxy, results, lock)
            with lock:
                done[0] += 1

        # batch threading
        for i in range(0, len(proxies), threads):
            batch = proxies[i:i+threads]
            pool = []
            for proxy in batch:
                t = threading.Thread(target=worker, args=(proxy,), daemon=True)
                t.start()
                pool.append(t)
            for t in pool:
                t.join()
            alive = len(results['alive'])
            dead = len(results['dead'])
            total = alive + dead
            logging.info(f'Progress: {total}/{len(proxies)} | Alive: {alive} | Dead: {dead}')

        print()
        logging.success(f'Done | Total: {len(proxies)} | Alive: {len(results["alive"])} | Dead: {len(results["dead"])}')
        print()

        if results['alive']:
            logging.success(f'Alive proxies:')
            for proxy, ip, country in results['alive']:
                logging.success(f'  {proxy:<45} {ip:<20} {country}')
            print()

        # save alive proxies
        if results['alive']:
            out = file.replace('.txt', '_alive.txt')
            with open(out, 'w') as f:
                for proxy, _, _ in results['alive']:
                    f.write(proxy + '\n')
            logging.success(f'Saved alive proxies to {out}')
            print()

    except KeyboardInterrupt:
        logging.info('Stopped')
    except Exception as e:
        logging.error(e)