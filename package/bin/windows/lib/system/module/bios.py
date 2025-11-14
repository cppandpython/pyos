from ....sys.tool import wmi_connect, wmi_date


QUERY = '''
SELECT 
    Name, 
    Description, 
    Manufacturer, 
    ReleaseDate, 
    SMBIOSBIOSVersion, 
    SerialNumber 
FROM Win32_BIOS
'''


def bios():
    wmi = wmi_connect()
    
    try:
        n = wmi.ExecQuery(QUERY)[0]

        return {
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'manufacturer': getattr(n, 'Manufacturer', None),
            'date': wmi_date(getattr(n, 'ReleaseDate', None)),
            'version': getattr(n, 'SMBIOSBIOSVersion', None),
            'serialnumber': getattr(n, 'SerialNumber', None)
        }
    except Exception:
        return None