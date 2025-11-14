from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    Name, 
    Description, 
    BootDirectory
FROM Win32_BootConfiguration
'''

QUERY_MODE = '''
SELECT 
    BootupState 
FROM Win32_ComputerSystem
'''


def boot():
    wmi = wmi_connect()

    try:
        n = wmi.ExecQuery(QUERY)[0]

        return {
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'dir': getattr(n, 'BootDirectory', None),
            'mode': getattr(wmi.ExecQuery(QUERY_MODE)[0], 'BootupState', None)
        } 
    except Exception:
        return None