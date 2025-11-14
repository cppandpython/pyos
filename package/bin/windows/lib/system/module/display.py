from ....sys.value import AVAILABILITY_STATUS
from ....sys.tool import wmi_connect


QUERY = '''
SELECT
    Name,
    Description,
    MonitorManufacturer,
    DeviceID,
    PNPDeviceID,
    SystemName,
    MonitorType,
    PixelsPerXLogicalInch,
    PixelsPerYLogicalInch,
    Availability
FROM Win32_DesktopMonitor
'''


def display():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'manufacturer': getattr(n, 'MonitorManufacturer', None),
            'id': getattr(n, 'DeviceID', None),
            'pnp': getattr(n, 'PNPDeviceID', None),
            'system_name': getattr(n, 'SystemName', None),
            'type': getattr(n, 'MonitorType', None),
            'dpi_x': getattr(n, 'PixelsPerXLogicalInch', None),
            'dpi_y': getattr(n, 'PixelsPerYLogicalInch', None),
            'status': AVAILABILITY_STATUS.get(getattr(n, 'Availability', None))
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None