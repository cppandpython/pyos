from .....sys.tool import to_gb
from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    TotalPhysicalMemory 
FROM Win32_ComputerSystem
'''


def ram():
    wmi = wmi_connect()

    try:
        return to_gb(getattr(wmi.ExecQuery(QUERY)[0], 'TotalPhysicalMemory', None))
    except Exception:
        return None