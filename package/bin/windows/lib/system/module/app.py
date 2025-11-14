from ....sys.value import LOCALE, APP_ASSIGNMENT_TYPE, APP_INSTALL_STATE
from .....sys.tool import to_date, to_int
from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    Name, 
    Description, 
    Vendor,
    Version, 
    InstallDate,
    AssignmentType,
    PackageName,
    Language, 
    InstallSource,
    InstallState
FROM Win32_Product
'''


def app():
    wmi = wmi_connect()
    
    app_result = []

    try:
        for n in wmi.ExecQuery(QUERY):
            app_result.append({
                'name': getattr(n, 'Name', None),
                'description': getattr(n, 'Description', None),
                'vendor': getattr(n, 'Vendor', None),
                'version': getattr(n, 'Version', None),
                'date': to_date(getattr(n, 'InstallDate', None), format_date='%d.%m.%Y', format_parse='%Y%m%d', format_time=None)[0], 
                'installation': APP_ASSIGNMENT_TYPE.get(getattr(n, 'AssignmentType', None)),
                'package': getattr(n, 'PackageName', None),
                'lang': LOCALE.get(to_int(getattr(n, 'Language', None))),
                'file': getattr(n, 'InstallSource', None),
                'status': APP_INSTALL_STATE.get(getattr(n, 'InstallState', None))
            })

        return app_result
    except Exception:
        return None  