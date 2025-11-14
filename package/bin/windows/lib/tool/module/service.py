from ....sys.value import (
    SERVICE_TYPE, 
    SERVICE_ACCEPT_CONTROL,
    SERVICE_RUNNING,
    SERVICE_STATUS,
    SERVICE_CHECKPOINT,
    SERVICE_MODE_VALUE,
    SERVICE_MODE_NAME
)
from .....sys.error import invalid_type, invalid_value, name_not_exist, path_not_exist
from .....sys.pyoslibs import abspath
from ....sys.win32libs import win32service, win32serviceutil

from ...system.module.service import service


class Service:
    __slots__ = (
        'name',
    )


    def __init__(self, name):
        invalid_type('name', name, {'str'})

        self.name = name


    def __enter__(self):
        return self
       

    def __exit__(self, exc_type, exc_value, traceback): ...


    def __bool__(self):
        return self.exists()
    

    def __eq__(self, other):
        invalid_type('other', other, {'service'})

        return self.name == other.name
    

    def __ne__(self, other):
        return not self.__eq__(other)


    def _set_mode(self, mode):
        invalid_type('mode', mode, {'str'})

        start_mode = SERVICE_MODE_NAME.get(mode)
        
        invalid_value('mode', mode, start_mode is None, 'enable, manually, disable')

        if self.exists():
            try:
                win32serviceutil.ChangeServiceConfig(self.name, self.name, startType=start_mode)
                return True
            except Exception: ...

        return False
        

    @staticmethod
    def get_service():
        return service()
    

    def info(self, _mode=False):
        invalid_type('_mode', _mode, {'bool'})

        name_not_exist(self.name, not self.exists())

        service_info = {
            'name': self.name,
            'description': None,
            'user': None,
            'command': None,
            'type': None,
            'accept_control': None,
            'check_point': None,
            'dependent': None,
            'mode': None,
            'status': None,
            'exit_code': None
        }
        
        sc_handle = None
        service_handle = None

        config = [None, None]
        status = [None]

        try:
            sc_handle = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_CONNECT)
            service_handle = win32service.OpenService(sc_handle, self.name, win32service.SERVICE_QUERY_CONFIG)

            config = win32service.QueryServiceConfig(service_handle)
        except Exception: ...
        finally:
            if service_handle:
                win32service.CloseServiceHandle(service_handle)

            if sc_handle:
                win32service.CloseServiceHandle(sc_handle)
            
        if _mode:
            return SERVICE_MODE_VALUE.get(config[1])

        try:
            status = win32serviceutil.QueryServiceStatus(self.name)
        except Exception: ...
        
        if len(config) == 9:
            service_info['description'] = config[8]
            service_info['user'] = config[7]
            service_info['command'] = config[3]
            service_info['dependent'] = config[6]
            service_info['mode'] = SERVICE_MODE_VALUE.get(config[1])

        if len(status) == 7:
            service_info['type'] = SERVICE_TYPE.get(status[0])
            service_info['accept_control'] = SERVICE_ACCEPT_CONTROL.get(status[2])
            service_info['check_point'] = SERVICE_CHECKPOINT.get(status[5])
            service_info['status'] = SERVICE_STATUS.get(status[1])
            service_info['exit_code'] = status[3]

        return service_info


    def exists(self):
        try:
            win32serviceutil.QueryServiceStatus(self.name)
            return True
        except Exception:
            return False


    def create(self, display_name, description, path, args='', user=None, password=None, mode='enable'):
        invalid_type('display_name', display_name, {'str'})
        invalid_type('description', description, {'str'})
        invalid_type('args', args, {'str'})
        invalid_type('user', user, {'nonetype', 'str'})
        invalid_type('password', password, {'nonetype', 'str'})
        invalid_type('mode', mode, {'str'})

        path_not_exist(path, file=True)

        start_mode = SERVICE_MODE_NAME.get(mode)

        invalid_value('mode', mode, start_mode is None, 'enable, manually, disable')

        try:
            (win32serviceutil.ChangeServiceConfig if self.exists() else win32serviceutil.InstallService)(
                self.name, 
                serviceName=self.name, 
                displayName=display_name,
                description=description,
                exeName=abspath(path),
                exeArgs=args,
                userName=user,
                password=password,
                startType=start_mode
            )
        except Exception: ...

        return self.exists()
    

    def delete(self):
        name_not_exist(self.name, not self.exists())

        self.stop()
    
        try:
            win32serviceutil.RemoveService(self.name)
            return True
        except Exception: 
            return False
        
    
    def mode(self):
        return self.info(_mode=True)
        

    def enable(self):
        return self._set_mode('enable')


    def manually(self):
        return self._set_mode('manually')


    def disable(self):
        return self._set_mode('disable')
    

    def status(self):
        try: 
            return win32serviceutil.QueryServiceStatus(self.name)[1] == SERVICE_RUNNING
        except Exception:
            return False

    
    def start(self):
        if not self.status():
            try:
                win32serviceutil.StartService(self.name)
            except Exception: ...
        
        return self.status()
    

    def restart(self):
        if self.exists():
            try:
                win32serviceutil.RestartService(self.name)
                return True
            except Exception: ...
        
        return False

    
    def stop(self):
        if self.status():
            try:
                win32serviceutil.StopService(self.name)
            except Exception: ...
        
        return not self.status()
    

    def __repr__(self):
        return f'Service({repr(self.name)})'