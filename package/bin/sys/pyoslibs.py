from warnings import warn as _warn, filterwarnings as _filterwarnings
_filterwarnings('once')
from ._import import _import




import ctypes as capi
import asyncio
from sys import (
    argv as _argv, 
    platform as sys_os, 
    executable,
    version_info,
    stdin, 
    stdout, 
    stderr
)
from threading import Thread
from multiprocessing import Process
from queue import Queue
from getpass import getuser as getlogin
from os import (
    getpid,
    mkdir,
    rename,
    remove as rmfile,
    rmdir,
    chmod,
    chdir as cd,
    getcwd as pwd,
    getenv,
    putenv as setenv,
    environ,
    get_terminal_size
)
if sys_os != 'win32': 
    from os import getuid, chown
from os.path import (
    exists,
    abspath,
    split as split_path,
    join as join_path,
    isfile,
    isdir
)
from shutil import (
    copy as copy_file, 
    move as move_file, 
    copytree as copy_dir,
    make_archive,
    unpack_archive
)
from glob import glob as find


import socket
import platform
import subprocess as sp
from re import compile as re_compile
from shlex import split as split_command, join as join_command
from locale import getlocale, getencoding, getpreferredencoding
from webbrowser import open as open_site
from json import dump as json_dump
from random import choice
from datetime import datetime
from time import sleep


tabulate = _import('tabulate', from_module=['tabulate'])
FileSystemEventHandler = _import('watchdog.events', from_module=['FileSystemEventHandler'])
Observer = _import('watchdog.observers', from_module=['Observer'])
detect = _import('chardet', from_module=['detect'])
get_http = _import('requests', from_module=['get'])
BleakScanner, BleakError = _import('bleak', from_module=['BleakScanner', 'BleakError'])