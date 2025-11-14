from ....sys.value import EVENTLOG_TYPE, EVENTLOG_CATEGORY
from .....sys.tool import to_date
from ....sys.win32libs import win32evtlog


QUERY = [
    'HardwareEvents',  
    'System',         
    'Security',       
    'Application',   
    'Setup',        
    'ForwardedEvents', 
    'TaskScheduler',   
    'Windows PowerShell',
    'Microsoft-Windows-WER-SystemErrorReporting'
]


def eventlog():
    eventlog_result = {
        'hardware': [],
        'system': [],
        'security': [],
        'app': [],
        'setup': [],
        'forwarded': [],
        'taskscheduler': [],
        'powershell': [],
        'error': []
    }

    for log in QUERY:
        try: 
            handle = win32evtlog.OpenEventLog('localhost' , log)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            
            events = win32evtlog.ReadEventLog(handle, flags, 0)
        except Exception:
            continue
        
        if log == 'HardwareEvents':
            log_name = 'hardware'
        elif log == 'System': 
            log_name = 'system'
        elif log == 'Security': 
            log_name = 'security'
        elif log == 'Application': 
            log_name = 'app'
        elif log == 'Setup': 
            log_name = 'setup'
        elif log == 'ForwardedEvents': 
            log_name = 'forwarded'
        elif log == 'TaskScheduler': 
            log_name = 'taskscheduler'
        elif log == 'Windows PowerShell': 
            log_name = 'powershell'
        elif log == 'Microsoft-Windows-WER-SystemErrorReporting': 
            log_name = 'error'
        else: 
            continue

        for n in events:
            eventlog_result[log_name].append({
                'date': to_date(getattr(n, 'TimeWritten', None)),
                'record': getattr(n, 'RecordNumber', None),
                'id': getattr(n, 'EventID', None),
                'type': EVENTLOG_TYPE.get(getattr(n, 'EventType', None)),
                'category': EVENTLOG_CATEGORY.get(getattr(n, 'EventCategory', None)),
                'source': getattr(n, 'SourceName', None),
                'info': getattr(n, 'StringInserts', None),
                'data': getattr(n, 'Data', None)
            })

    return eventlog_result 