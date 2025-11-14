from .....sys.pyoslibs import capi


def hibernate():
    try:
        capi.windll.powrprof.SetSuspendState(1, 0, 0) 
        return True
    except Exception:
        return False