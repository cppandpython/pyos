from ....sys.value import CONSOLE_COLOR_VALUE, CONSOLE_COLOR_NAME
from .....sys.error import invalid_type, invalid_value, failed_connect
from .....sys.pyoslibs import capi, stdout
from ....sys.win32libs import win32console

from .....module.shell import shell
from .....module.console_size import console_size
from .....module.clear import clear as clear_console


class CONSOLE_FONT_SIZE(capi.Structure):
    _fields_ = [
        ('X', capi.c_short),
        ('Y', capi.c_short)
    ]


class CONSOLE_FONT(capi.Structure):
    _fields_ = [
        ('cbSize', capi.c_ulong),
        ('nFont', capi.c_ulong),
        ('dwFontSize', CONSOLE_FONT_SIZE),
        ('FontFamily', capi.c_ulong),
        ('FontWeight', capi.c_ulong),
        ('FaceName', capi.c_wchar * 32)
    ]


class Console:
    __slots__ = (
        '_std_out_handle',
        '_std_input_handle'
    )
    

    def __init__(self): 
       self._std_out_handle = None
       self._std_input_handle = None


    def __enter__(self):
        if not self._std_out_handle:
            try:
                self._std_out_handle = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
            except Exception:
                failed_connect('console output')

        if not self._std_input_handle:
            try:
                self._std_input_handle = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)
            except Exception:
                failed_connect('console input')

        return self
       

    def __exit__(self, exc_type, exc_value, traceback): 
        if self._std_out_handle:
            self._std_out_handle.Close()
            self._std_out_handle = None
        
        if self._std_input_handle:
            self._std_input_handle.Close()
            self._std_input_handle = None


    def execute(self, *args, **kwargs):
        return shell(*args, **kwargs)
    

    def clear(self):
        return clear_console()
    

    def input(self, prompt='', buffer=1024):
        invalid_type('prompt', prompt, {'str'})
        invalid_type('buffer', buffer, {'int'})

        invalid_value('buffer', buffer, buffer < 1, 'buffer >= 1')

        self.write(prompt)

        with self:
            try:
                data = self._std_input_handle.ReadConsole(buffer)
            except Exception:
                return None

        return data
    

    def read(self):
        return stdout.read() if stdout.readable() else None
       

    def write(self, data):
        invalid_type('data', data, {'str'})
        
        with self:
            try:
                self._std_out_handle.WriteConsole(data)
                return True
            except Exception:
                return False
        

    def get_color(self):
        with self:
            try:
                attr = self._std_out_handle.GetConsoleScreenBufferInfo()['Attributes']
            except Exception:
                return None
        
        foreground = attr & 0x0F  
        background = (attr >> 4) & 0x0F  

        return {
            'foreground': CONSOLE_COLOR_VALUE.get(foreground),
            'background': CONSOLE_COLOR_VALUE.get(background)
        }
    

    def set_color(self, foreground=None, background=None):
        invalid_type('foreground', foreground, {'nonetype', 'str'})
        invalid_type('background', background, {'nonetype', 'str'})

        attr = 0

        if foreground is not None:
            foreground_color = CONSOLE_COLOR_NAME.get(foreground)

            invalid_value('foreground', foreground, foreground_color is None, 'black, blue, green, aqua, red, purple, yellow, white, gray, bright blue, bright green, bright aqua, bright red, bright purple, bright yellow, bright white')

            attr |= foreground_color 

        if background is not None:
            background_color = CONSOLE_COLOR_NAME.get(background)

            invalid_value('background', background, background_color is None, 'black, blue, green, aqua, red, purple, yellow, white, gray, bright blue, bright green, bright aqua, bright red, bright purple, bright yellow, bright white')

            attr |= (background_color << 4) 
        
        with self:
            try:
                self._std_out_handle.SetConsoleTextAttribute(attr)
                return True
            except Exception:
                return False


    def get_size(self):
        return console_size()


    def set_size(self, width, height):
        invalid_type('width', width, {'int'})
        invalid_type('height', height, {'int'})

        with self:
            try:
                self._std_out_handle.SetConsoleScreenBufferSize(win32console.PyCOORDType(width, height))
                self._std_out_handle.SetConsoleWindowInfo(True, win32console.PySMALL_RECTType(0, 0, width - 1, height - 1))
                return True
            except Exception:
                return False
    

    def get_title(self):
        try:
            return win32console.GetConsoleTitle()
        except Exception:
            return None


    def set_title(self, title):
        invalid_type('title', title, {'str'})

        try:
            win32console.SetConsoleTitle(title)
            return True
        except Exception:
            return False
        
    
    def get_cursor(self):
        with self:
            try:
                return self._std_out_handle.GetConsoleCursorInfo()
            except Exception:
                return None
    

    def set_cursor(self, size, visible):
        invalid_type('size', size, {'int'})
        invalid_type('visible', visible, {'bool'})

        with self:
            try:
                self._std_out_handle.SetConsoleCursorInfo(size, visible)
                return True
            except Exception:
                return False


    def move_cursor(self, x, y):
        invalid_type('x', x, {'int'})
        invalid_type('y', y, {'int'})

        with self:
            try:
                self._std_out_handle.SetConsoleCursorPosition(win32console.PyCOORDType(x, y))
                return True
            except Exception:
                return False


    def get_font(self):
        kernel32 = capi.windll.kernel32

        std_handle = kernel32.GetStdHandle(win32console.STD_OUTPUT_HANDLE)

        font = CONSOLE_FONT()
        font.cbSize = capi.sizeof(CONSOLE_FONT)  

        if kernel32.GetCurrentConsoleFontEx(std_handle, False, capi.byref(font)) == 0:
            return None
        
        dwFontSize = getattr(font, 'dwFontSize', None)

        return {
            'name': getattr(font, 'FaceName', None),
            'size': {
                'width': getattr(dwFontSize, 'X', None), 
                'height': getattr(dwFontSize, 'Y', None)
            }, 
            'weight': getattr(font, 'FontWeight', None),
            'family': getattr(font, 'FontFamily', None),
            'font': getattr(font, 'nFont', None)
        }
    

    def set_font(self, name, size, weight):
        invalid_type('name', name, {'str'})
        invalid_type('size', size, {'list', 'tuple'})
        invalid_type('weight', weight, {'int'})

        invalid_value('size', size, len(size) != 2, 'width, height')

        kernel32 = capi.windll.kernel32

        std_handle = kernel32.GetStdHandle(win32console.STD_OUTPUT_HANDLE)

        if std_handle == -1:
            return False

        font = CONSOLE_FONT()
        font.cbSize = capi.sizeof(CONSOLE_FONT)
        font.nFont = 0
        font.dwFontSize = CONSOLE_FONT_SIZE(*size)  
        font.FontFamily = 54
        font.FontWeight = weight
        font.FaceName = name

        return kernel32.SetCurrentConsoleFontEx(std_handle, False, capi.byref(font)) != 0


    def get_mode(self):
        with self:
            try:
                mode = self._std_out_handle.GetConsoleMode()
            except Exception:
                return None
            
            return {
                'ENABLE_ECHO_INPUT': bool(mode & win32console.ENABLE_ECHO_INPUT),
                'ENABLE_LINE_INPUT': bool(mode & win32console.ENABLE_LINE_INPUT),
                'ENABLE_MOUSE_INPUT': bool(mode & win32console.ENABLE_MOUSE_INPUT),
                'ENABLE_PROCESSED_INPUT': bool(mode & win32console.ENABLE_PROCESSED_INPUT),
                'ENABLE_PROCESSED_OUTPUT': bool(mode & win32console.ENABLE_PROCESSED_OUTPUT),
                'ENABLE_WINDOW_INPUT': bool(mode & win32console.ENABLE_WINDOW_INPUT),
                'ENABLE_WRAP_AT_EOL_OUTPUT': bool(mode & win32console.ENABLE_WRAP_AT_EOL_OUTPUT)
            }
    

    def set_mode(self, enable_echo_input=None, enable_line_input=None, enable_mouse_input=None, enable_processed_input=None, enable_processed_output=None, enable_window_input=None, enable_wrap_at_eol_output=None):
        invalid_type('enable_echo_input', enable_echo_input, {'nonetype', 'bool'})
        invalid_type('enable_line_input', enable_line_input, {'nonetype', 'bool'})
        invalid_type('enable_mouse_input', enable_mouse_input, {'nonetype', 'bool'})
        invalid_type('enable_processed_input', enable_processed_input, {'nonetype', 'bool'})
        invalid_type('enable_processed_output', enable_processed_output, {'nonetype', 'bool'})
        invalid_type('enable_window_input', enable_window_input, {'nonetype', 'bool'})
        invalid_type('enable_wrap_at_eol_output', enable_wrap_at_eol_output, {'nonetype', 'bool'})

        with self:
            try:
                mode = self._std_out_handle.GetConsoleMode()
            except Exception:
                return False

        mode_flag = {
            win32console.ENABLE_ECHO_INPUT: enable_echo_input,
            win32console.ENABLE_LINE_INPUT: enable_line_input,
            win32console.ENABLE_MOUSE_INPUT: enable_mouse_input,
            win32console.ENABLE_PROCESSED_INPUT: enable_processed_input,
            win32console.ENABLE_PROCESSED_OUTPUT: enable_processed_output,
            win32console.ENABLE_WINDOW_INPUT: enable_window_input,
            win32console.ENABLE_WRAP_AT_EOL_OUTPUT: enable_wrap_at_eol_output,
        }

        new_mode = mode

        for (flag, value) in mode_flag.items():
            if value is None:
                continue  
    
            if value:
                new_mode |= flag  
            else:
                new_mode &= ~flag  

        if new_mode != mode:
            with self:
                try:
                    self._std_out_handle.SetConsoleMode(new_mode)
                except Exception: 
                    return False
        
        return True