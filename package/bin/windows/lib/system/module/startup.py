from ....sys.tool import wmi_connect

from ....lib.tool.module.startup import Startup 


QUERY = '''
SELECT 
    Name, 
    Description, 
    User, 
    Command, 
    Location 
FROM Win32_StartupCommand
'''


def startup():
    wmi = wmi_connect()

    startup_result = []

    try:
        for n in wmi.ExecQuery(QUERY):
            name = getattr(n, 'Name', None)
            user = getattr(n, 'User', None)
            mode = None
            status = None

            if isinstance(name, str):
                startup_name = Startup(name)

                mode = startup_name.mode()
                status = startup_name.status()

            startup_result.append({
                'name': name,
                'description': getattr(n, 'Description', None),
                'user': user.split('\\', 1)[-1] if isinstance(user, str) else None,
                'command': getattr(n, 'Command', None),
                'location': getattr(n, 'Location', None),
                'mode': mode,
                'status':status
            })
        
        return startup_result
    except Exception:
        return None