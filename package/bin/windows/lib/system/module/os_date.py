from ....sys.tool import wmi_connect, wmi_date


QUERY = '''
SELECT 
    InstallDate 
FROM Win32_OperatingSystem
'''


def os_date():
    wmi = wmi_connect()

    try:
        return wmi_date(getattr(wmi.ExecQuery(QUERY)[0], 'InstallDate', None))
    except Exception:
        return None