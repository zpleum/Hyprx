from plugins.discord_rpc import set_idle, AUTO_IDLE, AUTO_IDLE_TIME, IDLE, LAST_ACTIVITY
import time

def idle():
    global IDLE, LAST_ACTIVITY

    if IDLE:
        print(f"  RPC Status: Idle")
    else:
        print(f"  RPC Status: Active")
        if AUTO_IDLE and not IDLE:
            remaining = AUTO_IDLE_TIME - int(time.time() - LAST_ACTIVITY)
            if remaining < 0:
                remaining = 0
            print(f"  Time until auto-idle: {remaining}s")
            print("  Forcing idle now...")
            set_idle()
        elif not AUTO_IDLE:
            pass