from ....sys.value import AVAILABILITY_STATUS
from .....sys.tool import to_gb
from ....sys.tool import wmi_connect, wmi_date


QUERY = '''
SELECT 
    Name,
    Description,
    NetEnabled,
    Manufacturer,
    TimeOfLastReset,
    DeviceID,
    PNPDeviceID,
    ServiceName,
    NetConnectionID,
    MACAddress,
    Speed,
    PhysicalAdapter,
    Availability
FROM Win32_NetworkAdapter
'''


def adapter():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'enabled_network': getattr(n, 'NetEnabled', None),
            'manufacturer': getattr(n, 'Manufacturer', None),
            'date': wmi_date(getattr(n, 'TimeOfLastReset', None)),
            'id': getattr(n, 'DeviceID', None),
            'pnp': getattr(n, 'PNPDeviceID', None),
            'service': getattr(n, 'ServiceName', None),
            'type': getattr(n, 'NetConnectionID', None),
            'mac': getattr(n, 'MACAddress', None),
            'gb_speed': to_gb(getattr(n, 'Speed', None)),
            'physical': getattr(n, 'PhysicalAdapter', None),
            'status': AVAILABILITY_STATUS.get(getattr(n, 'Availability', None))
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None