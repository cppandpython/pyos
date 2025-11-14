from ..sys.error import no_interface
from ..sys.pyoslibs import asyncio, Thread, Queue, BleakScanner, BleakError


async def discover_bluetooth():
    devices = await BleakScanner.discover()

    return [{
        'name': getattr(n, 'name', None),
        'mac': getattr(n, 'address', None)
    } for n in devices]


def bluetooth_thread(queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        device = loop.run_until_complete(discover_bluetooth())
    except BleakError:
        device = 'no interface'
    except Exception:
        device = None
    
    queue.put(device)


def bluetooth():
    queue = Queue()

    queue_thread = Thread(target=bluetooth_thread, args=(queue,))
    queue_thread.start()
    queue_thread.join()  
    
    bluetooth_result = queue.get()

    no_interface(bluetooth_result == 'no interface')
    
    return bluetooth_result if bluetooth_result else None