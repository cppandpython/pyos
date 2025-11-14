from .....sys.tool import to_int

from .....module.shell import shell


def netstat():
    netstat_ano = shell(['netstat', '-ano'], output=True, system=True)['stdout']

    if netstat_ano is None:
        return None
    
    netstat_result = []

    for line in netstat_ano.strip().splitlines():
        n = line.split()

        if len(n) < 4:
            continue

        local_host = n[1] 
        foreign_host = n[2]
        status = n[3]

        try:
            local_address_index = local_host.rindex(':')
            local_address = (local_host[:local_address_index], local_host[local_address_index + 1:])
        except Exception:
            local_address = local_host

        try:
            foreign_host_index = foreign_host.rindex(':')
            foreign_address = (foreign_host[:foreign_host_index], foreign_host[foreign_host_index + 1:])
        except Exception:
            foreign_address = foreign_host

        netstat_result.append({
            'pid': to_int(n[-1]),  
            'protocol': n[0],  
            'local_address': local_address,  
            'foreign_address': foreign_address,  
            'status': status if not status.isdigit() else None
        })
    
    return netstat_result if netstat_result else None