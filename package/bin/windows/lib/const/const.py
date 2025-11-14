from ....sys._import import _import, EmptyModule
from ....sys.define_os import (
    IS_ANDROID, 
    IS_WINDOWS, 
    IS_LINUX, 
    IS_MACOS
)
from ....sys.value import *
from ...sys.value import *
if not isinstance(_import('sys.win32libs', from_module=['win32con'], spec=__spec__, deep=3), EmptyModule):
    from win32con import *