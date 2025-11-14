from .....sys.error import invalid_type, invalid_value
from ....sys.win32libs import win32con, win32api

from .....module.shell import shell


def kill(process):
    invalid_type('process', process, {'int', 'str'})

    invalid_value('process', process, not str(process), 'pid, name')

    if isinstance(process, str) and process.isdigit():
        process = int(process)
    
    if isinstance(process, int):
        try:
            win32api.TerminateProcess(win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, process), 0)
            return True
        except Exception:
            return False

    return shell(['taskkill', '/f', '/t', '/im', process], system=True)['status']