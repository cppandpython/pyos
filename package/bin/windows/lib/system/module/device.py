from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    Name,
    Description, 
    Manufacturer, 
    DeviceID, 
    PNPClass, 
    Service,
    Status 
FROM Win32_PnPEntity
'''


def device():
    wmi = wmi_connect()

    try:  
        return [{
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'manufacturer': getattr(n, 'Manufacturer', None),
            'id': getattr(n, 'DeviceID', None),
            'type': getattr(n, 'PNPClass', None),
            'service': getattr(n, 'Service', None),
            'status': getattr(n, 'Status', None)
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None