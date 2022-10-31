from threading import Thread
from . import scanner
from . import terminator

monitor_file = '/tmp/.monitor'

def execute(options):
    watcher = Thread(target=scanner.main, args=(monitor_file,options,))
    killer = Thread(target=terminator.terminate, args=(monitor_file, options['time'],))
    watcher.start()
    killer.start()
    watcher.join()