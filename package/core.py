from .bin.sys.define_os import (
    IS_ANDROID as _IS_ANDROID, 
    IS_WINDOWS as _IS_WINDOWS, 
    IS_LINUX as _IS_LINUX, 
    IS_MACOS as _IS_MACOS
)
from .bin.sys.pyoslibs import _argv
from .bin.sys.check_right import _check_right




if _IS_ANDROID:


    from .bin.android.api import *
    from .bin.android.sys.argv import _executor_argv


elif _IS_WINDOWS:


    from .bin.windows.api import *
    from .bin.windows.sys.argv import _executor_argv


elif _IS_LINUX:


    from .bin.linux.api import *
    from .bin.linux.sys.argv import _executor_argv


elif _IS_MACOS:


    from .bin.macos.api import *
    from .bin.macos.sys.argv import _executor_argv




_check_right()




if len(_argv) > 2:
    _executor_argv(_argv[1:])