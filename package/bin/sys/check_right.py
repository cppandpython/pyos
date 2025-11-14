from .define_os import IS_WINDOWS
from .pyoslibs import _warn




if IS_WINDOWS:
    from ..windows.lib.system.module.is_admin import is_admin as right
    text = 'some functions require administrator rights to perform'
else:
    from ..module.is_root import is_root as right
    text = 'some functions require root rights to perform'




def _check_right():
    if right() == False:
        _warn(text, category=UserWarning)