from ....sys.value import USER
from .....sys.pyoslibs import exists, join_path
from ....sys.win32libs import win32api, win32security


def recycle():
    recycle_result = {}

    try:
        sid = str(win32security.LookupAccountName(None, USER)[0]).split(':', 1)[1]
      
        for n in win32api.GetLogicalDriveStrings().split('\000'):
            recycle_path = join_path(n, '$Recycle.Bin', sid)

            if exists(recycle_path):
                recycle_result[n.upper()] = recycle_path

        return recycle_result if recycle_result else None
    except Exception:
        return None