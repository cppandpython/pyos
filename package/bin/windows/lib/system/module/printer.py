from ....sys.value import PRINTER_ATTRIBUTES, PRINTER_STATUS
from ....sys.tool import wmi_connect


QUERY = '''
SELECT
    Name, 
    Default, 
    DriverName, 
    DeviceID, 
    Priority, 
    PrintProcessor, 
    PrintJobDataType, 
    Attributes, 
    CapabilityDescriptions, 
    EnableDevQueryPrint, 
    Queued, 
    Shared, 
    Network, 
    PaperSizesSupported, 
    PrinterPaperNames, 
    VerticalResolution, 
    HorizontalResolution, 
    PrinterStatus, 
    Status 
FROM Win32_Printer
'''


def printer():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'Name', None),
            'default': getattr(n, 'Default', None),
            'driver': getattr(n, 'DriverName', None),
            'id': getattr(n, 'DeviceID', None),
            'priority': getattr(n, 'Priority', None),
            'service': getattr(n, 'PrintProcessor', None),
            'type': getattr(n, 'PrintJobDataType', None),
            'attribute': PRINTER_ATTRIBUTES.get(getattr(n, 'Attributes', None)),
            'capability': getattr(n, 'CapabilityDescriptions', None),
            'query': getattr(n, 'EnableDevQueryPrint', None),
            'queued': getattr(n, 'Queued', None),
            'shared': getattr(n, 'Shared', None),
            'network': getattr(n, 'Network', None),
            'paper_size': getattr(n, 'PaperSizesSupported', None),
            'paper': getattr(n, 'PrinterPaperNames', None),
            'resolution': f'{getattr(n, "VerticalResolution", None)}x{getattr(n, "HorizontalResolution", None)}',
            'printer_status': PRINTER_STATUS.get(getattr(n, 'PrinterStatus', None)),
            'status': getattr(n, 'Status', None)
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None