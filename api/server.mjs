process.on('uncaughtException', (err) => {
  if (err.message?.includes('PartialReadError')) return;
  if (err.message?.includes('Chunk size')) return;
  console.error('[Hyprx]', err);
});

process.on('unhandledRejection', (error) => {
  console.error('[Hyprx]', error);
});

import express from 'express';
import { createBot } from 'mineflayer';
import { SocksClient } from 'socks';
const app = express();
const port = 6767;

const botz = {}, statuz = {};

app.use(express.json());

function parseProxy(proxyUrl) {
  try {
    const url = new URL(proxyUrl);
    if (!url.protocol.startsWith('socks')) throw new Error('Unsupported proxy type');
    return {
      type: parseInt(url.protocol.replace('socks', '').replace(':', ''), 10),
      host: url.hostname,
      port: parseInt(url.port, 10),
      userId: decodeURIComponent(url.username) || undefined,
      password: decodeURIComponent(url.password) || undefined
    };
  } catch {
    throw new Error('Invalid proxy URL format');
  }
}

app.post('/connect', async (req, res) => {
  console.log("CONNECT REQUEST:", req.body)

  const { host, port = 25565, username, proxy } = req.body;
  const server = `${host}:${port}`;
  if (botz[server]?.[username]) return res.status(400).json({ error: 'Bot already connected.' });

  try {
    let customConnect;
    if (proxy) {
      const broxy = parseProxy(proxy);
      customConnect = async (client) => {
        const { socket } = await SocksClient.createConnection({
          proxy: {
            host: broxy.host,
            port: broxy.port,
            type: broxy.type,
            userId: broxy.userId,
            password: broxy.password
          },
          command: 'connect',
          destination: { host: host.trim(), port: Number(port) }
        });
        console.log(`[Proxy] Connected through ${broxy.host}:${broxy.port}`);
        client.setSocket(socket);
        client.emit('connect');
      };
    }

    console.log(`Connecting bot ${username} -> ${host}:${port}`)

    const options = {
      username: username,
      host: host,
      port: Number(port),
      version: '1.21.11',
      auth: 'offline',
      hideErrors: true,
      checkTimeoutInterval: 120000,
      keepAlive: true
    }

    if (customConnect) {
      options.connect = customConnect
    }

    const bot = createBot(options)


    bot._client.on('add_resource_pack', (data) => {
      try {
        const url = data.url || 'unknown';
        const hash = data.hash || 'unknown';
        console.log(`[~] Bot ${username} accepting resource pack: ${url} (hash: ${hash})`)
      } catch {
        console.log(`[~] Bot ${username} accepting resource pack...`)
      }
      bot._client.write('resource_pack_receive', {
        uuid: data.uuid,
        result: 3
      })
      bot._client.write('resource_pack_receive', {
        uuid: data.uuid,
        result: 0
      })
    })

    bot.on('login', () => console.log(`[Bot] Logged in as ${username} on ${server}`))

    bot._client.on('state', (newState) => {
      console.log(`[Bot] State changed: ${newState}`)
    })

    bot._client.on('packet', (data, meta) => {
      if (meta.name === 'disconnect') {
        console.log(`[Bot] Disconnect packet:`, data)
      }
    })

    bot.on('spawn', () => {
      console.log(`[Bot] Spawned`)
      statuz[server][username].connected = true
    })

    bot.on('error', err => {
      if (err.message?.includes('PartialReadError')) return;
      if (err.message?.includes('Chunk size')) return;
      console.log(`[Bot ERROR]`, err)
    })

    bot.on('kicked', reason => {
      try {
        const deep = (obj) => {
          if (typeof obj === 'string') return obj;
          if (typeof obj === 'number') return String(obj);
          if (Array.isArray(obj)) return obj.map(deep).join('');
          if (obj?.value !== undefined) return deep(obj.value);
          if (obj?.text !== undefined) {
            let out = deep(obj.text);
            if (obj?.extra) out += deep(obj.extra);
            return out;
          }
          if (typeof obj === 'object') return Object.values(obj).map(deep).join('');
          return '';
        };

        const msg = deep(reason);
        console.log(`[Bot KICKED] ${msg}`);

        const shouldRejoin = msg.includes('analyzing your connection') || msg.includes('re-join') || msg.includes('re') || msg.includes('reconnect') || msg.includes('flame') || msg.includes('queued for verification') || msg.includes('ระบบ') || msg.includes('บอท') || msg.includes('ระบบป้องกัน') || msg.includes('เข้า') || msg.includes('เข้าใหม่') || msg.includes('ใหม่') || msg.includes('อีกครั้ง');

        const doRejoin = (attempt) => {
          if (attempt > 3) {
            console.log(`[Bot] Max rejoin attempts reached for ${username}`);
            return;
          }

          console.log(`[Bot] Rejoining ${username} in 10s... (attempt ${attempt}/3)`);
          setTimeout(() => {
            delete botz[server][username];
            if (statuz[server]?.[username]) {
              statuz[server][username].connected = false;
            }

            const newBot = createBot(options);
            botz[server][username] = newBot;

            newBot._client.on('add_resource_pack', (data) => {
              try {
                const url = data.url || 'unknown';
                const hash = data.hash || 'unknown';
                console.log(`[~] Bot ${username} accepting resource pack: ${url} (hash: ${hash})`);
              } catch { }
              newBot._client.write('resource_pack_receive', { uuid: data.uuid, result: 3 });
              newBot._client.write('resource_pack_receive', { uuid: data.uuid, result: 0 });
            });

            newBot.on('spawn', () => {
              console.log(`[Bot] Rejoined ${username} (attempt ${attempt})`);
              statuz[server][username].connected = true;
            });

            newBot.on('kicked', reason => {
              const msg2 = deep(reason);
              console.log(`[Bot KICKED after rejoin] ${msg2}`);
              const shouldRejoinAgain = msg2.includes('analyzing your connection') || msg2.includes('re-join') || msg2.includes('queued for verification') || msg2.includes('ระบบ') || msg2.includes('บอท') || msg2.includes('ระบบป้องกัน') || msg2.includes('เข้า') || msg2.includes('เข้าใหม่') || msg2.includes('ใหม่') || msg2.includes('อีกครั้ง');
              if (shouldRejoinAgain) doRejoin(attempt + 1);
            });

            newBot.on('error', err => {
              if (err.message?.includes('PartialReadError')) return;
              if (err.message?.includes('Chunk size')) return;
              console.log(`[Bot ERROR]`, err.message);
            });

            newBot.on('end', () => {
              console.log(`[Bot DISCONNECTED after rejoin]`);
              if (statuz[server]?.[username]) {
                statuz[server][username].connected = false;
              }
            });

          }, 10000);
        };

        if (shouldRejoin) doRejoin(1);

      } catch {
        console.log(`[Bot KICKED]`, reason);
      }
    })

    bot.on('end', () => {
      console.log(`[Bot DISCONNECTED]`)
      if (statuz[server]?.[username]) {
        statuz[server][username].connected = false
      }
    })

    botz[server] = botz[server] || {};
    statuz[server] = statuz[server] || {};
    botz[server][username] = bot;
    statuz[server][username] = { connected: false, username };

    res.json({ message: 'Bot connecting...', server, username, status: 'connecting' });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: `Connection failed: ${err.message}` });
  }
});


app.post('/send', (req, res) => {
  const { host, port = 25565, username, message } = req.body;
  const server = `${host}:${port}`;
  const bot = botz[server]?.[username];
  if (!bot) return res.status(400).json({ error: 'No bot with this username connected.' });

  bot.chat(message);
  res.json({ message: `Sent to ${server} by ${username}: ${message}` });
});

app.post('/disconnect', (req, res) => {
  const { host, port = 25565, username } = req.body;
  const server = `${host}:${port}`;
  const bot = botz[server]?.[username];
  const status = statuz[server]?.[username];

  if (!bot || !status) return res.status(400).json({ error: 'No bot connected.' });

  bot.quit();
  delete botz[server][username];
  delete statuz[server][username];
  if (!Object.keys(botz[server]).length) delete botz[server];
  if (!Object.keys(statuz[server]).length) delete statuz[server];

  res.json({ message: `Bot ${username} disconnected from ${server}` });
});

app.get('/status', (req, res) => res.json(Object.keys(statuz).length ? statuz : { connected: false }));
app.listen(port, () => console.log(`   ─╼ API listening on http://localhost:${port}`));