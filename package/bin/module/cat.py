from ..sys.tool import to_path
from ..sys.error import path_not_exist

from ..module.decode_bytes import decode_bytes


@to_path(generator=True)
def cat(path, /, encoding=None):
    path_not_exist(path, file=True)

    with open(path, 'rb') as f:
        return decode_bytes(f.read(), encoding)