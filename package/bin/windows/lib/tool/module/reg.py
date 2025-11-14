from ....sys.value import REG_ROOT_KEY, REG_TYPE
from .....sys.error import invalid_type, invalid_value, name_not_exist, key_not_exist, failed_connect
from .....sys.pyoslibs import split_path, join_path
from ....sys.win32libs import winreg


class Reg:
    __slots__ = (
        'full_key', 
        'root_key', 
        'key', 
        '_reg_root_key', 
        '_reg_handle'
    )


    TYPE_NONE = winreg.REG_NONE
    TYPE_SZ = winreg.REG_SZ
    TYPE_EXPAND_SZ = winreg.REG_EXPAND_SZ
    TYPE_BINARY = winreg.REG_BINARY
    TYPE_DWORD = winreg.REG_DWORD
    TYPE_DWORD_BIG_ENDIAN = winreg.REG_DWORD_BIG_ENDIAN
    TYPE_LINK = winreg.REG_LINK
    TYPE_MULTI_SZ = winreg.REG_MULTI_SZ
    TYPE_RESOURCE_LIST = winreg.REG_RESOURCE_LIST
    TYPE_FULL_RESOURCE_DESCRIPTOR = winreg.REG_FULL_RESOURCE_DESCRIPTOR
    TYPE_RESOURCE_REQUIREMENTS_LIST = winreg.REG_RESOURCE_REQUIREMENTS_LIST
    TYPE_QWORD = winreg.REG_QWORD


    def __init__(self, key):   
        self.full_key, self.root_key, self.key, self._reg_root_key = Reg._init_key(key)     
        
        self._reg_handle = None


    def __enter__(self):
        if not Reg.exists(self.full_key): 
            key_not_exist(self.full_key, not self.create_key())

        if not self._reg_handle:
            try:
                self._reg_handle = winreg.OpenKey(self._reg_root_key, self.key, access=winreg.KEY_ALL_ACCESS)
            except Exception:
                failed_connect('reg')

        return self
       

    def __exit__(self, exc_type, exc_value, traceback):
        if self._reg_handle:
            winreg.CloseKey(self._reg_handle)
            self._reg_handle = None

    
    def __bool__(self):
        return self.exists(self.full_key)
    

    def __eq__(self, other):
        invalid_type('other', other, {'reg'})

        return self.full_key == other.full_key
    

    def __ne__(self, other):
        return not self.__eq__(other)


    @staticmethod
    def _init_key(key):
        invalid_type('key', key, {'str'})

        try:
            root_key, key = key.lstrip('\\').split('\\', 1) 
        except Exception:
            invalid_value('key', key, True, 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion')

        root_key = root_key.upper()
        reg_root_key = REG_ROOT_KEY.get(root_key)
        full_key = join_path(root_key, key)

        key_not_exist(root_key, reg_root_key is None)

        return (
            full_key,
            root_key,
            key,
            reg_root_key
        )


    @staticmethod
    def exists(key, value=False):
        invalid_type('value', value, {'bool'})

        _, _, key, reg_root_key = Reg._init_key(key)

        try:
            if value:
                key, name = split_path(key)

            with winreg.OpenKey(reg_root_key, key) as k: 
                if value:
                    winreg.QueryValueEx(k, name)

                return True
        except Exception:
            return False

        
    def get_enum(self, key=None, value=False):
        invalid_type('key', key, {'nonetype', 'str'})
        invalid_type('value', value, {'bool'})

        flag_subkey = False

        if (key is None) and (self._reg_handle is not None):
            key = self._reg_handle
        else:
            enum_key = self.key if key is None else join_path(self.key, key.lstrip('\\'))
            reg_key = join_path(self.root_key, enum_key)

            key_not_exist(reg_key, not self.exists(reg_key))
            
            try:
                key = winreg.OpenKey(self._reg_root_key, enum_key)
            except Exception:
                return None
            
            flag_subkey = True
     
        reg_enum = []
        reg_index = 0

        while True:
            try:
                enum_key = (winreg.EnumKey if not value else winreg.EnumValue)(key, reg_index) 
            except Exception:
                break
            
            reg_enum.append({
                    'key': join_path('\\', enum_key)
                } if not value else {
                    'name': enum_key[0],
                    'value': enum_key[1],
                    'value_type': REG_TYPE.get(enum_key[2])
                }
            )

            reg_index += 1
        
        if flag_subkey:
            winreg.CloseKey(key)

        return reg_enum if reg_enum else None


    def create_key(self, name=None):
        invalid_type('name', name, {'nonetype', 'str'})

        name = self.key if name is None else join_path(self.key, name.lstrip('\\'))
    
        try:
            with winreg.CreateKey(self._reg_root_key, name): 
                return True
        except Exception:
            return False
            

    def delete_key(self, name=None):
        invalid_type('name', name, {'nonetype', 'str'})

        name = self.key if name is None else join_path(self.key, name.lstrip('\\'))

        try:
            with winreg.DeleteKey(self._reg_root_key, name): 
                return True
        except FileNotFoundError:
            key_not_exist(self.full_key, True)
        except Exception:
            return False
            

    def get_key(self):
        return self.get_enum(value=False)
                

    def get_value(self, name=None):
        invalid_type('name', name, {'nonetype', 'str'})

        if name is None:
            return self.get_enum(value=True)

        with self:
            try:
                query_result = winreg.QueryValueEx(self._reg_handle, name)
            except FileNotFoundError:
                name_not_exist(name, True)
            except Exception: 
                return None

        return {
            'value': query_result[0],
            'type': REG_TYPE.get(query_result[1])
        }
    

    def set_value(self, name, value, value_type):
        invalid_type('name', name, {'str'})
        invalid_type('value_type', value_type, {'int'})

        set_reg_type = REG_TYPE.get(value_type)

        invalid_value('value_type', value_type, set_reg_type is None, 'TYPE_NONE, TYPE_SZ, TYPE_EXPAND_SZ, TYPE_BINARY, TYPE_DWORD, TYPE_DWORD_BIG_ENDIAN, TYPE_LINK, TYPE_MULTI_SZ, TYPE_RESOURCE_LIST, TYPE_FULL_RESOURCE_DESCRIPTOR, TYPE_RESOURCE_REQUIREMENTS_LIST, TYPE_QWORD')
        
        with self:
            try:
                winreg.SetValueEx(self._reg_handle, name, 0, value_type, value)
                return True
            except ValueError:
                invalid_value('value', value, True, f'value must match reg type: {set_reg_type}')
            except Exception:
                return False
    

    def delete_value(self, name):
        invalid_type('name', name, {'str'})
        
        with self:
            try:
                winreg.DeleteValue(self._reg_handle, name)
                return True
            except FileNotFoundError:
                name_not_exist(name, True)
            except Exception:
                return False


    def __repr__(self):
        return f'Reg({repr(self.full_key)})'