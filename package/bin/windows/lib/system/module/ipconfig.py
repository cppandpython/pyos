from .....sys.value import HTTP_HEADER, IPCONFIG_GLOBAL_NETWORK_URL, IPCONFIG_GLOBAL_NETWORK_KEY
from ....sys.tool import wmi_connect
from .....sys.error import invalid_type
from .....sys.pyoslibs import get_http


QUERY = '''
SELECT 
    Description, 
    DefaultIPGateway, 
    IPAddress, 
    MACAddress 
FROM Win32_NetworkAdapterConfiguration 
WHERE IPEnabled = TRUE
'''


def ipconfig(global_inet=False):
    invalid_type('global_inet', global_inet, {'bool'})
    
    try:
        wmi = wmi_connect()

        local_network = [{
            'adapter': getattr(n, 'Description', None),  
            'ip_route': n.DefaultIPGateway[0] if n.DefaultIPGateway else None,
            'ipv4': n.IPAddress[0] if n.IPAddress else None,
            'ipv6': n.IPAddress[1] if len(n.IPAddress) > 1 else None,
            'mac': getattr(n, 'MACAddress', None)
        } for n in wmi.ExecQuery(QUERY)]
    except Exception:
        local_network = None

    if global_inet:
        try:
            global_network = get_http(IPCONFIG_GLOBAL_NETWORK_URL, headers=HTTP_HEADER, timeout=10).json()
        except Exception:
            global_network = {}
        else:
            global_network_data = {
                'ip': global_network.get(IPCONFIG_GLOBAL_NETWORK_KEY['ip']),
                'isp': global_network.get(IPCONFIG_GLOBAL_NETWORK_KEY['isp']),
                'country': global_network.get(IPCONFIG_GLOBAL_NETWORK_KEY['country']),
                'region': global_network.get(IPCONFIG_GLOBAL_NETWORK_KEY['region']),
                'city': global_network.get(IPCONFIG_GLOBAL_NETWORK_KEY['city']),
                'postal': global_network.get(IPCONFIG_GLOBAL_NETWORK_KEY['postal']),
                'timezone': global_network.get(IPCONFIG_GLOBAL_NETWORK_KEY['timezone']),
                'location': global_network.get(IPCONFIG_GLOBAL_NETWORK_KEY['location'])  
            }

    return {
        'local_network': local_network,
        'global_network': global_network_data if global_inet else None
    }