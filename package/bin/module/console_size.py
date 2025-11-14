from ..sys.pyoslibs import get_terminal_size


def console_size():
    try:
        size = get_terminal_size()

        if not hasattr(size, 'columns') or not hasattr(size, 'lines'):
            return None
    except Exception:
        return None
    
    return f'{size.columns}x{size.lines}'