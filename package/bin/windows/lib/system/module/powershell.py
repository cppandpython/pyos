from .....module.shell import shell


def powershell(command, *args, **kwargs):
    if isinstance(command, (list, tuple)):
        command = ['powershell'] + list(command)
    
    elif isinstance(command, str):
        command = 'powershell' + ' ' + command.lstrip()
    
    return shell(command, *args, **kwargs)