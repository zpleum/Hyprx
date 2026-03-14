from plugins.common import *
import base64

def b64(mode, text):
    try:
        mode = mode.lower()

        if mode in ['encode', 'enc', 'e']:
            encoded = base64.b64encode(text.encode()).decode()
            print()
            logging.success(f'Input:   {text}')
            logging.success(f'Encoded: {encoded}')
            print()

        elif mode in ['decode', 'dec', 'd']:
            try:
                decoded = base64.b64decode(text.encode()).decode()
                print()
                logging.success(f'Input:   {text}')
                logging.success(f'Decoded: {decoded}')
                print()
            except Exception:
                logging.error('Invalid base64 string')

        else:
            logging.error(f'Unknown mode: {mode} — use encode/decode')

    except Exception as e:
        logging.error(e)