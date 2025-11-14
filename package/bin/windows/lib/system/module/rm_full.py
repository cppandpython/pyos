from .....sys.tool import to_path
from .....sys.error import path_not_exist
from .....sys.pyoslibs import exists, isfile

from .....module.shell import shell


@to_path()
def rm_full(path, /):
    path_not_exist(path)

    shell(f'del /F /Q "{path}"' if isfile(path) else f'rmdir /S /Q "{path}"', system=True) 

    return not exists(path)