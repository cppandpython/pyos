from ....sys.value import SOUND_STATUS
from ....sys.tool import wmi_connect


QUERY = '''
SELECT
    Name,
    Description,
    Manufacturer,
    DeviceID,
    PNPDeviceID,
    SystemName,
    StatusInfo
FROM Win32_SoundDevice
'''


def sound():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'manufacturer': getattr(n, 'Manufacturer', None),
            'id': getattr(n, 'DeviceID', None),
            'pnp': getattr(n, 'PNPDeviceID', None),
            'system_name': getattr(n, 'SystemName', None),
            'status': SOUND_STATUS.get(getattr(n, 'StatusInfo', None))
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None