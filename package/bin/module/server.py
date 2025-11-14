from ..sys.error import format_error, invalid_type, invalid_value
from ..sys.pyoslibs import socket


def server(host, port, ipv4=True, protocol='tcp', connection=0, timeout=None):
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

    server_result = {
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
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))

        if timeout is not None:
            sock.settimeout(timeout)
    except Exception as error:
        server_result['error'] = f'bind failed: {format_error(error)}'
        server_result['status'] = False
    else:
        if protocol == 'tcp':
            try:
                sock.listen(connection)

                server_result['server'] = lambda: sock.accept()
                server_result['address'] = (host, port)
                server_result['status'] = True
            except socket.timeout:
                server_result['error'] = 'timeout waiting for connection'
                server_result['status'] = False
            except Exception as error:
                server_result['error'] = f'accept failed: {format_error(error)}'
                server_result['status'] = False
        else:
            server_result['server'] = sock
            server_result['address'] = (host, port)
            server_result['status'] = True
    finally:
        if not server_result['status']:
            sock.close()
    
    return server_result 