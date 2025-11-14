from ....sys.value import MESSAGEBOX_VALUE, MESSAGEBOX_TYPE
from .....sys.error import invalid_type, path_not_exist
from ....sys.win32libs import win32api, Notification


class Msg:
    __slots__ = (
        'title', 
        'text'
    )


    def __init__(self, title='', text=''):
        self.title = title
        self.text = text


    def __enter__(self):
        return self
       

    def __exit__(self, exc_type, exc_value, traceback): ...


    def _init_msg(func):


        def wrapper(self, *args, **kwargs):
            len_args = len(args)

            title = kwargs.get('title', self.title) or (args[0] if args else '')
            text = kwargs.get('text', self.text) or (args[1] if len_args > 1 else '')

            invalid_type('title', title, {'str'})
            invalid_type('text', text, {'str'})

            if func.__name__ == 'push':
                kwargs.setdefault('app_name', args[0] if args else 'Python')
                kwargs.setdefault('launch', args[1] if len_args > 1 else '')
                kwargs.setdefault('icon', args[2] if len_args > 2 else '')

                return func(self, **kwargs)
            
            return Msg._msg_box(title, text, func.__name__)


        return wrapper
        

    @staticmethod
    def _msg_box(title, text, type_msg):
        try:
            return MESSAGEBOX_VALUE[win32api.MessageBox(0, text, title, MESSAGEBOX_TYPE[type_msg])]
        except Exception:
            return False


    @_init_msg
    def push(self, title=None, text=None, app_name=None, launch=None, icon=None):
        invalid_type('app_name', app_name, {'str'})
        invalid_type('launch', launch, {'str'})

        if not app_name:
            app_name = 'Python'

        if icon:
            path_not_exist(icon, file=True)
        
        try:
            Notification(app_id=app_name, title=title, msg=text, launch=launch, icon=icon, duration='long').show()
            return True
        except Exception:
            return False


    @_init_msg
    def default(self, title=None, text=None): ...


    @_init_msg
    def system(self, title=None, text=None): ...


    @_init_msg
    def info(self, title=None, text=None): ...

    
    @_init_msg
    def warning(self, title=None, text=None): ...


    @_init_msg
    def error(self, title=None, text=None): ...

    
    @_init_msg
    def ok(self, title=None, text=None): ...
    

    @_init_msg
    def ok_cancel(self, title=None, text=None): ...


    @_init_msg
    def yes_no(self, title=None, text=None): ...
    

    @_init_msg
    def yes_no_cancel(self, title=None, text=None): ...


    @_init_msg
    def help(self, title=None, text=None): ...


    def __repr__(self):
        return f'Msg(title={repr(self.title)}, text={repr(self.text)})'