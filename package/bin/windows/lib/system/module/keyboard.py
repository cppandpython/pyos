from ....sys.value import KEYBOARD_LAYOUT
from ....sys.tool import wmi_connect


QUERY = '''
SELECT  
    Name,
    Description,
    DeviceID,
    PNPDeviceID,
    SystemName,
    Layout,
    NumberOfFunctionKeys,
    Status
FROM Win32_Keyboard
'''


def keyboard():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'id': getattr(n, 'DeviceID', None),
            'pnp': getattr(n, 'PNPDeviceID', None),
            'system_name': getattr(n, 'SystemName', None),
            'lang': KEYBOARD_LAYOUT.get(getattr(n, 'Layout', None)),
            'keys': getattr(n, 'NumberOfFunctionKeys', None),
            'status': getattr(n, 'Status', None)
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None