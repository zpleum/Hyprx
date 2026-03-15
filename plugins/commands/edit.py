from plugins.common import *
import json
import os
import sys
import time
from plugins.discord_rpc import AUTO_IDLE, AUTO_IDLE_TIME
import plugins.discord_rpc as rpc

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

languages = ["english", "thai"]
themes = ["hyprx", "galaxy", "sakura", "midnight", "lily", "ocean", "mint", "rose", "neon", "lava", "forest", "snow", "coffee", "sunset", "charcoal"]

RELOAD_KEYS = ["language", "theme"]

ALIASES = {
    "auto_idle": "rpc.auto_idle",
    "idle_time": "rpc.auto_idle_time"
}

def edit(tf, value=None):
    global default
    if not os.path.exists("config.json"):
        logging.error("Config file does not exist.")
        return

    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)

    if tf in ALIASES:
        tf = ALIASES[tf]

    keys = tf.split('.')
    ohio = default
    for k in keys:
        if not isinstance(ohio, dict) or k not in ohio:
            logging.error(f"Key invalid: {'.'.join(keys)}")
            return
        ohio = ohio[k]

    d = config
    for k in keys[:-1]:
        if not isinstance(d, dict) or k not in d:
            logging.error(f"Invalid Key: {'.'.join(keys)}")
            return
        d = d[k]

    final_key = keys[-1]

    if value is None:
        if tf == "language":
            logging.info(f"Values for language: {white}{', '.join(languages)}")
        elif tf == "theme":
            logging.info(f"Values for theme: {white}{', '.join(themes)}")
        else:
            logging.info(f"{tf} = {d.get(final_key)}")
        return

    if isinstance(d.get(final_key), bool) and isinstance(value, str):
        if value.lower() in ['true', '1', 'yes']:
            value = True
        elif value.lower() in ['false', '0', 'no']:
            value = False
    elif isinstance(d.get(final_key), int):
        try:
            value = int(value)
        except ValueError:
            logging.error("Value must be a number")
            return

    d[final_key] = value
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    logging.success(f"{tf} = {value}")

    if tf == "rpc.auto_idle":
        rpc.AUTO_IDLE = value
        logging.info(f"RPC Auto Idle → {value}")

    if tf == "rpc.auto_idle_time":
        rpc.AUTO_IDLE_TIME = value
        logging.info(f"RPC Idle Time → {value}s")

    if tf in RELOAD_KEYS:
        time.sleep(0.5)
        logging.info('Reloading Hyprx...')
        time.sleep(0.5)
        os.execv(sys.executable, [sys.executable] + sys.argv)