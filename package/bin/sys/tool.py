from .pyoslibs import exists, re_compile, datetime


unpack_module = lambda module, filter_func: {
    name.lower(): value 
    for (name, value) in module.__dict__.items() if filter_func(name, value)
}


def get_date():
    try:
        return datetime.now().strftime('%d.%m.%Y %H:%M:%S').split()
    except Exception:
        return (None, None)


def to_date(value, format_date='%d.%m.%Y', format_time='%H:%M:%S', format_parse='%d.%m.%Y %H:%M:%S'):
    try:
        if value is not None:
            value_date = value if isinstance(value, datetime) else datetime.strptime(value, format_parse)

            date = None if format_date is None else value_date.strftime(format_date)
            time = None if format_time is None else value_date.strftime(format_time)
            
            return [date, time]
    except Exception: ...
    return (None, None)


def to_int(value):
    try:
        if value is not None:
            return int(value)
    except Exception: ...
    return None


def to_mb(value):
    try:
        if value is not None:
            mb = int(value) >> 20

            return mb if mb > 0 else 0
    except Exception: ...
    return None
    

def to_gb(value):
    try:
        if value is not None:
            gb = int(value) >> 30

            return gb if gb > 0 else 0
    except Exception: ...
    return None


def to_ghz(value):
    try:
        if value is not None:
            ghz = round(float(value) / 1_000_000.0, 3)
            
            return ghz if ghz > 0 else None
    except Exception: ...
    return None


def to_path(generator=False):


    def decorator(func):


        def wrapper(path, *args, **kwargs):
            all_args = list(args) 
            all_args.extend(kwargs.values()) 
            
            if isinstance(path, (list, tuple)):
                if generator:
                    return (func(n, *all_args) for n in path)
                
                return [func(n, *i) for (n, i) in zip(path, all_args)] if all_args else [func(n, *all_args) for n in path]
            
            return func(path, *all_args)
        

        return wrapper
        

    return decorator
    

def parse_command(command):
    try:
        bracket = re_compile(r'[(](.*?)[)]').search(command)

        if bracket:
            args = bracket.group(1)
        else:
            args = command.split(None, 1)[1]
    except Exception:
        return (None, None)
  
    args = args.replace("'", '').replace('"', '')

    if exists(args):
        return (args.replace('/', '_').replace('\\', '_').replace(':', '_'), args)
    
    return (args.replace(' ', '_'), args)