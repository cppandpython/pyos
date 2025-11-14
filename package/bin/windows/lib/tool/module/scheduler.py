from ....sys.value import (
    TASK_LOGONTYPE, 
    TASK_RUNLEVEL,
    TASK_ACTION,
    TASK_TRIGGER
)
from .....sys.tool import to_date
from .....sys.error import invalid_type, name_not_exist, path_not_exist, failed_connect
from win32com.client import Dispatch as win32connect # from ....sys.win32libs import win32connect

from ...system.module.task import task


class Scheduler:
    __slots__ = (
        'name',
        'path',
        '_scheduler_handle',
        '_dir_handle'
    )


    def __init__(self, name, path='\\'): 
        invalid_type('name', name, {'str'})

        self.name = name
        self.path = path

        self._scheduler_handle = None
        self._dir_handle = None


    def __enter__(self):
        if not self._scheduler_handle:
            try:
                self._scheduler_handle = win32connect('Schedule.Service')
                self._scheduler_handle.Connect()
            except Exception:
                failed_connect('scheduler')
        
        if not self._dir_handle:
            try:
                self._dir_handle = self._scheduler_handle.GetFolder(self.path)
            except Exception:
                path_not_exist(self.path, exc=True)

        return self
       

    def __exit__(self, exc_type, exc_value, traceback): 
        if self._scheduler_handle:
            self._scheduler_handle = None

        if self._dir_handle:
            self._dir_handle = None


    def __bool__(self):
        return self.exists()
    

    def __eq__(self, other):
        invalid_type('other', other, {'scheduler'})

        return (self.name == other.name) and (self.path == other.path)
         
    
    def __ne__(self, other):
        return not self.__eq__(other)
    

    def _task(self):
        if self.exists():
            with self:
                try:
                    return self._dir_handle.GetTask(self.name)
                except Exception: ...

        return None
    

    @staticmethod 
    def get_task():
        return task()
    

    def info(self):
        name_not_exist(self.name, not self.exists())
        
        task_info = {
            'name': None,
            'description': None,
            'path': None,
            'id': None,
            'group': None,
            'owner': None,
            'author': None,
            'info': {
                'priority': None,
                'logon': None,
                'ondemand': None,
                'start_when_available': None,
                'wake_to_run': None,
                'run_only_if_idle': None,
                'stop_if_going_on_batteries': None,
                'allow_hard_terminate': None,
                'allow_idle_termination': None,
                'stop_on_idle_end': None,
                'restart_if_terminated': None,
                'hidden': None,
                'privilege': None,
                'next_runtime': None,
                'last_runtime': None,
                'execution_time_limit': None,
                'enabled': None,
                'status': None,
                'exit_code': None
            },
            'action': [],
            'trigger': []
        }
        
        task = self._task()
     
        if task is None:
            return task_info

        definition = getattr(task, 'Definition', None)

        registration = getattr(definition, 'RegistrationInfo', None)
        principal = getattr(definition, 'Principal', None)
        settings = getattr(definition, 'Settings', None)
        actions = getattr(definition, 'Actions', None)
        trigger = getattr(definition, 'Triggers', None)

        task_info['name'] = getattr(task, 'Name', None)
        task_info['path'] = getattr(task, 'Path', None)
        task_info['info']['next_runtime'] = to_date(getattr(task, 'NextRunTime', None))
        task_info['info']['last_runtime'] = to_date(getattr(task, 'LastRunTime', None))
        task_info['info']['enabled'] = getattr(task, 'Enabled', None)
        task_info['info']['status'] = getattr(task, 'state', None)
        task_info['info']['exit_code'] = getattr(task, 'LastTaskResult', None)

        if registration is not None:
            task_info['author'] = getattr(registration, 'Author', None)
            task_info['description'] = getattr(registration, 'Description', None)

        if principal is not None:
            task_info['id'] = getattr(principal, 'id', None)
            task_info['group'] = getattr(principal, 'GroupId', None)
            task_info['owner'] = getattr(principal, 'UserId', None)
            task_info['info']['logon'] = TASK_LOGONTYPE.get(getattr(principal, 'LogonType', None))
            task_info['info']['privilege'] = TASK_RUNLEVEL.get(getattr(principal, 'RunLevel', None))

        if settings is not None:
            task_info['info']['priority'] = getattr(settings, 'Priority', None)
            task_info['info']['ondemand'] = getattr(settings, 'AllowDemandStart', None)
            task_info['info']['start_when_available'] = getattr(settings, 'StartWhenAvailable', None)
            task_info['info']['wake_to_run'] = getattr(settings, 'WakeToRun', None)
            task_info['info']['run_only_if_idle'] = getattr(settings, 'RunOnlyIfIdle', None)
            task_info['info']['stop_if_going_on_batteries'] = getattr(settings, 'StopIfGoingOnBatteries', None)
            task_info['info']['allow_hard_terminate'] = getattr(settings, 'AllowHardTerminate', None)
            task_info['info']['allow_idle_termination'] = getattr(settings, 'AllowIdleTermination', None)
            task_info['info']['stop_on_idle_end'] = getattr(settings, 'StopOnIdleEnd', None)
            task_info['info']['restart_if_terminated'] = getattr(settings, 'RestartIfNecessary', None)
            task_info['info']['hidden'] = getattr(settings, 'Hidden', None)
            task_info['info']['execution_time_limit'] = getattr(settings, 'ExecutionTimeLimit', None)
            task_info['info']['enabled'] = getattr(settings, 'Enabled', None)

        if actions is not None:
            for n in actions:
                action_type = TASK_ACTION.get(getattr(n, 'Type', None))

                if action_type == 'TASK_ACTION_EXEC':
                    task_info['action'].append({
                        'id': getattr(n, 'Id', None),
                        'dir': getattr(n, 'WorkingDirectory', None),
                        'command': getattr(n, 'Path', None),
                        'args': getattr(n, 'Arguments', None),
                        'type': action_type,
                        'window': getattr(n, 'HideAppWindow', None)
                    })
                elif action_type == 'TASK_ACTION_SEND_EMAIL':
                    task_info['action'].append({
                        'id': getattr(n, 'Id', None),
                        'to': getattr(n, 'To', None),
                        'from': getattr(n, 'From', None),
                        'subject': getattr(n, 'Subject', None),
                        'body': getattr(n, 'Body', None),
                        'server': getattr(n, 'Server', None),
                        'port': getattr(n, 'ServerPort', None),
                        'username': getattr(n, 'UserName', None),
                        'password': getattr(n, 'Password', None),
                        'priority': getattr(n, 'Priority', None),
                        'type': action_type
                    })
                elif action_type == 'TASK_ACTION_SHOW_MESSAGE':
                    task_info['action'].append({
                        'id': getattr(n, 'Id', None),
                        'message': getattr(n, 'Message', None),
                        'title': getattr(n, 'Title', None),
                        'type': action_type
                    })

        if trigger is not None:
            for n in trigger:
                repetition = getattr(n, 'Repetition', None)
                task_repetition = None

                if repetition is not None:
                    task_repetition = {
                        'interval': getattr(repetition, 'Interval', None),  
                        'duration': getattr(repetition, 'Duration', None),  
                        'stop_duration_end': getattr(repetition, 'StopAtDurationEnd', None)  
                    }

                task_info['trigger'].append({
                    'id': getattr(n, 'Id', None),
                    'enabled': getattr(n, 'Enabled', None),
                    'type': TASK_TRIGGER.get(getattr(n, 'Type', None)),
                    'start_boundary': getattr(n, 'StartBoundary', None),
                    'end_boundary': getattr(n, 'EndBoundary', None),
                    'days_interval': getattr(n, 'DaysInterval', None),
                    'delay': getattr(n, 'RandomDelay', None),
                    'repetition': task_repetition,
                    'limit': getattr(n, 'ExecutionTimeLimit', None)
                })
          
        return task_info


    def exists(self):
        with self:
            try:
                return self.name in {n.Name for n in self._dir_handle.GetTasks(0)}
            except Exception: 
                return False


    def create(self):
        ...


    def delete(self):
        ...

    
    def mode(self):
        ...
    

    def enable(self):
        ...

    # И другие режимы
        
        
    def disable(self):
        ...


    def status(self):
        ...


    def start(self, args=''):
        invalid_type('args', args, {'str'})
            
    
    def stop(self):
        ...
    

    def __repr__(self):
        return f'Scheduler({repr(self.name)})' 