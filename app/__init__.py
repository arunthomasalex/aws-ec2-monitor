import argparse
import os
import sys
from . import monitor

VERSION = "1.0.0"
parser = argparse.ArgumentParser(
                    prog = "aws-monitor",
                    description="Monitor ports and shutdown instance if no request received in the specified time frame.")
parser.add_argument('-s', '--src-port', type=int, default=None)
parser.add_argument('-d', '--dest-port', type=int, default=None)
parser.add_argument('-l', '--log', type=str, default= None)
parser.add_argument('-t', '--time', type=float, default=1.0)
parser.add_argument('-v', '--version', action="version", version=f'%(prog) {VERSION}')

def start():
    try:
        monitor.execute(dict(parser.parse_known_args(sys.argv)[0]._get_kwargs()))
    except KeyboardInterrupt:
        os._exit(0)

if __name__ == "__main__":
    start()