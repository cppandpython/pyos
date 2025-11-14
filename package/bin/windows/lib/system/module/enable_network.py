from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    NetEnabled
FROM Win32_NetworkAdapter 
WHERE NetEnabled = False
'''


def enable_network():
    wmi = wmi_connect()

    enabled = False

    for n in wmi.ExecQuery(QUERY):
        Enable = getattr(n, 'Enable', None)

        if callable(Enable):
            try:
                Enable()
            except Exception:
                continue
            
            enabled = True

    return enabled