# Hyprx 🕹️ - High-performance tools for Minecraft automation and network analysis

> A powerful modular CLI toolkit for Minecraft server analysis, automation, and network testing

<h1 align="center">
  <img src="https://i.postimg.cc/GtCLVZnM/Hyprx.png" alt="Hyprx Logo" width="300" style="margin-right:40px;"/>
  <img src="https://i.postimg.cc/pLQgw8T1/Hyprx-Idle.png" alt="Hyprx Idle" width="300"/>
</h1>

<h1 align="center">
  <img src="https://i.postimg.cc/dtSM3ZhJ/image.png" alt="Hyprx Preview" width="700"/>
</h1>

<p align="center">

<img src="https://img.shields.io/github/stars/zPleum/Hyprx?style=for-the-badge&color=yellow"/>
<img src="https://img.shields.io/github/forks/zPleum/Hyprx?style=for-the-badge&color=blue"/>
<img src="https://img.shields.io/github/issues/zPleum/Hyprx?style=for-the-badge&color=red"/>
<img src="https://img.shields.io/github/license/zPleum/Hyprx?style=for-the-badge&color=green"/>
<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python"/>
<img src="https://img.shields.io/github/last-commit/zPleum/Hyprx?style=for-the-badge"/>

</p>

---

# 📌 Overview

**Hyprx** is a **modular command-line toolkit** designed for **Minecraft server analysis, automation, and network testing**.

It provides a large set of utilities for:

* Minecraft server reconnaissance
* bot automation
* proxy management
* network testing
* hash utilities

The project focuses on **performance, modularity, and extensibility**, allowing users to automate complex tasks directly from the CLI.

---

# 📜 License Notice

**Hyprx** is a modified version of the original project **Banana**.

| Item             | Value                                                                  |
| ---------------- | ---------------------------------------------------------------------- |
| Original Creator | x5ten                                                                  |
| Original Project | Banana                                                                 |
| Repository       | [https://github.com/x3fication/Banana](https://github.com/x3fication/Banana) |

This project continues to be distributed under the **GNU General Public License v3.0 (GPL-3.0)**.

In accordance with the GPL license:

* The software must remain **open source**
* Derivative works must **retain the same license**
* Proper **credit must be given to the original author**

---

# ⚙️ Core Capabilities

Hyprx combines several different tool categories into a single CLI interface.

### Minecraft Tools

* Server status inspection
* Player enumeration
* Bot automation
* Cracked / premium detection
* RCON interaction

### Network Tools

* TCP / UDP scanning
* traceroute and ping
* DNS and WHOIS lookups
* IP intelligence

### Proxy Utilities

* Proxy scraping
* Proxy validation
* Proxy-based automation

### Security Utilities

* Hash generation
* Wordlist-based hash cracking
* Web fuzzing
* Subdomain enumeration

---

# 🧠 Key Features

| Feature                       | Description                                     |
| ----------------------------- | ----------------------------------------------- |
| **Modular CLI Architecture**  | Commands are organized into independent modules |
| **Multi-Threaded Networking** | High performance scanning and requests          |
| **Bot Automation**            | Control Minecraft bots via CLI                  |
| **Proxy Integration**         | SOCKS / HTTP proxy scraping and validation      |
| **Network Recon Tools**       | DNS, WHOIS, traceroute, reverse IP lookup       |
| **Hash Utilities**            | Built-in hash generator and cracker             |
| **Extensible Command System** | Easy to add new commands                        |

---

# 📦 Installation

## Requirements

* **Python 3.10+**
* **Git**
* Windows / Linux / macOS

---

## Setup

Clone the repository

```bash
git clone https://github.com/zPleum/Hyprx.git
```

Enter the directory

```bash
cd Hyprx
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start Hyprx

```bash
python main.py
```

Windows users can alternatively launch:

```
START Hyprx.bat
```

---

# 🖥️ Example Usage

Example commands inside the CLI:

```bash
mcstatus hypixel.net
```

<h1 align="center">
  <img src="https://i.postimg.cc/PrGNSzZM/ex1.png" alt="Example Usage" width="700"/>
</h1>

```bash
playerlist play.cubecraft.net
```

<h1 align="center">
  <img src="https://i.postimg.cc/CLj5XBsg/ex2.png" alt="Example Usage" width="700"/>
</h1>

```bash
scan 192.168.1.1 20000-30000 100
```

<h1 align="center">
  <img src="https://i.postimg.cc/sgsxrjTB/ex3.png" alt="Example Usage" width="700"/>
</h1>

```bash
ogv2 random localhost bot_cmd.txt true 10 auto 1.21.11
```

<h1 align="center">
  <img src="https://i.postimg.cc/nh2zVyWG/ex4.png" alt="Example Usage" width="700"/>
</h1>

---

# 📚 Command List

Hyprx contains **40+ built-in commands**.

| Command       | Description                                 |
| ------------- | ------------------------------------------- |
| `check`       | Checks server status from a file            |
| `mcstatus`    | Shows detailed Minecraft server information |
| `playerlist`  | Retrieves online players                    |
| `connect`     | Connects a bot to a server                  |
| `botchat`     | Sends chat messages via bot                 |
| `botspam`     | Sends repeated messages                     |
| `proxycheck`  | Validates proxy lists                       |
| `proxyscrape` | Scrapes proxies from multiple sources       |
| `dns`         | Displays DNS records                        |
| `ogmur`       | Connects bots sequentially and runs a command list|
| `ogv2`        | Connects bots in parallel threads and runs a command list|
| `scan`        | Multi-threaded port scanner                 |
| `crack`       | Wordlist-based hash cracking                |
| `hash`        | Hash generator                              |
| `reverseip`   | Domain enumeration by IP                    |
| `fuzz`        | URL path fuzzing                            |

*(Full command documentation available in the CLI help menu.)*

---

# 📊 Architecture

Hyprx is built around a **command-based modular architecture**.

```
Hyprx
│
├─ api
│   └─ server.mjs
│
├─ plugins
│   ├─ commands
│   │   ├─ connect.py
│   │   ├─ ogmur.py
│   │   ├─ ogv2.py
│   │   ├─ mcstatus.py
│   │   ├─ reverseip.py
│   │   └─ synflood.py
│   │
│   ├─ common.py
│   ├─ discord_rpc.py
│   ├─ initialize.py
│   ├─ logging.py
│   ├─ theme.py
│   └─ default_proxies.txt
│
├─ proxy
│   ├─ fakeproxy
│   └─ velocity
│
├─ translations
│   ├─ english.json
│   └─ thai.json
│
├─ main.py
├─ config.json
└─ requirements.txt
```

This structure allows new commands to be added with minimal changes to the core system.

---

# 🚀 Performance

Hyprx uses **multi-threading and asynchronous networking** to improve speed in:

* port scanning
* proxy validation
* server enumeration
* bot automation

This allows the tool to handle **large scale network operations efficiently**.

---

# ⭐ Star History

<p align="center">
  <a href="https://star-history.com/#zPleum/Hyprx&Date">
    <img src="https://api.star-history.com/svg?repos=zPleum/Hyprx&type=Date" width="600"/>
  </a>
</p>

---

## 📜 License

Based on [Banana](https://github.com/x3fication/Banana) by x5ten.
Distributed under the **GNU General Public License v3.0** — free to use and modify, provided derivatives carry the same license and credits.

---

# ⚠️ Disclaimer

This software is intended **strictly for educational purposes, security research, and authorized testing environments**.

The developer of **Hyprx** is **not responsible for misuse, damage, or illegal activity** caused by this software.

By using this tool, you agree that:

* you have permission to test the target systems
* you comply with your **local cybersecurity laws**