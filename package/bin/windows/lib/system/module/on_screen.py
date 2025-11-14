from .....sys.pyoslibs import sleep
from ....sys.win32libs import win32con, win32api


def on_screen():
    try:
        win32api.keybd_event(0x01, 0, win32con.KEYEVENTF_SCANCODE, 0) 
        sleep(0.1)  
        win32api.keybd_event(0x01, 0, win32con.KEYEVENTF_KEYUP, 0) 
        return True
    except Exception:
        return False