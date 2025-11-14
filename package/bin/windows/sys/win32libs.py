from ...sys._import import _import




import winreg
from os import startfile


win32con = _import('win32con')
win32api = _import('win32api')
win32connect = _import('win32com.client', from_module=['Dispatch'])
win32gui = _import('win32gui')
win32console = _import('win32console')
win32clipboard = _import('win32clipboard')
win32service = _import('win32service')
win32serviceutil = _import('win32serviceutil')
win32security = _import('win32security')
win32evtlog = _import('win32evtlog')
PyWiFi, pywifi_set_loglevel = _import('pywifi', from_module=['PyWiFi', 'set_loglevel'])
Notification = _import('winotify', from_module=['Notification'])