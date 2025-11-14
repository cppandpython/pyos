from ....sys.value import ACCOUNT_TYPE
from ....sys.tool import wmi_connect


QUERY = '''
SELECT 
    Name, 
    Description, 
    PasswordRequired, 
    SID, 
    Domain, 
    Lockout, 
    Disabled, 
    AccountType,
    Status 
FROM Win32_UserAccount
'''


def users():
    wmi = wmi_connect()

    try:
        return [{
            'name': getattr(n, 'Name', None),
            'description': getattr(n, 'Description', None),
            'password': getattr(n, 'PasswordRequired', None),
            'sid': getattr(n, 'SID', None),
            'domain': getattr(n, 'Domain', None),
            'lockout': getattr(n, 'Lockout', None),
            'disabled': getattr(n, 'Disabled', None),
            'type': ACCOUNT_TYPE.get(getattr(n, 'AccountType', None)),
            'status': getattr(n, 'Status', None)
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        return None