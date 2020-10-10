#!/usr/bin/env python3

import logging
import configparser

class Logger():
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read('logger.conf')
        self._FORMAT = "%(asctime)-15s %(levelname)s:%(funcName)-8s %(message)s"
        self._FILE = 'server.log'
        self._LEVEL = logging.INFO
        logging.basicConfig(filename=self._FILE, filemode='a',
                            format=self._FORMAT, level=self._LEVEL)
        
    def info(self, message):
        logging.info(message)
    
    def error(self, message):
        logging.error(message)
    
    def warn(self, message):
        logging.warn(message)
    
    def debug(self, message):
        logging.debug(message)
    
    def log(self, msg):
        self.info(msg)
