import logging as Logging
import os, sys

log_file = 'script.log'

class ShutdownHandler(Logging.StreamHandler):
    # Will leave the application on critical log
    def emit(self, record):
        super(ShutdownHandler, self).emit(record)
        if record.levelno >= Logging.CRITICAL:
            sys.exit(1)

def create_logger(name: str, deletePreviousLog: bool = False):
    if deletePreviousLog:
        if os.path.isfile(log_file):
            os.remove(log_file)

    logging = Logging.getLogger(name)
    Logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s.%(funcName)s(%(lineno)d): %(message)s',
        handlers=[
            Logging.FileHandler(
                filename=log_file,
                encoding='utf-8',
                mode='a+'
            )
        ]
    )
    logging.setLevel(Logging.DEBUG)
    # create console handler and set level to debug
    ch = ShutdownHandler()
    ch.setLevel(Logging.INFO)
    # create formatter
    formatter = Logging.Formatter('%(asctime)s - %(levelname)s - %(name)s.%(funcName)s(%(lineno)d): %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logging.addHandler(ch)
    return logging
