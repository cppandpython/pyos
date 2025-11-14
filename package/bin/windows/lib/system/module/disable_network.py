from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    NetEnabled
FROM Win32_NetworkAdapter 
WHERE NetEnabled = True
'''


def disable_network():
    wmi = wmi_connect()

    disabled = False

    for n in wmi.ExecQuery(QUERY):
        Disable = getattr(n, 'Disable', None)
        
        if callable(Disable):
            try:
                Disable()
            except Exception:
                continue
            
            disabled = True

    return disabled 