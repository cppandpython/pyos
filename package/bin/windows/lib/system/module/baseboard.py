from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    Name, 
    Description, 
    Manufacturer, 
    Product, 
    Version,
    SerialNumber
FROM Win32_BaseBoard
'''


def baseboard():
    wmi = wmi_connect()

    try:
        n = wmi.ExecQuery(QUERY)[0]

        return {
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'manufacturer': getattr(n, 'Manufacturer', None),
            'product': getattr(n, 'Product', None),
            'version': getattr(n, 'Version', None),
            'serialnumber': getattr(n, 'SerialNumber', None)
        } 
    except Exception:
        return None