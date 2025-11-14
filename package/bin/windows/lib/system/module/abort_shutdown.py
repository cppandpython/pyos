from ....sys.win32libs import win32api


def abort_shutdown():
    try:
        win32api.AbortSystemShutdown(None)
        return True
    except Exception:
        return False 