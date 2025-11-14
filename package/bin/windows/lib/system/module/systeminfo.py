from .....sys.value import (
    DATE, 
    MACHINE, 
    ARCHITECTURE,
    ENVIRONMENT, 
    NODE, 
    USER,
    LANG,
    ENCODING,
    FILESYSTEM_ENCODING
)
from ....sys.value import OS, SYSTEM_DISK
from .....sys.error import invalid_type

from .is_admin import is_admin
from .os_date import os_date
from .product_code import product_code
from .boot import boot
from .bios import bios
from .battery import battery
from .baseboard import baseboard
from .cpu import cpu
from .gpu import gpu
from .memory import memory
from .ram import ram
from .swap import swap
from .virtual_memory import virtual_memory
from .disk import disk
from .display import display
from .mouse import mouse
from .keyboard import keyboard
from .get_layout import get_layout
from .sound import sound
from .adapter import adapter
from .printer import printer
from .usb import usb
from .device import device
from .users import users
from .ipconfig import ipconfig


def systeminfo(global_inet=False): 
    invalid_type('global_inet', global_inet, 'bool')

    os = OS.copy()

    os['system_disk'] = SYSTEM_DISK
    os['product_code'] = product_code()
    os['os_date'] = os_date()

    return {
        'date': DATE,
        'machine': MACHINE,   
        'architecture': ARCHITECTURE,   
        'os': os,
        'lang': LANG,   
        'encoding': ENCODING,   
        'filesystem_encoding': FILESYSTEM_ENCODING,
        'layout': get_layout(),
        'node': NODE,   
        'user': USER,   
        'is_admin': is_admin(),
        'ipconfig': ipconfig(global_inet),   
        'boot': boot(),
        'bios': bios(),
        'battery': battery(),
        'baseboard': baseboard(),
        'cpu': cpu(),
        'gpu': gpu(),
        'memory': memory(),
        'ram': ram(),
        'swap': swap(),
        'virtual_memory': virtual_memory(),
        'disk': disk(),
        'display': display(),
        'mouse': mouse(),
        'keyboard': keyboard(),
        'sound': sound(),
        'adapter': adapter(),
        'printer': printer(),
        'usb': usb(),
        'device': device(),
        'users': users(),
        'env': ENVIRONMENT
    }