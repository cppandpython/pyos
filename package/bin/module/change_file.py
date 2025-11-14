from ..sys.tool import to_path
from ..sys.error import invalid_type, path_not_exist


@to_path()
def change_file(path, /, pattern, value, delete=False):
    invalid_type('pattern', pattern, {'str'})
    invalid_type('value', value, {'str'})
    invalid_type('delete', delete, {'bool'})

    path_not_exist(path, file=True)

    change_file_result = {
        'path': path,
        'pattern': pattern,
        'value': value,
        'delete': delete,
        'replaced': []
    }
    
    changed = False

    if not value.endswith('\n'):
        value += '\n'

    with open(path, 'r') as f:
        f_data = f.readlines()

    with open(path, 'w') as f:
        if not delete:
            for n in f_data:
                n = n.rstrip()

                if pattern in n:
                    f.write(value)
                    change_file_result['replaced'].append({n: value})
                    changed = True
                else:
                    f.write(n + ('\n' if not n.endswith('\n') else ''))
                    
            if (not changed) and (value not in f_data):
                f.write(value)
                changed = True
        else:
            for n in f_data:
                n = n.rstrip()

                if pattern in n:
                    change_file_result['replaced'].append({n: None})
                    changed = True
                else:
                    f.write(n + ('\n' if not n.endswith('\n') else ''))

    change_file_result['changed'] = changed

    return change_file_result