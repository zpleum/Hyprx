from plugins.common import *
import subprocess
import re
import platform
import socket

def ping(host, count=4):
    try:
        if ':' in host:
            host = host.split(':')[0]

        host = host.strip()
        count = int(count)

        try:
            ip = socket.gethostbyname(host)
        except:
            ip = None

        if ip and ip != host:
            logging.info(f'Pinging {host} [{ip}] {count} times')
        else:
            logging.info(f'Pinging {host} {count} times')

        system = platform.system().lower()

        times = []
        for i in range(count):
            if system == 'windows':
                cmd = ['ping', '-n', '1', host]
            else:
                cmd = ['ping', '-c', '1', host]

            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout + result.stderr

            match = re.search(r'time[=<](\d+\.?\d*)ms', output, re.IGNORECASE)
            if match:
                t = float(match.group(1))
                times.append(t)
                logging.success(f'Reply from {ip or host}: time={t:.2f}ms')
            else:
                logging.error(f'Request timeout for {ip or host}')

        print()
        if times:
            sent = count
            recv = len(times)
            lost = sent - recv
            logging.success(f'Sent:     {sent}')
            logging.success(f'Received: {recv}')
            logging.success(f'Lost:     {lost} ({round(lost/sent*100)}%)')
            logging.success(f'Min:      {min(times):.2f} ms')
            logging.success(f'Max:      {max(times):.2f} ms')
            logging.success(f'Avg:      {sum(times)/len(times):.2f} ms')
        else:
            logging.error(f'Host unreachable: {host}')
        print()

    except Exception as e:
        logging.error(e)