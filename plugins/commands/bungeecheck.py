from plugins.common import *
import socket
import struct

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

def handshake_packet(host, port, next_state=2):
    data = (
        b'\x00' +
        varint(767) +
        varint(len(host)) + host.encode() +
        struct.pack('>H', int(port)) +
        varint(next_state)
    )
    return make_packet(data)

def login_packet(username):
    name = username.encode()
    data = b'\x00' + varint(len(name)) + name
    return make_packet(data)

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

def bungeecheck(server):
    try:
        if ':' in server:
            host, port = server.split(':')
            port = int(port)
        else:
            host, port = server, 25565

        logging.info(f'Checking {host}:{port} for IP forwarding...')

        results = {}

        # test 1 — connect with fake forwarded IP header (BungeeCord style)
        try:
            s = socket.socket()
            s.settimeout(5)
            s.connect((host, port))

            # send handshake with fake IP in host field (bungeecord passes host\00ip\00uuid)
            fake_host = f"{host}\x00{'.'.join(str(x) for x in [1,2,3,4])}\x00{'00000000-0000-0000-0000-000000000001'}"
            data = (
                b'\x00' +
                varint(767) +
                varint(len(fake_host)) + fake_host.encode() +
                struct.pack('>H', port) +
                varint(2)
            )
            s.send(make_packet(data))
            s.send(login_packet('TestBot'))

            resp = s.recv(4096)
            s.close()

            if resp:
                results['ip_forward_test'] = True
                if b'disconnect' in resp.lower() or b'kicked' in resp.lower():
                    results['ip_forward_response'] = 'kicked'
                else:
                    results['ip_forward_response'] = 'accepted'
            else:
                results['ip_forward_test'] = False

        except Exception as e:
            results['ip_forward_test'] = False
            results['ip_forward_error'] = str(e)

        # test 2 — connect normally and check response
        try:
            s = socket.socket()
            s.settimeout(5)
            s.connect((host, port))
            s.send(handshake_packet(host, port))
            s.send(login_packet('TestBot2'))
            resp2 = s.recv(4096)
            s.close()
            results['normal_response'] = resp2.hex() if resp2 else None
        except Exception as e:
            results['normal_response'] = None

        # test 3 — check if online mode (sends encryption request = premium)
        try:
            s = socket.socket()
            s.settimeout(5)
            s.connect((host, port))
            s.send(handshake_packet(host, port))
            s.send(login_packet('TestBot3'))

            length = read_varint(s)
            if length > 0:
                data = s.recv(length)
                packet_id = data[0] if data else None
                if packet_id == 0x01:
                    results['online_mode'] = True
                elif packet_id == 0x02:
                    results['online_mode'] = False
                else:
                    results['online_mode'] = 'unknown'
            s.close()
        except:
            results['online_mode'] = 'unknown'

        # print results
        print()
        logging.success(f'Host:            {host}:{port}')

        # ip forwarding
        if results.get('ip_forward_test'):
            logging.success(f'IP Forwarding:   Possibly OPEN ⚠')
            logging.success(f'Response:        {results.get("ip_forward_response", "N/A")}')
        else:
            logging.success(f'IP Forwarding:   Protected ✓')

        # online mode
        om = results.get('online_mode')
        if om == True:
            logging.success(f'Online Mode:     Yes (Premium)')
        elif om == False:
            logging.success(f'Online Mode:     No (Cracked)')
        else:
            logging.success(f'Online Mode:     Unknown')

        # bungeecord guess
        if results.get('ip_forward_test') and results.get('online_mode') == False:
            logging.success(f'BungeeCord:      Likely VULNERABLE — try UUID spoofing')
        elif results.get('ip_forward_test'):
            logging.success(f'BungeeCord:      Possibly open — test manually')
        else:
            logging.success(f'BungeeCord:      Protected or not BungeeCord')

        print()

    except Exception as e:
        logging.error(e)