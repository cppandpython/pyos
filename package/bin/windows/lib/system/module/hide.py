from ....sys.value import FILE_ATTRIBUTE_HIDDEN
from .....sys.tool import to_path
from .....sys.error import path_not_exist
from ....sys.win32libs import win32api


@to_path()
def hide(path, /):
    path_not_exist(path)

    hidden = False

    current_attribute = win32api.GetFileAttributes(path)

    if current_attribute == -1:
        return hidden

    if not (current_attribute & FILE_ATTRIBUTE_HIDDEN):
        win32api.SetFileAttributes(path, current_attribute | FILE_ATTRIBUTE_HIDDEN)

        if win32api.GetFileAttributes(path) & FILE_ATTRIBUTE_HIDDEN:
            hidden = True
    else:
        hidden = True

    return hidden