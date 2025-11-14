from .....module.shell import shell


def arp():
    arp_a = shell(['arp', '-a'], output=True, system=True)['stdout']

    if arp_a is None:
        return None

    arp_result = []

    for line in arp_a.strip().splitlines():
        n = line.split()

        if (len(n) < 3) or (n[0].count('.') != 3):
            continue

        arp_result.append({
            'ip': n[0],
            'mac': n[1].replace('-', ':').upper(),
            'type': n[2]
        })
    
    return arp_result if arp_result else None