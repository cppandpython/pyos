from ....sys.value import FILE_ATTRIBUTE_HIDDEN
from .....sys.tool import to_path
from .....sys.error import format_error, path_not_exist
from ....sys.win32libs import win32api


@to_path()
def unhide(path, /):
    path_not_exist(path)

    unhidden = False

    current_attribute = win32api.GetFileAttributes(path)

    if current_attribute == -1:
        return unhidden
    
    if current_attribute & FILE_ATTRIBUTE_HIDDEN:
        win32api.SetFileAttributes(path, current_attribute & ~FILE_ATTRIBUTE_HIDDEN)

        if not (win32api.GetFileAttributes(path) & FILE_ATTRIBUTE_HIDDEN):
            unhidden = True
    else:
        unhidden = True

    return unhidden