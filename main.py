import threading
import importlib.util
import win32api
from plugins.initialize import *
from plugins.common import *
from plugins.logging import *
from plugins.commands.server import server
from plugins.commands.uuid import puuid
from plugins.commands.rcon import rcon
from plugins.commands.rconbrut import rconbrut
from plugins.commands.fuzz import fuzz
from plugins.commands.ipinfo import ipinfo
from plugins.commands.dns import lookup
from plugins.commands.checker import check
from plugins.commands.scan import mcscan
from plugins.commands.scan import scan
from plugins.commands.monitor import monitor
from plugins.commands.proxy import proxy
from plugins.commands.connect import connect
from plugins.commands.kick import kick
from plugins.commands.shell import shell
from plugins.commands.ogmur import ogmur
from plugins.commands.ogv2 import ogv2
from plugins.commands.target import target
from plugins.commands.fakeproxy import fakeproxy
from plugins.commands.fetch import fetch
from plugins.commands.edit import edit
from plugins.commands.bungeeguard import bungee
from plugins.commands.websearch import web
from plugins.commands.pterodactyl import ptero
from plugins.commands.iphistory import iphistory
from plugins.commands.sendmsg import sendmsg
from plugins.commands.tcpflood import tcpflood
from plugins.commands.udpflood import udpflood
from plugins.commands.logflood import logflood

scripts = {}

stars, updated, version = repostuff()
clear = lambda: loadmenu(); print("\033c", end="")

def flush():
    print("\033c", end="")
    loadmenu()
    stats(stars, updated, version)

def getcmds():
    return {
        'iphistory':    (iphistory, 1, 0, getstring('iphistoryh')),
        'websearch':    (web, 0, 0, getstring('websearchh')),
        'server':       (server, 1, 0, getstring('serverh')),
        'edit':         (edit, 1, 1, getstring('edith')),
        'bungeeguard':  (bungee, 2, 0, getstring('bungeeguardh')),
        'ptero':        (ptero, 1, 0, getstring('pteroh')),
        'uuid':         (puuid, 1, 0, getstring('uuidh')),
        'ipinfo':       (ipinfo, 1, 0, getstring('ipinfoh')),
        'fetch':        (fetch, 1, 0, getstring('fetchh')),
        'monitor':      (monitor, 1, 0, getstring('monitorh')),
        'dns':          (lookup, 1, 0, getstring('dnsh')),
        'target':       (target, 1, 0, getstring('targeth')),
        'proxy':        (proxy, 2, 0, getstring('proxyh')),
        'fakeproxy':    (fakeproxy, 2, 0, getstring('fakeproxyh')),
        'check':        (check, 1, 0, getstring('checkh')),
        'mcscan':       (mcscan, 3, 0, getstring('mcscanh')),
        'scan':         (scan, 3, 0, getstring('scanh')),
        'clear':        (flush, 0, 0, getstring('clearh')),
        'update':       (upd, 0, 0, getstring('updateh')),
        'kick':         (kick, 2, 1, getstring('kickh')),
        'shell':        (shell, 3, 0, getstring('shellh')),
        'connect':      (connect, 2, 1, getstring('connecth')),
        'rcon':         (rcon, 2, 0, getstring('rconh')),
        'brutrcon':     (rconbrut, 2, 0, getstring('brutrconh')),
        'fuzz':         (fuzz, 3, 0, getstring('fuzzh')),
        'ogmur':        (ogmur, 4, 2, getstring('ogmurh')),
        'ogv2':         (ogv2, 4, 2, getstring('ogv2h')),
        'sendmsg':      (sendmsg, 2, 0, getstring('sendmsgh')),
        'tcpflood':     (tcpflood, 2, 0, getstring('tcpfloodh')),
        'udpflood':     (udpflood, 2, 0, getstring('udpfloodh')),
        'logflood':     (logflood, 2, 0, getstring('logfloodh')),
        'reload':       (reload, 0, 0, getstring('reloadh')),
        'exit':         (exit, 0, 0, getstring('exith'))
    }

def chelp(command=None):
    commands = getcmds()
    tw = os.get_terminal_size().columns

    c1 = yellow
    c2 = '\033[38;2;120;100;200m'
    d1 = white
    d2 = '\033[38;2;140;160;200m'

    if command is None:
        entries = []
        for cmd, entry in sorted(commands.items()):
            msg = entry[2] if len(entry) == 3 else entry[3]
            lines = msg.strip().splitlines()
            desc = lines[1].strip() if len(lines) > 1 else lines[0].strip()
            entries.append((cmd, desc))

        maxcmd = max(len(cmd) for cmd, _ in entries)
        maxdesc = max(len(desc) for _, desc in entries)
        maxdesc = min(maxdesc, tw - maxcmd - 16)
        W = maxcmd + maxdesc + 12
        pad = ' ' * ((tw - W) // 2)

        header = "  COMMANDS  "

        maxcmd = max(len(cmd) for cmd, _ in entries)
        maxdesc = max(len(desc) for _, desc in entries)
        maxdesc = min(maxdesc, tw - maxcmd - 16)

        W = maxcmd + maxdesc + 8

        pad = ' ' * ((tw - W - 2) // 2)

        top_bar = W - len(header)
        left_bar = top_bar // 2
        right_bar = top_bar - left_bar

        print()
        print(f"{pad}{dim}╭{'─' * left_bar}{gray}{header}{dim}{'─' * right_bar}╮{reset}")
        print(f"{pad}{dim}│  {gray}{'COMMAND'.ljust(maxcmd)}    {'DESCRIPTION'.ljust(maxdesc)}  {dim}│{reset}")
        print(f"{pad}{dim}├{'─' * (maxcmd + 4)}┼{'─' * (maxdesc + 4)}┤{reset}")

        for i, (cmd, desc) in enumerate(entries):
            cc = c1 if i % 2 == 0 else c2
            dc = d1 if i % 2 == 0 else d2
            desc_trimmed = desc[:maxdesc]
            print(f"{pad}{dim}│  {cc}{cmd.ljust(maxcmd)}    {dc}{desc_trimmed.ljust(maxdesc)}  {dim}│{reset}")

        print(f"{pad}{dim}╰{'─' * (maxcmd + 4)}┴{'─' * (maxdesc + 4)}╯{reset}")
        print()

    elif command in commands:
        msg = commands[command][2] if len(commands[command]) == 3 else commands[command][3]
        lines = msg.strip().splitlines()
        W = max(len(l.strip()) for l in lines) + 6
        W = min(W, tw - 4)
        pad = ' ' * ((tw - W - 2) // 2)
        print()
        print(f"{pad}{dim}╭{'─' * W}╮{reset}")
        for line in lines:
            l = line.strip()[:W-2]
            print(f"{pad}{dim}│  {white}{l.ljust(W - 4)}  {dim}│{reset}")
        print(f"{pad}{dim}╰{'─' * W}╯{reset}")
        print()

    elif command in scripts:
        print(scripts[command]['usage'])
    else:
        print(f"  {dim}unknown command {gray}'{yellow}{command}{gray}'{reset}  —  {white}type {yellow}help{white} for commands{reset}")

def loadscripts(folder='scripts'):
    if not os.path.exists(folder): return
    for filename in os.listdir(folder):
        if filename.endswith('.py'):
            path = os.path.join(folder, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            name = filename[:-3]
            scripts[name] = {
                "module": module,
                "arguments": getattr(module, 'arguments', []),
                "usage": getattr(module, 'usage', ''),
            }

_api_title = "Hyprx — API"
_main_title = "Hyprx — MAIN"
_api_process = None
_shutting_down = False
_reloading = False

def api():
    global _api_process

    gg = os.path.join(os.getcwd(), "api")

    if os.name == "nt":
        cmd = (
            f'title "{_api_title}" && '
            f'color 0B && '
            f'echo. && '
            f'echo   +--------------------------------------------------+ && '
            f'echo   ^|              H Y P R X   A P I                  ^| && '
            f'echo   ^|         Listening on port 6767                  ^| && '
            f'echo   +--------------------------------------------------+ && '
            f'echo. && '
            f'node server.mjs'
        )

        _api_process = subprocess.Popen(
            ["cmd", "/k", cmd],
            cwd=gg,
            creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP
        )
def watch_api():
    global _shutting_down
    time.sleep(1)

    while not _shutting_down:
        if _api_process and _api_process.poll() is not None:

            if _reloading:
                return

            print("\n  API closed. shutting down Hyprx...")
            _shutting_down = True
            os.kill(os.getpid(), 9)

        time.sleep(1)

def kill_api():
    global _api_process

    if _api_process and _api_process.poll() is None:
        subprocess.run(
            f"taskkill /F /T /PID {_api_process.pid}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def reload():
    import sys
    global _reloading

    logging.info('Reloading Hyprx...')
    _reloading = True

    kill_api()
    time.sleep(1)

    os.execv(sys.executable, [sys.executable] + sys.argv)

def execmd(cmd):
    commands = getcmds()
    try:
        part = cmd.split()
        if len(part) == 0: return
        command, *args = part

        if command == "help":
            chelp(args[0] if args else None)
            return

        if command in commands:
            func, required_args, *rest = commands[command]
            optional_args = 0
            usage = ''
            if rest:
                if len(rest) == 2:
                    optional_args, usage = rest
                else:
                    usage = rest[0]

            total = required_args + optional_args
            if len(args) >= required_args:
                if total == 0:
                    func()
                else:
                    merged = args[:total - 1] + [' '.join(args[total - 1:])] if len(args) >= total else args
                    func(*merged)
            else:
                print(usage)
            return

        if command in scripts:
            script = scripts[command]
            if len(args) >= len(script["arguments"]):
                merged_args = args[:len(script["arguments"]) - 1] + [' '.join(args[len(script["arguments"]) - 1:])]
                script["module"].run(dict(zip(script["arguments"], merged_args)))
            else:
                print(script["usage"])
            return

        print(f"  {dim}unknown command {gray}'{yellow}{command}{gray}'{reset}  —  {white}type {yellow}help{white} for commands{reset}")

    except Exception as e:
        logging.error(e)

def console_handler(event):
    global _shutting_down
    _shutting_down = True
    kill_api()
    return True

win32api.SetConsoleCtrlHandler(console_handler, True)

if __name__ == '__main__':
    if os.name == 'nt':
        os.system(f'title {_main_title}')
    initialize()
    api()
    threading.Thread(target=watch_api, daemon=True).start()
    loadscripts()
    stats(stars, updated, version)

    while True:
        try:
            cmd = input(f'\n  {dim}┌─{yellow}Hyprx{dim}─╼{reset} ')
            if not cmd.strip():
                print(f'  {dim}└╼  {gray}{getstring("helphint")}{reset}')
                continue
            print(f'  {dim}└╼{reset} ', end='', flush=True)
            execmd(cmd)
        except KeyboardInterrupt:
            print()
            exit()
        except EOFError:
            pass