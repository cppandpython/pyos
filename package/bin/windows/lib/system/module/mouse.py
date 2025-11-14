from ....sys.value import MOUSE_TYPE, MOUSE_INTERFACE
from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    Name, 
    Description, 
    Manufacturer, 
    DeviceID, 
    PNPDeviceID, 
    PointingType, 
    SystemName, 
    HardwareType, 
    DeviceInterface, 
    Status
FROM Win32_PointingDevice
'''


def mouse():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'manufacturer': getattr(n, 'Manufacturer', None),
            'id': getattr(n, 'DeviceID', None),
            'pnp': getattr(n, 'PNPDeviceID', None),
            'device': MOUSE_TYPE.get(getattr(n, 'PointingType', None)),
            'system_name': getattr(n, 'SystemName', None),
            'type': getattr(n, 'HardwareType', None),
            'interface': MOUSE_INTERFACE.get(getattr(n, 'DeviceInterface', None)),
            'status': getattr(n, 'Status', None)
        } for n in wmi.ExecQuery(QUERY)] 
    except Exception:
        return None