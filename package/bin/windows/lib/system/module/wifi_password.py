from .....module.shell import shell


def wifi_password():
    wlan_profile = shell(['netsh', 'wlan', 'show', 'profiles'], output=True, system=True)['stdout']

    if wlan_profile is None:
        return None
    
    profile = []
    
    for line in wlan_profile.strip().splitlines():
        n = line.split()

        if n.count(':') == 1:
            profile.append(' '.join(n[n.index(':') + 1:]))

    if profile is None:
        return None
    
    wifi_password_result = []

    for n in profile:
        password_pattern = []

        profile_name = shell(f'netsh wlan show profile name="{n}" key=clear', output=True, system=True)['stdout']

        if profile_name is None:
            continue

        for line in profile_name.strip().splitlines():
            i = line.split()

            if i.count(':') == 1:
                password_pattern.append(i[-1])

        wifi_password_result.append({
            'ssid': n,
            'password': password_pattern[-1]
        })

    return wifi_password_result if wifi_password_result else None