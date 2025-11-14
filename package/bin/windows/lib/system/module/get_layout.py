from ....sys.value import KEYBOARD_LAYOUT
from ....sys.win32libs import win32api


def get_layout():
    try:
        return KEYBOARD_LAYOUT.get(win32api.GetKeyboardLayoutName())
    except Exception:
        return None