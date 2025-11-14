from ..sys.define_os import IS_WINDOWS
from ..sys.value import PATH_SEP
from ..sys.error import invalid_type


def transform_path(path):
    invalid_type('path', path, {'str'})

    return path.replace('/' if IS_WINDOWS else '\\', PATH_SEP)