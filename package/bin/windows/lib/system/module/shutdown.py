from .....sys.error import invalid_type
from ....sys.win32libs import win32api


def shutdown(msg=None, timeout=0):
    invalid_type('msg', msg, {'nonetype', 'str'})
    invalid_type('timeout', timeout, {'int'})

    try:
        win32api.InitiateSystemShutdown(None, msg, timeout, True, False)
        return True
    except Exception:
        return False