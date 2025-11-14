from ..sys.error import format_error, invalid_type, invalid_value
from ..sys.pyoslibs import sp, split_command, join_command

from ..module.decode_bytes import decode_bytes


def shell(command, input=None, output=None, encoding=None, system=False, env=None, timeout=None):
    invalid_type('command', command, {'str', 'list', 'tuple'})   
    invalid_type('input', input, {'nonetype', 'str', 'bytes'})
    invalid_type('output', output, {'nonetype', 'bool'})
    invalid_type('system', system, {'bool'})
    invalid_type('env', env, {'nonetype', 'dict'})
    invalid_type('timeout', timeout, {'nonetype', 'int', 'float'})
    
    if isinstance(input, str):
        input = input.encode()

    if timeout is not None:
        invalid_value('timeout', timeout, timeout < 0, 'timeout >= 0')
    
    if not system and isinstance(command, str):
        command = split_command(command)

    elif system and isinstance(command, (list, tuple)):
        command = join_command(command)

    command_result = {
        'stdout': None,
        'stderr': None,
        'status': None,
        'error': None
    }
    
    try:
        shell_result = sp.run(
            command, 
            input=input, 
            stdout=sp.DEVNULL if output is None else None,
            stderr=sp.DEVNULL if output is None else None,
            capture_output=bool(output),
            shell=system,
            env=env,
            timeout=timeout
        ) 
    except FileNotFoundError:
        command_result['error'] = f'command not found "{command}"'
        command_result['status'] = False
    except sp.TimeoutExpired:
        command_result['error'] = f'timeout after {timeout}'
        command_result['status'] = False
    except Exception as error:
        command_result['error'] = format_error(error)
        command_result['status'] = False
    else:
        if output:
            command_result['stdout'] = decode_bytes(shell_result.stdout, encoding) if shell_result.stdout else None
            command_result['stderr'] = decode_bytes(shell_result.stderr, encoding) if shell_result.stderr else None
            command_result['status'] = shell_result.returncode == 0 
        else: 
            command_result['status'] = shell_result.returncode == 0 

    return command_result 