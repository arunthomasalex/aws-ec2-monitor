import logging
from logging.handlers import RotatingFileHandler

def get_logger(name, file=None):
    logger = logging.getLogger(name)
    if file:

        handler = RotatingFileHandler(filename=file, mode='w', maxBytes=20*1024*1024, backupCount=10)
        handler.setFormatter(logging.Formatter(f'%(asctime)s - %(message)s'))
    else:
        handler = logging.NullHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

if __name__ == "__main__":
    logger = get_logger('test')
    logger.error("Hello World!")
