from ..sys._import import EmptyModule
from ..sys.value import TRACKER_SLEEP
from ..sys.tool import get_date
from ..sys.error import path_not_exist
from ..sys.pyoslibs import sleep, Queue, FileSystemEventHandler, Observer


if isinstance(FileSystemEventHandler, EmptyModule):
    FileSystemEventHandler = None


class Event(FileSystemEventHandler if FileSystemEventHandler else object):
    __slots__ = (
        'queue',
    )

    
    def __init__(self, queue):
        self.queue = queue


    def _put_event(self, event_type, src, dest=None):
        self.queue.put({
            'date': get_date(),
            'type': event_type,
            'src': src,
            'dest': dest
        })


    def on_created(self, event):
        self._put_event('created', event.src_path)


    def on_deleted(self, event):
        self._put_event('deleted', event.src_path)


    def on_modified(self, event):
        self._put_event('modified', event.src_path)


    def on_moved(self, event):
        self._put_event('moved', event.src_path, event.dest_path)
    

def tracker(path):
    path_not_exist(path)

    if FileSystemEventHandler is None:
        return None

    event_queue = Queue()

    try:
        event_handler = Event(event_queue)

        path_observer = Observer()
        path_observer.schedule(event_handler, path, recursive=True)
        path_observer.start()
    except Exception:
        return None

    try:
        while True:
            if not event_queue.empty():
                yield event_queue.get()
                
            sleep(TRACKER_SLEEP)
    except (Exception, KeyboardInterrupt): ...
    finally:
        path_observer.stop()
        path_observer.join()    