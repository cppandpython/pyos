from .....sys._import import _import
from ....sys.value import (
    PATH_STARTUP, 
    PATH_STARTUP_CURRENT_USER,
    REG_KEY_LOCAL_MACHINE_RUN,
    REG_KEY_LOCAL_MACHINE_RUN_STATUS,
    REG_KEY_CURRENT_USER_RUN,
    REG_KEY_CURRENT_USER_RUN_STATUS,
    REG_VALUE_STATUS_ENABLED,
    REG_VALUE_STATUS_DISABLED
)
from .....sys.error import invalid_type, invalid_value, name_not_exist, path_not_exist
from .....sys.pyoslibs import exists, abspath, split_path, join_path, rmfile

from .reg import Reg
from ...system.module.launch import launch
from ...system.module.kill import kill


class Startup:
    __slots__ = (
        'name',
        '_info',
        '_key_status'
    )
    
        
    def __init__(self, name):
        invalid_type('name', name, {'str'})

        invalid_value('name', name, not name, 'name in startup')

        self.name = name

        self._info = self._get_info()
        self._key_status = self._get_key_status()
    

    def __enter__(self):
        return self
       

    def __exit__(self, exc_type, exc_value, traceback): ...


    def __bool__(self):
        return self.exists()
    

    def __eq__(self, other):
        invalid_type('other', other, {'startup'})

        return (self.name == other.name) and (self._info == other._info) and (self._key_status == other._key_status)
         
    
    def __ne__(self, other):
        return not self.__eq__(other)
            

    def _get_info(self):
        startup_info = {
            'type': None,
            'key': None
        }

        if Reg.exists(join_path(REG_KEY_LOCAL_MACHINE_RUN, self.name), value=True):
            startup_info['type'] = 'reg'
            startup_info['key'] = REG_KEY_LOCAL_MACHINE_RUN
        elif Reg.exists(join_path(REG_KEY_CURRENT_USER_RUN, self.name), value=True):
            startup_info['type'] = 'reg'
            startup_info['key'] = REG_KEY_CURRENT_USER_RUN
        else:
            startup_file = join_path(PATH_STARTUP, self.name)

            if exists(startup_file):
                startup_info['type'] = 'file'
                startup_info['key'] = startup_file
            else:
                startup_file_current_user = join_path(PATH_STARTUP_CURRENT_USER, self.name) 

                if exists(startup_file_current_user):
                    startup_info['type'] = 'file'
                    startup_info['key'] = startup_file_current_user

        return startup_info
    

    def _get_key_status(self):
        if self.exists():
            reg_key_status = REG_KEY_LOCAL_MACHINE_RUN_STATUS if self._info['key'] == REG_KEY_LOCAL_MACHINE_RUN else REG_KEY_CURRENT_USER_RUN_STATUS

            if Reg.exists(join_path(reg_key_status, self.name), value=True):
                return reg_key_status
        
        return None
    

    def _set_mode(self, mode):
        invalid_type('mode', mode, {'str'})

        if mode == 'enable':
            new_mode = REG_VALUE_STATUS_ENABLED
        elif mode == 'disable':
            new_mode = REG_VALUE_STATUS_DISABLED
        else:
            invalid_value('mode', mode, True, 'enable, disable')

        if self._key_status is None:
            return False
        
        return Reg(self._key_status).set_value(self.name, new_mode, Reg.TYPE_BINARY)


    @staticmethod
    def get_startup():
        return _import('system.module.startup', from_module=['startup'], spec=__spec__, deep=3)()

    
    def exists(self):
        return self._info['type'] is not None

    
    def create(self, path, current_user=False, mode='enable'):
        invalid_type('current_user', current_user, {'bool'})

        path_not_exist(path, file=True)

        if Reg(REG_KEY_LOCAL_MACHINE_RUN if not current_user else REG_KEY_CURRENT_USER_RUN).set_value(self.name, abspath(path), Reg.TYPE_SZ):
            self._set_mode(mode)
            self._info = self._get_info()
            self._key_status = self._get_key_status()

            return True

        return False


    def delete(self):
        name_not_exist(self.name, not self.exists())

        self.stop()

        is_deleted = False

        if self._info['type'] == 'file':
            rmfile(self._info['key'])
            is_deleted = not exists(self._info['key'])
        else:
            is_deleted = Reg(self._info['key']).delete_value(self.name)
        
        if is_deleted:
            self._info = {
                'type': None,
                'key': None
            }
            self._key_status = None

            return True

        return False
    

    def mode(self):
        if self._key_status is None:
            return None

        reg_mode = Reg(self._key_status).get_value(self.name)

        if reg_mode is None:
            return None
        
        reg_mode = reg_mode['value']

        if reg_mode == REG_VALUE_STATUS_ENABLED:
            return 'enable'
        elif reg_mode == REG_VALUE_STATUS_DISABLED:
            return 'disable'
        
        return None

    
    def enable(self):
        return self._set_mode('enable')
        
        
    def disable(self):
        return self._set_mode('disable')


    def status(self):
        if self._key_status is None:
            return None

        reg_status = Reg(self._key_status).get_value(self.name)

        if reg_status is None:
            return None

        return reg_status['value'] == REG_VALUE_STATUS_ENABLED
    
    
    def start(self):
        if not self.exists():
            return False
        
        if self._info['type'] == 'file':
            path = self._info['key']
        else:
            path = Reg(self._info['key']).get_value(self.name)

            if path is None:
                return False
            
            path = path['value']

        return launch(path)
            
    
    def stop(self):
        if not self.exists():
            return False
        
        if self._info['type'] == 'file':
            name = self._info['key']
        else:
            name = Reg(self._info['key']).get_value(self.name)

            if name is None:
                return False
            
            name = name['value']
            
        return kill(split_path(name)[1])
    

    def __repr__(self):
        return f'Startup({repr(self.name)})' 