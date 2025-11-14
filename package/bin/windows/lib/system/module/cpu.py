from ....sys.value import CPU_ARCHITECTURE, AVAILABILITY_STATUS
from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    Name, 
    Description, 
    Manufacturer,
    Version,
    DeviceID,
    Architecture,
    NumberOfCores, 
    NumberOfLogicalProcessors, 
    MaxClockSpeed, 
    VirtualizationFirmwareEnabled, 
    VMMonitorModeExtensions,
    Availability
FROM Win32_Processor
'''


def cpu():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'manufacturer': getattr(n, 'Manufacturer', None),
            'version': getattr(n, 'Version', None),
            'id': getattr(n, 'DeviceID', None),
            'architecture': CPU_ARCHITECTURE.get(getattr(n, 'Architecture', None)),
            'core': getattr(n, 'NumberOfCores', None),
            'stream': getattr(n, 'NumberOfLogicalProcessors', None),
            'mhz': getattr(n, 'MaxClockSpeed', None),
            'virtualization': getattr(n, 'VirtualizationFirmwareEnabled', False) and getattr(n, 'VMMonitorModeExtensions', False),
            'status': AVAILABILITY_STATUS.get(getattr(n, 'Availability', None))
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None