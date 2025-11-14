from ..sys.value import ENCODING, FILESYSTEM_ENCODING
from ..sys.error import invalid_type
from ..sys.pyoslibs import detect


def decode_bytes(data, encoding=None):
    invalid_type('data', data, {'bytes', 'bytearray'})
    invalid_type('encoding', encoding, {'nonetype', 'str'})
    
    try:
        if encoding is not None:
            return data.decode(encoding, 'replace')
        
        try:
            detected_encoding = detect(data[:1024], should_rename_legacy=True)['encoding']
        except (UnicodeDecodeError, TypeError):
            try:
                return data.decode(FILESYSTEM_ENCODING, 'replace')
            except UnicodeDecodeError:
                return data.decode(ENCODING, 'replace')
        else:
            return data.decode(detected_encoding, 'replace')
    except Exception:
        return data