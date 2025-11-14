from .....sys.tool import to_path
from .....sys.error import invalid_type, path_not_exist
from ....sys.win32libs import startfile


@to_path()
def launch(path, /, args='', window=True):
    path_not_exist(path)

    invalid_type('args', args, {'str'})
    invalid_type('window', window, {'bool'})

    try:
        startfile(
            path, 
            arguments=args, 
            show_cmd=int(window)
        )
        return True
    except Exception: 
        return False