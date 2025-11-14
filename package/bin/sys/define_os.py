from .pyoslibs import sys_os, environ




IS_ANDROID = 'ANDROID_HOME' in environ
IS_WINDOWS = sys_os == 'win32'
IS_LINUX = sys_os == 'linux'
IS_MACOS = sys_os == 'darwin'




if not any([IS_ANDROID, IS_WINDOWS, IS_LINUX, IS_MACOS]):
    raise OSError(f'pyos not supported ({sys_os})')