from ...sys.error import failed_connect
from ...sys.pyoslibs import datetime
from ..sys.win32libs import win32connect


def wmi_connect():
    try:
        return win32connect('WbemScripting.SWbemLocator').ConnectServer('.', 'root\\cimv2')
    except Exception:
        failed_connect('wmi')
    
 
def wmi_date(date):
    try:
        if date is not None:
            return datetime.strptime(date.split('.', 1)[0], '%Y%m%d%H%M%S').strftime('%d.%m.%Y %H:%M:%S').split()
    except Exception: ...
    return (None, None)