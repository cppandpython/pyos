from ..sys.define_os import IS_WINDOWS

from ..module.shell import shell 


clear = lambda: shell(['cls' if IS_WINDOWS else 'clear'], output=False, system=True)['status']