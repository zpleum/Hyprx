from plugins.common import *
import hashlib
import os
import threading
import time

ALGORITHMS = {
    'md5':      hashlib.md5,
    'sha1':     hashlib.sha1,
    'sha224':   hashlib.sha224,
    'sha256':   hashlib.sha256,
    'sha384':   hashlib.sha384,
    'sha512':   hashlib.sha512,
    'sha3_224': hashlib.sha3_224,
    'sha3_256': hashlib.sha3_256,
    'sha3_384': hashlib.sha3_384,
    'sha3_512': hashlib.sha3_512,
    'blake2b':  hashlib.blake2b,
    'blake2s':  hashlib.blake2s,
}

def detect_algo(hash_str):
    length = len(hash_str)
    mapping = {
        32:  'md5',
        40:  'sha1',
        56:  'sha224',
        64:  'sha256',
        96:  'sha384',
        128: 'sha512',
    }
    return mapping.get(length, None)

def crack(hash_str, wordlist, algo='auto', threads=4):
    try:
        hash_str = hash_str.strip().lower()
        threads = int(threads)

        if not os.path.exists(wordlist):
            logging.error(f'Wordlist not found: {wordlist}')
            return

        if algo == 'auto':
            algo = detect_algo(hash_str)
            if not algo:
                logging.error('Cannot detect algorithm — specify manually')
                logging.info(f'Available: {", ".join(ALGORITHMS.keys())}')
                return
            logging.info(f'Detected algorithm: {algo}')

        algo = algo.lower()
        if algo not in ALGORITHMS:
            logging.error(f'Unknown algorithm: {algo}')
            logging.info(f'Available: {", ".join(ALGORITHMS.keys())}')
            return

        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            words = [line.strip() for line in f if line.strip()]

        if not words:
            logging.error('Wordlist is empty')
            return

        logging.info(f'Cracking {hash_str[:16]}... | algo={algo} | wordlist={len(words)} words | {threads} threads')

        found = [None]
        stop = threading.Event()
        count = [0]
        start_time = time.time()

        def worker(chunk):
            for word in chunk:
                if stop.is_set():
                    return
                try:
                    h = ALGORITHMS[algo](word.encode()).hexdigest()
                    count[0] += 1
                    if h == hash_str:
                        found[0] = word
                        stop.set()
                        return
                except:
                    pass

        def stats():
            while not stop.is_set():
                time.sleep(1)
                elapsed = time.time() - start_time
                rate = count[0] / elapsed if elapsed > 0 else 0
                logging.info(f'Tried: {count[0]}/{len(words)} | {rate:.0f} h/s')

        # split wordlist into chunks
        chunk_size = max(1, len(words) // threads)
        chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]

        pool = [threading.Thread(target=worker, args=(chunk,), daemon=True) for chunk in chunks]
        stats_thread = threading.Thread(target=stats, daemon=True)

        for t in pool:
            t.start()
        stats_thread.start()

        for t in pool:
            t.join()

        stop.set()
        elapsed = time.time() - start_time

        print()
        if found[0]:
            logging.success(f'CRACKED!')
            logging.success(f'Hash:     {hash_str}')
            logging.success(f'Password: {found[0]}')
            logging.success(f'Algo:     {algo}')
            logging.success(f'Tried:    {count[0]} words in {elapsed:.2f}s')
        else:
            logging.error(f'Not found in wordlist')
            logging.info(f'Tried: {count[0]} words in {elapsed:.2f}s')
        print()

    except KeyboardInterrupt:
        stop.set()
        logging.info(f'Stopped | Tried: {count[0]} words')
    except Exception as e:
        logging.error(e)