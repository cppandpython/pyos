from .....sys.value import PATH_PYTHON
from .....sys.error import invalid_type, path_not_exist
from .....sys.pyoslibs import _argv, join_command
from ....sys.win32libs import win32api

from .is_admin import is_admin


def get_admin(file=PATH_PYTHON, args=None, window=True):
    invalid_type('args', args, {'nonetype', 'str', 'list', 'tuple'})
    invalid_type('window', window, {'bool'})
    
    path_not_exist(file, file=True)    

    current_file = _argv[0]

    if (args is None) and (file == PATH_PYTHON):
        args = current_file
    else:
        if isinstance(args, (list, tuple)):
            args = join_command(args)

    current = args == current_file

    if current and is_admin():
        return True
    
    try:
        code_runas = win32api.ShellExecute(
            None, 
            'runas', 
            file, 
            args, 
            None, 
            int(window)
        )
    except Exception:
        code_runas = -1

    get_admin_result = {
        'file': file,
        'args': args,
        'window': window,
        'status': False
    }

    if code_runas > 32:
        if current:
            exit(0)

        get_admin_result['status'] = True

    return False if current else get_admin_result