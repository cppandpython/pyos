from ....sys.value import CLIPBOARD_FORMAT
from .....sys.error import invalid_type, failed_connect
from ....sys.win32libs import win32clipboard


class Clipboard:
    __slots__ = tuple()


    def __init__(self): ...


    def __enter__(self):
        return self
       

    def __exit__(self, exc_type, exc_value, traceback): ...

    
    @staticmethod
    def _init_clipboard(func):


        def wrapper(*args, **kwargs):
            try:
                win32clipboard.OpenClipboard()
            except Exception:
                failed_connect('clipboard')
            
            try:
                func_result = func(*args, **kwargs)
            except Exception: 
                func_result = None
            finally:
                win32clipboard.CloseClipboard()

            return func_result


        return wrapper


    @staticmethod
    @_init_clipboard
    def get():
        return win32clipboard.GetClipboardData()
    

    @staticmethod
    @_init_clipboard
    def copy(data):
        invalid_type('data', data, {'str'})

        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(data)
        
        return True
    

    @staticmethod
    @_init_clipboard
    def get_format():
        return CLIPBOARD_FORMAT.get(win32clipboard.EnumClipboardFormats(0))


    @staticmethod
    @_init_clipboard
    def clear():
        win32clipboard.EmptyClipboard()

        return True