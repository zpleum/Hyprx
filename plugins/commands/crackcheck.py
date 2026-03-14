from plugins.common import *
import socket
import struct
import json

VERSIONS = {
    '1.21.11': 774,
    '1.21.10': 773,
    '1.21.9':  773,
    '1.21.8':  772,
    '1.21.7':  772,
    '1.21.6':  771,
    '1.21.5':  770,
    '1.21.4':  769,
    '1.21.3':  768,
    '1.21.1':  767,
    '1.21':    767,
    '1.20.6':  766,
    '1.20.5':  766,
    '1.20.4':  765,
    '1.20.2':  764,
    '1.20.1':  763,
    '1.20':    763,
    '1.19.4':  762,
    '1.19.3':  761,
    '1.19.2':  760,
    '1.19.1':  760,
    '1.19':    759,
    '1.18.2':  758,
    '1.18.1':  757,
    '1.18':    757,
    '1.17.1':  756,
    '1.17':    755,
    '1.16.5':  754,
    '1.16.4':  754,
    '1.16.3':  753,
    '1.16.2':  751,
    '1.16.1':  736,
    '1.16':    735,
    '1.15.2':  578,
    '1.15.1':  575,
    '1.15':    573,
    '1.14.4':  498,
    '1.14.3':  490,
    '1.14.2':  485,
    '1.14.1':  480,
    '1.14':    477,
    '1.13.2':  404,
    '1.13.1':  401,
    '1.13':    393,
    '1.12.2':  340,
    '1.12.1':  338,
    '1.12':    335,
    '1.11.2':  316,
    '1.11':    315,
    '1.10.2':  210,
    '1.10':    210,
    '1.9.4':   110,
    '1.9.2':   109,
    '1.9':     107,
    '1.8.9':   47,
    '1.8.8':   47,
    '1.8':     47,
}

def varint(value):
    buf = b''
    while True:
        part = value & 0x7F
        value >>= 7
        if value:
            part |= 0x80
        buf += bytes([part])
        if not value:
            return buf

def make_packet(data):
    return varint(len(data)) + data

def read_varint(s):
    result = 0
    shift = 0
    while True:
        b = s.recv(1)
        if not b:
            return 0
        val = b[0]
        result |= (val & 0x7F) << shift
        if not (val & 0x80):
            return result
        shift += 7

def read_packet(s):
    length = read_varint(s)
    if length <= 0:
        return None, None
    data = b''
    while len(data) < length:
        chunk = s.recv(length - len(data))
        if not chunk:
            break
        data += chunk
    if not data:
        return None, None
    return data[0], data[1:]

def read_string(data):
    i = 0
    result = 0
    shift = 0
    while i < len(data):
        b = data[i]
        i += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7
    return data[i:i+result].decode(errors='ignore')

def parse_reason(payload):
    try:
        text = read_string(payload)
        parsed = json.loads(text)
        parts = []
        if parsed.get('text'):
            parts.append(parsed['text'])
        for extra in parsed.get('extra', []):
            parts.append(extra.get('text', ''))
        result = ''.join(parts).strip()
        if result:
            return result
    except:
        pass
    try:
        raw = payload.decode(errors='ignore')
        idx = raw.find('{')
        if idx != -1:
            parsed = json.loads(raw[idx:])
            parts = []
            if parsed.get('text'):
                parts.append(parsed['text'])
            for extra in parsed.get('extra', []):
                parts.append(extra.get('text', ''))
            result = ''.join(parts).strip()
            if result:
                return result
    except:
        pass
    return None

TRY_VERSIONS = ['1.21.11', '1.21.8', '1.21.4', '1.21.1', '1.20.4', '1.20.1', '1.19.4', '1.18.2', '1.17.1', '1.16.5', '1.12.2', '1.8.8']

def try_connect(host, port, proto):
    try:
        s = socket.socket()
        s.settimeout(5)
        s.connect((host, port))

        host_bytes = host.encode()
        data = (
            b'\x00' +
            varint(proto) +
            varint(len(host_bytes)) + host_bytes +
            struct.pack('>H', port) +
            varint(2)
        )
        s.send(make_packet(data))
        name = b'HyprxCrackCheck'
        s.send(make_packet(b'\x00' + varint(len(name)) + name))

        mode = None
        disconnect_reason = None

        for _ in range(5):
            packet_id, payload = read_packet(s)
            if packet_id is None:
                break
            if packet_id == 0x01:
                mode = 'premium'
                break
            elif packet_id == 0x02:
                mode = 'cracked'
                break
            elif packet_id == 0x00:
                disconnect_reason = parse_reason(payload)
                mode = 'disconnected'
                break
            elif packet_id == 0x03:
                continue

        s.close()
        return mode, disconnect_reason
    except:
        return None, None

def crackcheck(server, version):
    try:
        if ':' in server:
            host, port = server.split(':')
            port = int(port)
        else:
            host, port = server, 25565

        proto = VERSIONS.get(version)
        if proto is None:
            logging.error(f'Unknown version: {version}')
            logging.info(f'Available: {", ".join(VERSIONS.keys())}')
            return

        logging.info(f'Checking {host}:{port} [{version}]...')

        mode, disconnect_reason = try_connect(host, port, proto)

        if mode == 'disconnected' and not disconnect_reason:
            logging.info('No reason received — trying other versions...')
            for v in TRY_VERSIONS:
                if v == version:
                    continue
                p = VERSIONS.get(v)
                m, r = try_connect(host, port, p)
                if m in ['premium', 'cracked']:
                    mode = m
                    version = v
                    proto = p
                    break
                if m == 'disconnected' and r:
                    mode = m
                    disconnect_reason = r
                    version = v
                    proto = p
                    break
                logging.info(f'Tried {v} — {m or "no response"}')

        print()
        logging.success(f'Host:        {host}:{port}')
        logging.success(f'Version:     {version} (protocol {proto})')

        if mode == 'premium':
            logging.success(f'Mode:        Premium (Online Mode)')
            logging.success(f'Cracked:     No')
            logging.success(f'UUID Spoof:  May work via BungeeCord exploit')

        elif mode == 'cracked':
            logging.success(f'Mode:        Cracked (Offline Mode)')
            logging.success(f'Cracked:     Yes ✓')
            logging.success(f'UUID Spoof:  Likely works')

        elif mode == 'disconnected':
            reason_lower = disconnect_reason.lower() if disconnect_reason else ''
            logging.success(f'Mode:        Disconnected')
            if disconnect_reason:
                logging.success(f'Reason:      {disconnect_reason}')
            if any(x in reason_lower for x in ['outdated client', 'outdated server', 'please use', 'version']):
                logging.success(f'Cracked:     Likely Premium — wrong version')
                logging.success(f'Tip:         Try a different version')
            elif any(x in reason_lower for x in ['whitelist', 'not whitelisted']):
                logging.success(f'Cracked:     Unknown — server is whitelisted')
            elif any(x in reason_lower for x in ['banned', 'blacklisted']):
                logging.success(f'Cracked:     Unknown — IP banned')
            elif any(x in reason_lower for x in ['proxy', 'vpn', 'bot', 'flood']):
                logging.success(f'Cracked:     Unknown — anti-bot triggered')
            else:
                logging.success(f'Cracked:     Unknown')
        else:
            logging.error(f'No response — may be protected or offline')

        print()

    except ConnectionRefusedError:
        logging.error(f'Connection refused — server offline or port closed')
    except socket.timeout:
        logging.error(f'Connection timed out — may be behind TCPShield/Cloudflare')
    except socket.gaierror:
        logging.error(f'Cannot resolve hostname — check domain spelling')
    except Exception as e:
        logging.error(e)