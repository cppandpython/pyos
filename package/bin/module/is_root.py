from ..sys.pyoslibs import getuid


def is_root():
    try:
        return getuid() == 0
    except Exception:
        return None