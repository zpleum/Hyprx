from plugins.common import *
import hashlib

ALGORITHMS = {
    'md5':        hashlib.md5,
    'sha1':       hashlib.sha1,
    'sha224':     hashlib.sha224,
    'sha256':     hashlib.sha256,
    'sha384':     hashlib.sha384,
    'sha512':     hashlib.sha512,
    'sha3_224':   hashlib.sha3_224,
    'sha3_256':   hashlib.sha3_256,
    'sha3_384':   hashlib.sha3_384,
    'sha3_512':   hashlib.sha3_512,
    'blake2b':    hashlib.blake2b,
    'blake2s':    hashlib.blake2s,
}

def hash(mode, text):
    try:
        mode = mode.lower()

        if mode == 'all':
            print()
            logging.success(f'Input: {text}')
            print()
            for name, fn in ALGORITHMS.items():
                try:
                    result = fn(text.encode()).hexdigest()
                    logging.success(f'{name:<12} {result}')
                except:
                    pass
            print()
            return

        if mode not in ALGORITHMS:
            logging.error(f'Unknown algorithm: {mode}')
            logging.info(f'Available: {", ".join(ALGORITHMS.keys())}, all')
            return

        result = ALGORITHMS[mode](text.encode()).hexdigest()
        print()
        logging.success(f'Algorithm: {mode}')
        logging.success(f'Input:     {text}')
        logging.success(f'Hash:      {result}')
        print()

    except Exception as e:
        logging.error(e)