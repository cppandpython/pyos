from ....sys.value import MEMORY_FORMFACTOR, MEMORY_TYPE, MEMORY_TYPE_DETAIL
from .....sys.tool import to_mb
from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    Name, 
    BankLabel, 
    Manufacturer,
    Version,
    SerialNumber,
    DeviceLocator,
    FormFactor, 
    MemoryType,
    TypeDetail,
    DataWidth,
    MaxVoltage,
    Capacity, 
    Speed
FROM Win32_PhysicalMemory
'''


def memory():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'Name', None),
            'label': getattr(n, 'BankLabel', None),
            'manufacturer': getattr(n, 'Manufacturer', None),
            'version': getattr(n, 'Version', None),
            'serialnumber': getattr(n, 'SerialNumber', None),
            'location': getattr(n, 'DeviceLocator', None),
            'formfactor': MEMORY_FORMFACTOR.get(getattr(n, 'FormFactor', None)),
            'type': MEMORY_TYPE.get(getattr(n, 'MemoryType', None)),
            'detail': MEMORY_TYPE_DETAIL.get(getattr(n, 'TypeDetail', None)),
            'data_width': getattr(n, 'DataWidth', None),
            'voltage': getattr(n, 'MaxVoltage', None),
            'mb': to_mb(getattr(n, 'Capacity', None)), 
            'mhz': getattr(n, 'Speed', None)
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None