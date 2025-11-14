from ..sys.define_os import IS_WINDOWS, IS_LINUX
from ..sys.value import CIPHER_MAP, AKM_MAP
from ..sys.tool import to_ghz
from ..sys.error import invalid_type, invalid_value, no_interface
from ..sys.pyoslibs import sleep
if IS_WINDOWS:
    from ..windows.sys.win32libs import PyWiFi, pywifi_set_loglevel
elif IS_LINUX:
    from ..linux.sys.linuxlibs import PyWiFi, pywifi_set_loglevel
else:
    'Доделать для macOS'


pywifi_set_loglevel(50)


def ghz_to_channel(ghz):
    if (ghz is None) or (ghz < 0):
        return None

    mhz = ghz * 1000  

    if 2400 <= mhz <= 2500: 
        return int((mhz - 2407) // 5)
    elif 5000 <= mhz <= 6000:
        return int((mhz - 5000) // 5)
    elif 5950 <= mhz <= 7125:
        return int((mhz - 5950) // 5)
    
    return None


def wifi(timeout=3):
    invalid_type('timeout', timeout, {'int'})

    invalid_value('timeout', timeout, timeout < 0, 'timeout >= 0')

    interfaces = PyWiFi().interfaces()

    no_interface(not interfaces)
    
    iface_result = []

    for iface in interfaces:
        try:
            iface.scan()
            sleep(timeout)
            iface_result = iface.scan_results()
        except Exception:
            continue

        if iface_result:
            break

    if not iface_result:
        return None
    
    wifi_result = []

    iface_result.sort(key=lambda n: n.signal, reverse=True)

    for n in iface_result:
        if hasattr(n, 'ssid'):
            try:
                ssid = n.ssid.encode('raw_unicode_escape').decode(errors='replace') or '<hidden>'
            except Exception:
                ssid = n.ssid or '<hidden>' 
        else:
            ssid = None

        bssid = getattr(n, 'bssid', None) 
        ghz = to_ghz(getattr(n, 'freq', None))

        wifi_result.append({
            'ssid': ssid,
            'bssid': bssid.strip(':').upper() if isinstance(bssid, str) else None,
            'ghz': ghz,
            'channel': ghz_to_channel(ghz),
            'auth': AKM_MAP.get(getattr(n, 'akm', [6])[0]),
            'cipher': CIPHER_MAP.get(getattr(n, 'cipher', None)),
            'signal': getattr(n, 'signal', None)
        })

    return wifi_result if wifi_result else None