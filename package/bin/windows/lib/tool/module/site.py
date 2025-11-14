from ....sys.value import FILE_HOSTS
from .....sys.tool import get_date
from .....sys.error import invalid_type
from .....sys.pyoslibs import socket, open_site

from .....module.change_file import change_file


class Site:
    __slots__ = (
        'url',
        'domain',
        'ip'
    )


    def __init__(self, url):
        invalid_type('url', url, {'str'})

        self.url = url
        self.domain = self._get_domain()
        self.ip = self._get_ip()


    def __enter__(self):
        return self
       

    def __exit__(self, exc_type, exc_value, traceback): ...


    def __bool__(self):
        return self.ip is not None


    def __eq__(self, other):
        invalid_type('other', other, {'site'})

        return self.url == other.url
    
    
    def __ne__(self, other):
        return not self.__eq__(other)

 
    def _get_domain(self):
        for n in self.url.split('/'):
            if n and not n.startswith('http'):
                return n

        return None
    

    def _get_ip(self):
        try:
            return socket.gethostbyname(self.domain)
        except Exception:
            return None
    

    def open(self):
        return open_site(self.url)


    def block(self):
        date = get_date()

        try:
            return change_file(FILE_HOSTS, self.domain, f'127.0.0.1    {self.domain}    # {date[0]} {date[1]}')['changed']
        except Exception:
            return False


    def unblock(self):
        try:
           return change_file(FILE_HOSTS, self.domain, self.domain, delete=True)['changed']
        except Exception:
            return False 


    @staticmethod
    def all_unblock():
        try:
            with open(FILE_HOSTS, 'w'): 
                return True
        except Exception:
            return False
    

    @staticmethod
    def get_blocked():
        try:
            with open(FILE_HOSTS, 'r') as f:
                hosts_data = f.read()
        except Exception:
            return None
        
        blocked_site = []
        
        for line in hosts_data.strip().splitlines():
            n = line.split()

            if (len(n) != 5) or (n[2] != '#'):
                continue

            blocked_site.append({
                'domain': n[1],
                'date': (n[3], n[4])
            })
        
        return blocked_site if blocked_site else None


    def __repr__(self):
        return f'Site({repr(self.url)})'