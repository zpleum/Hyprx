from pypresence import Presence
import time
import threading

RPC = None
START_TIME = None
_ready = False

def init_rpc(client_id):
    global RPC, START_TIME, _ready

    def _connect():
        global RPC, START_TIME, _ready
        for attempt in range(5):
            try:
                RPC = Presence(client_id)
                RPC.connect()
                START_TIME = time.time()
                _ready = True
                update_rpc(state='Finding server to exploit', details='Hyprx - CLI toolkit for Minecraft')
                return
            except Exception as e:
                time.sleep(3)
        _ready = False

    threading.Thread(target=_connect, daemon=True).start()
    return True

def update_rpc(state='Exploiting', details='Modular CLI toolkit for Minecraft'):
    global RPC, _ready
    if not RPC or not _ready:
        return
    try:
        RPC.update(
            state=state,
            details=details,
            start=START_TIME,
        )
    except Exception as e:
        pass

def stop_rpc():
    global RPC, _ready
    if RPC:
        try:
            RPC.close()
        except:
            pass
        RPC = None
        _ready = False