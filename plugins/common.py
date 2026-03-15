import os
import re
import json
import time
import random
import requests
import threading
from bs4 import BeautifulSoup
from plugins.logging import *
from plugins.theme import theme
from colorama import Fore, Style
import time
import sys

prots = ["TCPShield", 'NeoProtect', 'Cloudflare', "craftserve.pl"]
colorz = theme()
white = colorz['white']
reset = '\033[0m'
yellow = colorz['yellow']
red = colorz['red']
green = colorz['green']
gray = '\033[38;2;120;120;140m'
dim = '\033[38;2;80;80;100m'
underline = '\033[4m'
hide = "\033[?25l"
show = "\033[?25h"

VERSION = "v1.0"

def ranproxy():
    with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    if not proxies:
        return None
    return random.choice(proxies)

def is_protected(host):
    try:
        url = f"http://{host}"
        response = requests.get(url, timeout=5, allow_redirects=False)
        gangster = response.text.lower()
        if 300 <= response.status_code < 400:
            location = response.headers.get("Location")
            if location:
                if "tcpshield" in location: return "TCPShield"
                elif "craftserve.pl" in location: return "craftserve.pl"
                elif "neoprotect" in location: return "NeoProtect"
        if "cloudflare" in gangster: return "Cloudflare"
        elif "tcpshield" in gangster: return "TCPShield"
        elif "craftserve.pl" in gangster: return "craftserve.pl"
        elif "neoprotect" in gangster: return "NeoProtect"
        else: return 'Unprotected'
    except:
        return 'Unprotected'

def firstload():
    if not os.path.exists("hyprx"):
        with open("hyprx", "w") as f:
            f.write('')
        return True
    return False

def hyprxc():
    default = {
        "language": "english",
        "theme": "hyprx",
        "server": {
            "port": 23457,
            "randomize_port": False
        },
        "rpc": {
            "auto_idle": True,
            "auto_idle_time": 300
        }
    }
    if not os.path.exists('config.json'):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default, f, indent=2)
        return default

    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    change = False
    if not isinstance(config['server']['port'], int) or not (1 <= config['server']['port'] <= 65535):
        config["server"]["port"] = default["server"]["port"]
        change = True
    if not isinstance(config['server']['randomize_port'], bool):
        config["server"]["randomize_port"] = default["server"]["randomize_port"]
        change = True
    valid_languages = {'jordanian', 'english', 'persian'}
    if config['language'] not in valid_languages:
        config["language"] = default["language"]
        change = True
    if change:
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    return config

def getstring(key):
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    lang = config['language']
    try:
        with open(f"./translations/{lang}.json", 'r', encoding='utf-8') as f:
            strings = json.load(f)
    except FileNotFoundError:
        with open("./translations/english.json", 'r', encoding='utf-8') as f:
            strings = json.load(f)
    return strings.get(key, f"[Missing string for '{key}']")

def animate():
    print("\033c", end="")
    tw = os.get_terminal_size().columns
    art = [
        "██╗  ██╗ ██╗   ██╗ ██████╗  ██████╗  ██╗  ██╗",
        "██║  ██║ ╚██╗ ██╔╝ ██╔══██╗ ██╔══██╗ ╚██╗██╔╝",
        "███████║  ╚████╔╝  ██████╔╝ ██████╔╝  ╚███╔╝  ",
        "██╔══██║   ╚██╔╝   ██╔═══╝  ██╔══██╗  ██╔██╗  ",
        "██║  ██║    ██║    ██║      ██║  ██║  ██╔╝██╗ ",
        "╚═╝  ╚═╝    ╚═╝    ╚═╝      ╚═╝  ╚═╝  ╚═╝  ╚═╝",
    ]

    art_w = max(len(l) for l in art)
    pad_left = (tw - art_w) // 2
    pad = ' ' * pad_left
    shine = 8
    delay = 0.006

    print(hide, end="")
    try:
        for p in range(-shine, art_w + shine):
            print("\033[H", end="")
            print()
            for line in art:
                s = pad
                for i, c in enumerate(line):
                    dist = abs(i - p)
                    if dist == 0:
                        s += '\033[38;2;255;255;255m' + c
                    elif dist <= 2:
                        s += '\033[38;2;180;220;255m' + c
                    elif dist <= shine:
                        s += yellow + c
                    else:
                        s += dim + c
                print(s + reset)
            print()
            time.sleep(delay)
    finally:
        print(show, end="")

def loadmenu():
    print("\033c", end="")
    tw = os.get_terminal_size().columns
    art = [
        "██╗  ██╗ ██╗   ██╗ ██████╗  ██████╗  ██╗  ██╗",
        "██║  ██║ ╚██╗ ██╔╝ ██╔══██╗ ██╔══██╗ ╚██╗██╔╝",
        "███████║  ╚████╔╝  ██████╔╝ ██████╔╝  ╚███╔╝  ",
        "██╔══██║   ╚██╔╝   ██╔═══╝  ██╔══██╗  ██╔██╗  ",
        "██║  ██║    ██║    ██║      ██║  ██║  ██╔╝██╗ ",
        "╚═╝  ╚═╝    ╚═╝    ╚═╝      ╚═╝  ╚═╝  ╚═╝  ╚═╝",
    ]
    art_w = max(len(l) for l in art)
    pad = ' ' * ((tw - art_w) // 2)
    print()
    for line in art:
        print(f"{pad}{yellow}{line}{reset}")
    print()

from datetime import datetime

def repostuff():
    repo = "https://api.github.com/repos/zPleum/Hyprx"
    data = requests.get(repo).json()
    stars = data.get("stargazers_count", 0)
    updated = data.get("updated_at")
    return stars, updated, VERSION

def stats(stars, updated, version):
    if updated:
        updated = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %b %Y")
    else:
        updated = "N/A"

    user = os.getlogin()
    tw = os.get_terminal_size().columns

    rows = [
        ("stars  ", str(stars)),
        ("updated", updated),
        ("user   ", user),
        ("credit ", "Hyprx modified by zPleum, based on Banana by x5ten"),
    ]

    title_text = f"  Hyprx {version}"
    max_row = max(len(f"  {l}  {v}") for l, v in rows)
    W = min(max(len(title_text), max_row) + 10, tw - 4)

    pad_left = ' ' * max(0, (tw - W - 2) // 2)

    def row(label, value):
        inner = f"  {label}  {value}"
        if len(inner) > W:
            value = value[:W - len(f"  {label}  ") - 3] + "..."
            inner = f"  {label}  {value}"
        pad = W - len(inner)
        return f"{pad_left}{dim}│{gray}  {label}  {white}{value}{' ' * pad}{dim}│{reset}"

    top   = f"{pad_left}{dim}╭{'─' * W}╮{reset}"
    title = f"{pad_left}{dim}│{yellow}  Hyprx {white}{version}{' ' * (W - len(title_text))}{dim}│{reset}"
    sep   = f"{pad_left}{dim}├{'─' * W}┤{reset}"
    bot   = f"{pad_left}{dim}╰{'─' * W}╯{reset}"

    print()
    print(top)
    print(title)
    print(sep)
    for label, value in rows:
        print(row(label, value))
    print(bot)
    print()

def initialize():
    if firstload() == True:
        print("\033c", end="")
        print(rf'''
{yellow}
  ██╗  ██╗██╗   ██╗██████╗ ██████╗ ██╗  ██╗
  ██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗╚██╗██╔╝
  ███████║ ╚████╔╝ ██████╔╝██████╔╝ ╚███╔╝ 
  ██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══██╗ ██╔██╗ 
  ██║  ██║   ██║   ██║     ██║  ██║██╔╝ ██╗
  ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝
{reset}
  {gray}welcome, {white}{os.getlogin()}{gray}.
  {getstring('initmsg')}{reset}
''')
        node()
        velocity()
        animate()
        loadmenu()

    elif firstload() == False:
        animate()
        loadmenu()

def scrapeproxy(ptype):
    if ptype.lower() not in ['socks5', 'socks4']:
        logging.error('Please enter a valid proxy type (socks5, socks4)')
        return
    proxies = []
    try:
        response = requests.get(f'https://raw.githubusercontent.com/RattlesHyper/proxy/main/{ptype}', timeout=5)
        for site in response.text.splitlines():
            r = requests.get(site)
            for proxy in r.text.splitlines():
                proxies.append(f'{ptype}://{proxy}')
        logging.info(f'Fetched {len(proxies)} {ptype} proxies')
        return proxies
    except Exception as e:
        logging.error(e)
        return

def checkserver(server):
    if ':' in server:
        server = server.split(':')[0]
    if server == 'localhost': return True
    ipre = r'^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)$'
    domre = r'^(?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})$'
    if re.match(domre, server) or re.match(ipre, server):
        return True
    return False

def checkip(ip):
    ipre = r'^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)$'
    if re.match(ipre, ip): return True
    if '*' in ip: return True
    return False