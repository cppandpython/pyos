from ....sys.value import LOGON
from .....sys.error import invalid_type, invalid_value
from ....sys.win32libs import win32security


def logon(user, password, domain='', logon='batch'):
    invalid_type('user', user, {'str'})
    invalid_type('password', password, {'str'})
    invalid_type('domain', domain, {'str'})
    invalid_type('logon', logon, {'str'})

    logon_type = LOGON.get(logon)

    invalid_value('logon', logon, logon_type is None, 'batch, interactive, service, network, network_cleartext, credentials, unlock')

    try:
        return win32security.LogonUser(
            Username=user,
            Password=password,
            Domain=domain,
            LogonType=logon_type,
            LogonProvider=win32security.LOGON32_PROVIDER_DEFAULT
        )
    except Exception as error:
        raise PermissionError(error)