from .....module.shell import shell


def task():
    schtasks_query = shell(['schtasks', '/query', '/fo', 'csv'], output=True, system=True)['stdout']

    if schtasks_query is None:
        return None
    
    task_result = []

    for line in schtasks_query.strip().splitlines():
        n = line.replace('"', '').split(',')
  
        if (not n[0].startswith('\\')) or (len(n) != 3):
            continue

        task_result.append({
            'name': n[0],
            'event': n[1],
            'status': n[2]
        })
    
    return task_result if task_result else None