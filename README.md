# Hyprx 🕹️ - **A free and improved alternative to MCPTool**

This project is based on Banana by x5ten.
Modifications and improvements were made in Hyprx.

<h1 align="center">
  <img src="https://i.postimg.cc/WzVsMTfx/image.png" alt="Header Image" style="width:80%; max-width:600px;"/>
</h1>

---

## 📜 License Notice

**Hyprx** is a modified version of the original project **Banana**.

- **Original Creator:** x5ten (@x5ten on Discord)
- **Original Project:** Banana
- **Original Repository:** [https://github.com/Renovsk/Banana](https://github.com/Renovsk/Banana)

This project continues to be distributed under the **GNU General Public License v3.0**.
In accordance with the GPLv3 and the original author's request, this software remains free to use and modify, provided that all derivatives also carry the same license and proper credits.

---

# 📦 Installation

## Requirements

- Python **3.10+**
- Winget package manager *(Windows only)*

## Setup

```bash
git clone https://github.com/zPleum/Hyprx.git
cd Hyprx
pip install -r requirements.txt
python main.py / Open 'START Hyprx.bat'
```

---

# ⚙️ Features

## Commands

| Command         | Arguments                                                                       | Description                                                       |
| --------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `b64`           | `<encode/decode> <text>`                                                        | Encodes or decodes a string using base64                          |
| `botchat`       | `<server> <message> [username/all]`                                             | Sends a chat message via a connected bot                          |
| `botdisconnect` | `<server> [username/all]`                                                       | Disconnects a bot from a server                                   |
| `botspam`       | `<server> <message> [delay] [username/all]`                                     | Spams a server with messages using connected bots                 |
| `brutrcon`      | `<server> <file>`                                                               | Brute-forces RCON using passwords from a file                     |
| `bungeecheck`   | `<server>`                                                                      | Checks if a server is vulnerable to IP forwarding                 |
| `bungeeguard`   | `<ip> <token>`                                                                  | Creates a BungeeGuard-authenticated proxy                         |
| `check`         | `<file>`                                                                        | Checks the status of Minecraft servers listed in a file           |
| `clear`         | N/A                                                                             | Clears the terminal screen                                        |
| `connect`       | `<username> <server> [version] [proxy]`                                         | Joins a server with a bot and lets you send messages              |
| `crack`         | `<hash> <wordlist> [algo] [threads]`                                            | Cracks a hash using a wordlist                                    |
| `crackcheck`    | `<server> <version>`                                                            | Checks if a Minecraft server is cracked or premium                |
| `dns`           | `<domain>`                                                                      | Shows all DNS records for a domain                                |
| `edit`          | `<language/theme> <value>`                                                      | Edits the Hyprx configuration                                     |
| `exit`          | N/A                                                                             | Exits Hyprx                                                       |
| `fakeproxy`     | `<ip> <mode>`                                                                   | Starts a Velocity proxy that logs all commands sent to the server |
| `fetch`         | `<socks4/socks5>`                                                               | Scrapes fresh proxies of the given type                           |
| `fuzz`          | `<url> <file> <threads>`                                                        | Fuzzes a URL for hidden paths or subdomains                       |
| `geoip`         | `<ip>`                                                                          | Shows detailed information about an IP address                    |
| `hash`          | `<algorithm/all> <text>`                                                        | Generates a hash of a string using a specified algorithm          |
| `httpflood`     | `<host> [threads]`                                                              | Floods a web server with HTTP GET requests                        |
| `iphistory`     | `<domain>`                                                                      | Retrieves historical IPv4 addresses for a domain                  |
| `ipinfo`        | `<ip>`                                                                          | Shows detailed information about an IP address                    |
| `kick`          | `<username> <server> <proxy>`                                                   | Kicks a player from a cracked server                              |
| `logflood`      | `<host:port> <coroutines>`                                                      | Floods a server with Minecraft login requests                     |
| `mcscan`        | `<ip> <range> <threads>`                                                        | Scans for Minecraft servers on a given IP range                   |
| `mcstatus`      | `<server>`                                                                      | Shows detailed information about a Minecraft server               |
| `monitor`       | `<ip>`                                                                          | Monitors player joins and leaves on a server (query required)     |
| `ogmur`         | `<users/random> <server> <commands> <keep> [count] [proxy] [delay] [version]`  | Connects bots sequentially and runs a command list                |
| `ogv2`          | `<users/random> <server> <commands> <keep> [count] [proxy] [version]`          | Connects bots in parallel threads and runs a command list         |
| `ping`          | `<host> [count]`                                                                | Pings a host and shows per-reply and summary stats                |
| `playerlist`    | `<server[:port]>`                                                               | Shows the online player list of a Minecraft server                |
| `proxy`         | `<ip> <mode>`                                                                   | Starts a Velocity proxy that redirects to the target server       |
| `proxycheck`    | `<file> [threads]`                                                              | Checks the status of proxies listed in a file                     |
| `proxyscrape`   | `<socks5/socks4/http> [output]`                                                 | Scrapes free proxies from multiple sources                        |
| `ptero`         | `<panel_url>`                                                                   | Exploits a vulnerability on a Pterodactyl panel                   |
| `rcon`          | `<server> <password>`                                                           | Connects to a server's RCON console                               |
| `reload`        | N/A                                                                             | Restarts Hyprx without closing the terminal                       |
| `reverseip`     | `<ip>`                                                                          | Finds all domains pointing to an IP address                       |
| `scan`          | `<ip> <range> <threads>`                                                        | Performs a multi-threaded TCP port scan on an IP address          |
| `server`        | `<address>`                                                                     | Shows information about a Minecraft server                        |
| `shell`         | `<host> <port> <bind_port>`                                                     | Listens on a port using netcat                                    |
| `slowloris`     | `<host> [port] [connections]`                                                   | Floods a web server with slow partial HTTP connections            |
| `synflood`      | `<host:port> <threads>`                                                         | Floods a server with TCP SYN packets (raw socket)                 |
| `target`        | `<domain>`                                                                      | Enumerates all subdomains and their resolved IPs                  |
| `tcpflood`      | `<host:port> <threads>`                                                         | Floods a server with TCP connections                              |
| `traceroute`    | `<host> [max_hops]`                                                             | Traces the network route to a host hop by hop                     |
| `udpflood`      | `<host:port> <processes>`                                                       | Floods a server with UDP packets                                  |
| `update`        | N/A                                                                             | Re-initializes and restarts Hyprx                                 |
| `uuid`          | `<ign>`                                                                         | Looks up a player's UUID by username                              |
| `websearch`     | N/A                                                                             | Crawls Minecraft server lists to discover and enumerate servers   |
| `whois`         | `<domain>`                                                                      | Shows detailed WHOIS information about a domain                   |

---

### ⚠️ Disclaimer

**This tool is for educational and ethical testing purposes only.** The developer of **Hyprx** is not responsible for any misuse, damage, or illegal activities caused by this software. Use it at your own risk. By using this tool, you agree to comply with your local laws and regulations regarding cybersecurity and network testing.