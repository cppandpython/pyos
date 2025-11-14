from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    Name,
    InitialSize,
    MaximumSize
FROM Win32_PageFileSetting
'''


def swap():
    wmi = wmi_connect()

    try: 
        return [{
            'name': getattr(n, 'Name', None),
            'mb_min': getattr(n, 'InitialSize', None),
            'mb_max': getattr(n, 'MaximumSize', None)
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None