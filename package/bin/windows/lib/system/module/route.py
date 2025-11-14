from .....module.shell import shell


def route():
    route_result = {
        'ipv4': [],
        'ipv6': []
    }

    route_print_4 = shell(['route', 'PRINT', '-4'], output=True, system=True)['stdout']
    route_print_6 = shell(['route', 'PRINT', '-6'], output=True, system=True)['stdout']

    if route_print_4 is not None:
        for line in route_print_4.strip().splitlines():
            n = line.split()

            if (len(n) < 5) or (n[1].count('.') != 3):
                continue
            
            route_result['ipv4'].append({
                'netaddress': n[0],
                'netmask': n[1],
                'interface': n[3],
                'gateway': n[2],
                'metric': n[4]
            })
    else:
        route_result['ipv4'] = None
    
    if route_print_6 is not None:
        for line in route_print_6.strip().splitlines():
            n = line.split()

            if len(n) < 3:
                continue
            
            if n[2].count('::'):
                route_result['ipv6'].append({
                    'netaddress': n[2],
                    'gateway': n[-1] if n[2] != n[-1] else 'On-link',
                    'metric': ' '.join(n[:2])
                })
    else:
        route_result['ipv6'] = None

    return route_result