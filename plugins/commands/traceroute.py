from plugins.common import *
import subprocess
import re
import platform
import socket

def traceroute(host, max_hops=30):
    try:
        if ':' in host:
            host = host.split(':')[0]

        host = host.strip()
        max_hops = int(max_hops)

        # resolve IP
        try:
            ip = socket.gethostbyname(host)
        except:
            ip = None

        if ip and ip != host:
            logging.info(f'Traceroute to {host} [{ip}] max {max_hops} hops')
        else:
            logging.info(f'Traceroute to {host} max {max_hops} hops')

        system = platform.system().lower()
        if system == 'windows':
            cmd = ['tracert', '-d', '-h', str(max_hops), host]
        else:
            cmd = ['traceroute', '-n', '-m', str(max_hops), host]

        print()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        hop_num = 0
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue

            # skip header lines
            if any(x in line.lower() for x in ['tracing', 'traceroute', 'over a maximum', 'route to']):
                continue
            if line.lower().startswith('trace'):
                continue

            # parse windows format: "  1    <1 ms    <1 ms    <1 ms  192.168.1.1"
            if system == 'windows':
                match = re.match(r'^\s*(\d+)\s+(.+)$', line)
                if match:
                    hop = match.group(1)
                    rest = match.group(2)

                    # extract times
                    times = re.findall(r'(\d+)\s*ms|<(\d+)\s*ms', rest)
                    ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', rest)

                    if '*' in rest and not ip_match:
                        logging.info(f'  {hop:<3}  * * *  Request timed out')
                        continue

                    hop_ip = ip_match.group(1) if ip_match else 'N/A'

                    time_vals = []
                    for t in times:
                        val = t[0] or t[1]
                        if val:
                            time_vals.append(float(val))

                    if time_vals:
                        avg = sum(time_vals) / len(time_vals)
                        mn  = min(time_vals)
                        mx  = max(time_vals)
                        logging.success(f'  {hop:<3}  {hop_ip:<20}  avg={avg:.0f}ms  min={mn:.0f}ms  max={mx:.0f}ms')
                    else:
                        logging.success(f'  {hop:<3}  {hop_ip:<20}  * * *')
            else:
                # linux format: "  1  192.168.1.1  1.234 ms  1.123 ms  1.456 ms"
                match = re.match(r'^\s*(\d+)\s+(.+)$', line)
                if match:
                    hop = match.group(1)
                    rest = match.group(2)

                    if rest.strip() == '* * *':
                        logging.info(f'  {hop:<3}  * * *  Request timed out')
                        continue

                    ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', rest)
                    times = re.findall(r'(\d+\.?\d*)\s*ms', rest)

                    hop_ip = ip_match.group(1) if ip_match else 'N/A'
                    time_vals = [float(t) for t in times]

                    if time_vals:
                        avg = sum(time_vals) / len(time_vals)
                        mn  = min(time_vals)
                        mx  = max(time_vals)
                        logging.success(f'  {hop:<3}  {hop_ip:<20}  avg={avg:.1f}ms  min={mn:.1f}ms  max={mx:.1f}ms')
                    else:
                        logging.success(f'  {hop:<3}  {hop_ip:<20}  * * *')

        process.wait()
        print()
        logging.success(f'Traceroute complete')
        print()

    except KeyboardInterrupt:
        logging.info('Stopped')
    except Exception as e:
        logging.error(e)