import plugins.discord_rpc as rpc
import time

def idle():
    if rpc.IDLE:
        rpc.activity() 
        status_text = "[ ACTIVE ]"
        msg = "Status has been woken up from Idle."
    else:
        rpc.set_idle()
        status_text = "[ IDLE ]"
        msg = "Status has been synchronized to Discord."
    
    print(f"  RPC Configuration:")
    print(f"    Auto-Idle : {'[ ENABLED ]' if rpc.AUTO_IDLE else '[ DISABLED ]'}")
    print(f"    Timeout   : {rpc.AUTO_IDLE_TIME}s")
    print()
    
    print(f"  Current Status: {status_text}")
    print(f"  Message: {msg}")