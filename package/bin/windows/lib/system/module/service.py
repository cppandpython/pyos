from ....sys.tool import wmi_connect


QUERY = '''
SELECT
    Name, 
    Description, 
    DisplayName, 
    SystemName, 
    StartName, 
    ServiceType, 
    StartMode, 
    DesktopInteract, 
    PathName, 
    ProcessId, 
    Started, 
    ErrorControl, 
    State 
FROM Win32_Service
'''


def service():
    wmi = wmi_connect()

    try: 
        return [{
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'display_name': getattr(n, 'DisplayName', None),
            'system_name': getattr(n, 'SystemName', None),
            'user': getattr(n, 'StartName', None),
            'type': getattr(n, 'ServiceType', None),
            'mode': getattr(n, 'StartMode', None),
            'desktop_interact': getattr(n, 'DesktopInteract', None),
            'path': getattr(n, 'PathName', None),
            'pid': getattr(n, 'ProcessId', None),
            'started': getattr(n, 'Started', None),
            'error': getattr(n, 'ErrorControl', None),
            'status': getattr(n, 'State', None)
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None