from .....sys.tool import to_mb
from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    TotalVirtualMemorySize 
FROM Win32_OperatingSystem
'''


def virtual_memory():
    wmi = wmi_connect()

    try:
        return to_mb(getattr(wmi.ExecQuery(QUERY)[0], 'TotalVirtualMemorySize', None))
    except Exception:
        return None