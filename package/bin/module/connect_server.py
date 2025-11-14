from ..sys.error import format_error, invalid_type, invalid_value
from ..sys.pyoslibs import socket


def connect_server(host, port, ipv4=True, protocol='tcp', connection=0, timeout=None):
    invalid_type('host', host, {'str', 'int'})
    invalid_type('port', port, {'int'})
    invalid_type('ipv4', ipv4, {'bool'})
    invalid_type('protocol', protocol, {'str'})
    invalid_type('connection', connection, {'int'})
    invalid_type('timeout', timeout, {'nonetype', 'int', 'float'})

    invalid_value('protocol', protocol, protocol not in {'tcp', 'udp'}, 'tcp, udp')
    invalid_value('connection', connection, connection < 0, 'connection >= 0')

    if timeout is not None:
        invalid_value('timeout', timeout, timeout < 0, 'timeout >= 0')

    connect_server_result = {
        'server': None,
        'address': None,
        'status': None,
        'error': None
    }

    try:
        sock = socket.socket(
            socket.AF_INET if ipv4 else socket.AF_INET6,
            socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM,
        )

        if timeout is not None:
            sock.settimeout(timeout)

        sock.connect((host, port)) 
    except socket.timeout:
        connect_server_result['error'] = 'timeout waiting for connection'
        connect_server_result['status'] = False
    except socket.gaierror as error:
        connect_server_result['error'] = f'host error: {format_error(error)}'
        connect_server_result['status'] = False
    except Exception as error:
        connect_server_result['error'] = format_error(error)
        connect_server_result['status'] = False
    else:
        connect_server_result['server'] = sock
        connect_server_result['address'] = (host, port)
        connect_server_result['status'] = True
    finally:
        if not connect_server_result['status']:
            sock.close()

    return connect_server_result 