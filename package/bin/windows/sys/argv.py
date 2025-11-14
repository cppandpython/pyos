from ...sys.tool import unpack_module, parse_command
from ...sys.error import format_error, invalid_value, path_not_exist
from ...sys.pyoslibs import _warn, mkdir, join_path, isdir, json_dump

from ..lib.const import const
from ..lib.system import system
from ..lib.tool import tool
from ..lib.device import device


def to_json(command, data):
    with open(join_path('pyosdata', command + '.json'), 'w') as result_json:
        json_dump(data, result_json, indent=4, ensure_ascii=False)


def parser(line):
    line_lower = line.lower()


    const_value = CONST.get(line_lower, NotImplemented)

    if const_value is not NotImplemented:
        to_json(line_lower, const_value)
        return
    

    for n in SYSTEM:
        if not line_lower.startswith(n):
            continue
        
        exit(0)

        file_name = n
        func = SYSTEM[n]


        # if n == 'cmd':

        #     name, arg = parse_single_arg(line_lower)

        #     func.__defaults__ = (arg, None, True, None, True, None, None) 
        #     file_name = f'cmd_{name}'


        to_json(file_name, func())
        return


def _executor_argv(args):
    global CONST, SYSTEM

    CONST = unpack_module(const, lambda name, _: name.isupper())
    SYSTEM = unpack_module(system, lambda _, value: callable(value))

    flag = args[0]

    if flag == '-e':
        command = args[1:]
    elif flag == '-f':
        path = args[1]

        path_not_exist(path, file=True)
        
        with open(path, 'r') as args_file:
            command = args_file.readlines()
    else:
        invalid_value('flag', flag, True, '-e execute arguments | -f path to file to execute')

    if not isdir('pyosdata'):
        mkdir('pyosdata')

    for n in command:
        try:
            parser(n.strip())
        except Exception as error:
            _warn(f'\n({n}): {format_error(error)}', category=RuntimeWarning) 