from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    SerialNumber 
FROM Win32_OperatingSystem
'''


def product_code():
    wmi = wmi_connect()
    
    try:
        return getattr(wmi.ExecQuery(QUERY)[0], 'SerialNumber', None)
    except Exception:
        return None