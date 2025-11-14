from .pyoslibs import exists, isfile, isdir


format_error = lambda error: f'{type(error).__name__}({error})'


def invalid_type(name, value, valid):
    value_type = type(value).__name__.lower()

    if value_type not in valid:
        raise TypeError(f'({name} is {value_type}) must be one of {valid} only')


def invalid_value(name, value, not_valid, expected):
    if not_valid:
        raise ValueError(f'({name} is {value}) invalid value, acceptable value ({expected})')


def name_not_exist(name, not_valid):
    if not_valid:
        raise NameError(f'name ({name}) is not exist')


def key_not_exist(key, not_valid):
    if not_valid:
        raise KeyError(f'key ({key}) is not exist')


def path_not_exist(path, file=False, dir=False, exc=False):
    invalid_type('path', path, {'str'})

    if exc or not exists(path):
        raise FileNotFoundError(f'path ({path}) is not exist')

    if file:
        if not isfile(path):
            raise TypeError(f'({path}) is not file')

    if dir:
        if not isdir(path):
            raise TypeError(f'({path}) is not dir')


def no_interface(not_valid):
    if not_valid:
        raise RuntimeError('no interface')


def failed_connect(name):
    raise ConnectionError(f'failed to connect to {name}')