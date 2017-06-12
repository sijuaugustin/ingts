'''
Created on Oct 7, 2016

@author: joseph
'''
import logging
import os


class NoLoggerFound(Exception):
    pass


class BaseLoggerFactory:
    logpath = None
    logger_names = []
    level = logging.INFO

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    def __init__(self, console=True):
        logger_args = {'level': self.level,
                       'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                       'datefmt': '%m-%d %H:%M'}
        if self.logpath is not None:
            logging_directory = os.path.dirname(self.logpath)
            if not os.path.exists(logging_directory):
                os.makedirs(logging_directory)
            logger_args.update({'filename': self.logpath,
                                'filemode': 'w'})
        logging.basicConfig(**logger_args)
        if console:
            h_console = logging.StreamHandler()
            h_console.setLevel(self.level)
            formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
            h_console.setFormatter(formatter)
            logging.getLogger('').addHandler(h_console)

    def get_every_logger(self):
        return [logging.getLogger(logger_name) for logger_name in self.logger_names]

    def get_logger(self, name):
        if name in self.logger_names:
            return logging.getLogger(name)
        else:
            raise NoLoggerFound()

if __name__ == "__main__":
    from cognub.logging import BaseLoggerFactory

    class iPriceLoggerFactory(BaseLoggerFactory):
        logpath = "/tmp/cognub/iprice/trend.log"
        logger_names = ["Main"]
        level = BaseLoggerFactory.DEBUG

    logger = iPriceLoggerFactory().get_logger("Main")
    logger.debug("Sample")
