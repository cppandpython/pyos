from ....sys.value import GPU_ARCHITECTURE, GPU_VIDEOMEMORY_TYPE, AVAILABILITY_STATUS
from .....sys.tool import to_gb
from ....sys.tool import wmi_connect, wmi_date


QUERY = '''
SELECT 
    Name, 
    Description, 
    DeviceID, 
    PNPDeviceID, 
    DriverDate, 
    InstalledDisplayDrivers, 
    DriverVersion, 
    VideoArchitecture,
    VideoProcessor,
    VideoMemoryType,
    AdapterRAM, 
    CurrentNumberOfColors, 
    CurrentRefreshRate, 
    CurrentHorizontalResolution, 
    CurrentVerticalResolution, 
    Availability 
FROM Win32_VideoController
'''


def gpu():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'id': getattr(n, 'DeviceID', None),
            'pnp': getattr(n, 'PNPDeviceID', None),
            'date': wmi_date(getattr(n, 'DriverDate', None)),
            'driver': getattr(n, 'InstalledDisplayDrivers', None),
            'version': getattr(n, 'DriverVersion', None),
            'architecture': GPU_ARCHITECTURE.get(getattr(n, 'VideoArchitecture', None)),
            'processor': getattr(n, 'VideoProcessor', None),
            'memory_type': GPU_VIDEOMEMORY_TYPE.get(getattr(n, 'VideoMemoryType', None)),
            'gb': to_gb(getattr(n, 'AdapterRAM', None)),
            'color': getattr(n, 'CurrentNumberOfColors', None),
            'refresh': getattr(n, 'CurrentRefreshRate', None),
            'resolution': f'{getattr(n, 'CurrentHorizontalResolution', None)}x{getattr(n, 'CurrentVerticalResolution', None)}',
            'status': AVAILABILITY_STATUS.get(getattr(n, 'Availability', None))
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None