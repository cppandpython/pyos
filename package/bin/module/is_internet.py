from ..sys.value import HTTP_HEADER, IS_INTERNET_STATUS_URL
from ..sys.pyoslibs import get_http


def is_internet():
    try:
        return get_http(IS_INTERNET_STATUS_URL, headers=HTTP_HEADER, timeout=10).ok
    except Exception: 
        return False