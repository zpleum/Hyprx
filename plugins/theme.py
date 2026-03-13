import json
from colorama import Fore, Style
from plugins.common import *

THEMES = {
    "hyprx": {
        "white": '\033[38;2;200;190;255m',
        "yellow": '\033[38;2;180;130;255m',
        "red": '\033[38;2;255;100;180m',
        "green": '\033[38;2;100;220;255m',
    },
    "galaxy": {
        "white": '\033[38;2;180;220;255m',
        "yellow": '\033[38;2;80;160;255m',
        "red": '\033[38;2;255;80;120m',
        "green": '\033[38;2;80;220;255m',
    },
    "sakura": {
        "white": '\033[38;2;255;240;245m',
        "yellow": '\033[38;2;255;182;193m',
        "red": '\033[38;2;255;105;135m',
        "green": '\033[38;2;200;230;180m',
    },
    "midnight": {
        "white": '\033[38;2;180;180;220m',
        "yellow": '\033[38;2;130;100;220m',
        "red": '\033[38;2;220;80;120m',
        "green": '\033[38;2;80;200;160m',
    },
    "lily": {
        "white": '\033[38;2;217;224;238m',
        "yellow": '\033[38;2;245;194;231m',
        "red": '\033[38;2;242;143;173m',
        "green": '\033[38;2;171;233;179m',
    },
    "ocean": {
        "white": '\033[38;2;220;240;255m',
        "yellow": '\033[38;2;100;200;255m',
        "red": '\033[38;2;255;100;100m',
        "green": '\033[38;2;100;255;200m',
    },
    "mint": {
        "white": '\033[38;2;220;255;245m',
        "yellow": '\033[38;2;150;255;220m',
        "red": '\033[38;2;255;120;150m',
        "green": '\033[38;2;100;230;180m',
    },
    "rose": {
        "white": '\033[38;2;255;235;235m',
        "yellow": '\033[38;2;255;180;180m',
        "red": '\033[38;2;220;60;80m',
        "green": '\033[38;2;180;220;160m',
    },
    "neon": {
        "white": '\033[38;2;220;220;220m',
        "yellow": '\033[38;2;255;255;0m',
        "red": '\033[38;2;255;0;100m',
        "green": '\033[38;2;0;255;100m',
    },
    "lava": {
        "white": '\033[38;2;255;220;200m',
        "yellow": '\033[38;2;255;150;50m',
        "red": '\033[38;2;255;50;50m',
        "green": '\033[38;2;255;200;50m',
    },
    "forest": {
        "white": '\033[38;2;210;230;210m',
        "yellow": '\033[38;2;180;230;140m',
        "red": '\033[38;2;255;120;80m',
        "green": '\033[38;2;120;255;120m',
    },
    "snow": {
        "white": '\033[38;2;230;230;230m',
        "yellow": '\033[38;2;192;237;249m',
        "red": Fore.LIGHTRED_EX,
        "green": Fore.LIGHTGREEN_EX,
    },
    "coffee": {
        "white": '\033[38;2;240;220;190m',
        "yellow": '\033[38;2;210;170;110m',
        "red": '\033[38;2;200;80;60m',
        "green": '\033[38;2;160;200;120m',
    },
    "sunset": {
        "white": '\033[38;2;235;219;178m',
        "yellow": '\033[38;2;255;189;89m',
        "red": Fore.RED + Style.BRIGHT,
        "green": Fore.YELLOW + Style.BRIGHT,
    },
    "charcoal": {
        "white": '\033[38;2;213;210;221m',
        "yellow": '\033[38;2;98;114;164m',
        "red": '\033[38;2;255;85;85m',
        "green": '\033[38;2;80;250;123m',
    },
}

def theme():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except:
        return THEMES["hyprx"]

    theme_name = str(config['theme']).lower()

    if theme_name not in THEMES:
        theme_name = "hyprx"

    return THEMES[theme_name]