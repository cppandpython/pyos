from package.bin.sys.define_os import IS_ANDROID, IS_WINDOWS, IS_LINUX, IS_MACOS

from setuptools import setup, find_packages




MODULE = [    
    'tabulate',
    'watchdog',
    'chardet',
    'requests',
    'bleak'
]


LINUX_PACKAGE = [
    
]




if IS_ANDROID:
    ...
elif IS_WINDOWS:
    MODULE.append('pywin32')
    MODULE.append('pywifi')
    MODULE.append('winotify')
elif IS_LINUX:
    MODULE.append('pywifi')
elif IS_MACOS:
    ...




setup(
    url='https://github.com/cppandpython/pyos',
    name='pyos',
    version='0.2.0',
    description='Cross-platform library of OS utilities',
    author='Vladislav Khudash',
    author_email='',
    packages=find_packages(),
    install_requires=MODULE,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS (Android, Windows, Linux, macOS)'
    ],
    python_requires='>=3.6'
)