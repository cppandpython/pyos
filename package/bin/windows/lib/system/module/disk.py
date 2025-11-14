from ....sys.value import DISK_ACCESS
from .....sys.tool import to_gb
from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    VolumeName, 
    Description, 
    DeviceID, 
    FileSystem, 
    Size, 
    FreeSpace,
    VolumeSerialNumber,
    Access
FROM Win32_LogicalDisk
'''


def disk():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'VolumeName', None),
            'description': getattr(n, 'Description', None),
            'disk': getattr(n, 'DeviceID', None),
            'filesystem': getattr(n, 'FileSystem', None),
            'gb': to_gb(getattr(n, 'Size', None)),
            'gb_free': to_gb(getattr(n, 'FreeSpace', None)),
            'serialnumber': getattr(n, 'VolumeSerialNumber', None),
            'access': DISK_ACCESS.get(getattr(n, 'Access', None))
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None