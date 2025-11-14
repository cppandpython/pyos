from .....sys.pyoslibs import capi


def is_admin():
    try:
        return capi.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return None