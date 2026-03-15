from pypresence import Presence
import time
import threading

RPC = None
START_TIME = None
_ready = False

LAST_ACTIVITY = time.time()
IDLE = False

AUTO_IDLE = True
AUTO_IDLE_TIME = 300

def init_rpc(client_id):
    global RPC, START_TIME, _ready

    def _connect():
        global RPC, START_TIME, _ready
        try:
            RPC = Presence(client_id)
            RPC.connect()
            START_TIME = time.time()
            _ready = True
            update_rpc(state='Starting Hyprx...', details='Hyprx - CLI toolkit for Minecraft')
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
            elif IDLE and elapsed < AUTO_IDLE_TIME:
                IDLE = False
                update_rpc()
        time.sleep(1)

def set_idle():
    global IDLE
    if not RPC or not _ready: return
    try:
        RPC.update(
            state="Idle",
            details="Hyprx - CLI toolkit for Minecraft",
            start=START_TIME
        )
        IDLE = True
    except: pass

def activity():
    global LAST_ACTIVITY, IDLE
    LAST_ACTIVITY = time.time()
    
    if IDLE:
        IDLE = False
        update_rpc(
            state='Finding server to exploit', 
            details='Hyprx - CLI toolkit for Minecraft'
        )

def update_rpc(state='Finding server to exploit', details='Hyprx - CLI toolkit for Minecraft'):
    global RPC, _ready
    if not RPC or not _ready: return
    
    global LAST_ACTIVITY, IDLE
    LAST_ACTIVITY = time.time()
    IDLE = False 

    try:
        RPC.update(state=state, details=details, start=START_TIME)
    except: pass


def stop_rpc():
    global RPC, _ready

    if RPC:
        try:
            RPC.close()
        except:
            pass

    RPC = None
    _ready = False