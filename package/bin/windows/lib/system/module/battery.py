from ....sys.value import BATTERY_CHEMISTRY, BATTERY_STATUS
from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    Name, 
    Description, 
    EstimatedChargeRemaining, 
    DeviceID, 
    Chemistry, 
    DesignCapacity, 
    DesignVoltage, 
    BatteryStatus
FROM Win32_Battery
'''


def battery():
    wmi = wmi_connect()

    try:
        n = wmi.ExecQuery(QUERY)[0]

        return {
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'charge': getattr(n, 'EstimatedChargeRemaining', None),
            'id': getattr(n, 'DeviceID', None),
            'type': BATTERY_CHEMISTRY.get(getattr(n, 'Chemistry', None)),
            'capacity': getattr(n, 'DesignCapacity', None),
            'voltage': getattr(n, 'DesignVoltage', None),
            'status': BATTERY_STATUS.get(getattr(n, 'BatteryStatus', None))
        } 
    except Exception:
        return None