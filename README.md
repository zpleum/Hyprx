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
````

---

# ⚙️ Features

## Commands

| Command       | Arguments                                                   | Description                                       |
| ------------- | ----------------------------------------------------------- | ------------------------------------------------- |
| `websearch`   | N/A                                                         | Crawls Minecraft server lists to discover servers |
| `server`      | `<address>`                                                 | Shows information about a Minecraft server        |
| `uuid`        | `<ign>`                                                     | Looks up a player's UUID                          |
| `edit`        | `<language/theme> <value>`                                  | Edits the Hyprx configuration                     |
| `ipinfo`      | `<ip>`                                                      | Shows detailed IP information                     |
| `iphistory`   | `<domain>`                                                  | Retrieves historical IPv4 addresses               |
| `dns`         | `<domain>`                                                  | Shows all DNS records                             |
| `target`      | `<domain>`                                                  | Enumerates subdomains and their IPs               |
| `fetch`       | `<socks4/socks5>`                                           | Scrapes fresh proxies                             |
| `monitor`     | `<ip>`                                                      | Monitors player joins/leaves (query required)     |
| `proxy`       | `<ip> <mode>`                                               | Starts a Velocity proxy redirecting traffic       |
| `fakeproxy`   | `<ip> <mode>`                                               | Starts a proxy that logs commands                 |
| `bungeeguard` | `<ip> <token>`                                              | Creates a BungeeGuard proxy                       |
| `check`       | `<file>`                                                    | Checks Minecraft server status from file          |
| `mcscan`      | `<ip> <range> <threads>`                                    | Scans ports for Minecraft servers                 |
| `scan`        | `<ip> <range> <threads>`                                    | Multi-threaded TCP port scan                      |
| `ogmur`       | `<users/random> <server> <commands> <keep> <count> <proxy>` | Sequential bot execution                          |
| `ogv2`        | `<users/random> <server> <commands> <keep> <count> <proxy>` | Multi-threaded bot execution                      |
| `connect`     | `<username> <server> <proxy>`                               | Connects a bot and allows messaging               |
| `sendmsg`     | `<server> <message> <username/all>`                         | Sends chat messages                               |
| `sendcmd`     | `<username> <server> <commands> <proxy>`                    | Bot executes commands from file                   |
| `kick`        | `<username> <server> <proxy>`                               | Kicks a player from cracked server                |
| `rcon`        | `<server> <password>`                                       | Connects to server RCON                           |
| `brutrcon`    | `<server> <file>`                                           | Brute-force RCON passwords                        |
| `fuzz`        | `<url> <file> <threads>`                                    | URL / subdomain fuzzing                           |
| `shell`       | `<host> <port> <bind_port>`                                 | Netcat listener                                   |
| `tcpflood`    | `<host:port> <threads>`                                     | Floods with TCP connections                       |
| `udpflood`    | `<host:port> <processes>`                                   | Floods with UDP packets                           |
| `logflood`    | `<host:port> <coroutines>`                                  | Floods Minecraft login packets                    |
| `clear`       | N/A                                                         | Clears the terminal                               |
| `reload`      | N/A                                                         | Restarts Hyprx                                    |
| `update`      | N/A                                                         | Re-initializes Hyprx                              |
| `exit`        | N/A                                                         | Exits the application                             |

### ⚠️ Disclaimer

**This tool is for educational and ethical testing purposes only.** The developer of **Hyprx** is not responsible for any misuse, damage, or illegal activities caused by this software. Use it at your own risk. By using this tool, you agree to comply with your local laws and regulations regarding cybersecurity and network testing.
