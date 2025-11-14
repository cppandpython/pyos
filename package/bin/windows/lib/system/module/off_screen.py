from ....sys.win32libs import win32api


def off_screen():
    try:
        win32api.SendMessage(0xFFFF, 0x112, 0xF170, 2)
        return True
    except Exception:
        return False 