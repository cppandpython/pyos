from .....sys.pyoslibs import capi


def sleep():
    try:
        capi.windll.powrprof.SetSuspendState(0, 0, 0)
        return True
    except Exception:
        return False