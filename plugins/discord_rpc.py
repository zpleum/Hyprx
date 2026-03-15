from pypresence import Presence
import time
import threading

CLIENT_ID = '1482373256219594823'

ICON_MAIN = 'hyprx'
ICON_IDLE = 'hyprx_idle'

RPC = None
START_TIME = None
_ready = False
LAST_ACTIVITY = time.time()
IDLE = False
AUTO_IDLE = True
AUTO_IDLE_TIME = 300

def set_config(auto_idle, auto_idle_time):
    global AUTO_IDLE, AUTO_IDLE_TIME
    AUTO_IDLE = auto_idle
    AUTO_IDLE_TIME = float(auto_idle_time)

def init_rpc(client_id):
    global RPC, START_TIME, _ready

    def _connect():
        global RPC, START_TIME, _ready
        try:
            RPC = Presence(client_id)
            RPC.connect()
            START_TIME = time.time()
            _ready = True
            update_rpc(state='Starting Hyprx...')
            threading.Thread(target=_idle_watchdog, daemon=True).start()
        except Exception:
            _ready = False

    threading.Thread(target=_connect, daemon=True).start()

def _idle_watchdog():
    global IDLE
    while True:
        if AUTO_IDLE:
            elapsed = time.time() - LAST_ACTIVITY
            if not IDLE and elapsed >= AUTO_IDLE_TIME:
                set_idle()
        time.sleep(1)

def set_idle():
    global IDLE
    if not RPC or not _ready: return
    try:
        RPC.update(
            state="Idling",
            details="Hyprx - CLI toolkit for Minecraft",
            start=START_TIME,
            large_image=ICON_IDLE,
            large_text="System is Idle"
        )
        IDLE = True
    except: pass

def activity():
    global LAST_ACTIVITY, IDLE
    LAST_ACTIVITY = time.time()
    
    if IDLE:
        IDLE = False
        update_rpc(state='Finding server to exploit')

def update_rpc(state=None, details='Hyprx - CLI toolkit for Minecraft'):
    global RPC, _ready, IDLE
    if not RPC or not _ready: return
    
    if state is None:
        state = 'Finding server to exploit'

    current_icon = ICON_IDLE if IDLE else ICON_MAIN

    try:
        RPC.update(
            state=state, 
            details=details, 
            start=START_TIME,
            large_image=current_icon,
            large_text="Hyprx Minecraft Toolkit"
        )
    except: pass

def stop_rpc():
    global RPC, _ready
    if RPC:
        try: RPC.close()
        except: pass
    RPC = None
    _ready = False