from .....sys.tool import to_mb
from ....sys.tool import wmi_connect, wmi_date


QUERY = '''
SELECT 
    Name, 
    Description, 
    CreationDate, 
    ProcessId, 
    Priority, 
    ThreadCount, 
    WorkingSetSize, 
    CommandLine 
FROM Win32_Process
'''


def ps():
    wmi = wmi_connect()

    ps_result = []

    try:
        for n in wmi.ExecQuery(QUERY):
            GetOwner = getattr(n, 'GetOwner', None)

            if callable(GetOwner):
                try:
                    _, user = GetOwner()
                except Exception: 
                    user = None

            ps_result.append({
                'name': getattr(n, 'Name', None),
                'description': getattr(n, 'Description', None),
                'date': wmi_date(getattr(n, 'CreationDate', None)),
                'user': user,
                'pid': getattr(n, 'ProcessId', None),
                'priority': getattr(n, 'Priority', None),
                'thread': getattr(n, 'ThreadCount', None),
                'mb': to_mb(getattr(n, 'WorkingSetSize', None)),
                'command': getattr(n, 'CommandLine', None)   
            })
    except Exception:
        return None