from plugins.discord_rpc import set_idle, AUTO_IDLE, AUTO_IDLE_TIME, IDLE, LAST_ACTIVITY
import time

def idle():
    global IDLE, LAST_ACTIVITY

    if IDLE:
        IDLE = False
        LAST_ACTIVITY = time.time()
        print("  RPC Status: Active (manual toggle)")
    else:
        print("  RPC Status: Active")
        if AUTO_IDLE:
            remaining = AUTO_IDLE_TIME - int(time.time() - LAST_ACTIVITY)
            if remaining <= 0:
                remaining = 0
            print(f"  Time until auto-idle: {remaining}s")
            if remaining == 0:
                print("  Idle now...")
                set_idle()