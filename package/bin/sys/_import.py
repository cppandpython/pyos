from .pyoslibs import _warn


class EmptyModule:
    def __init__(self, *args, **kwargs): ...
    def __call__(self, *args, **kwargs): return EmptyModule()  
    def __getattribute__(self, _): return '<EmptyModule>'
    def __setattr__(self, name, value): super().__setattr__(name, value)
    def __getitem__(self, _): return '<EmptyModule>'
    def __iter__(self): yield from []
    def __len__(self): return 0
    def __repr__(self): return '<EmptyModule>'


def _import(name, from_module=None, spec='', deep=0):
    try:
        module = __import__(
            name, 
            fromlist=[] if from_module is None else from_module, 
            globals={'__spec__': spec}, 
            level=deep
        )
    except (ModuleNotFoundError, ImportError):
        _warn(f'module ({name}) is not installed', category=RuntimeWarning)
        
        return EmptyModule() if len(from_module) == 1 else [EmptyModule() for _ in from_module]
    else:
        if from_module is None:
            return module
        
        return getattr(module, from_module[0], EmptyModule()) if len(from_module) == 1 else [getattr(module, n, EmptyModule()) for n in from_module]