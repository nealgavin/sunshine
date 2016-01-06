#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: LogModule.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/04 11:08:00
# Saying: Fight for freedom ^-^ !
#################################################################
import os
import sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path += [path + '/../../../sunshine/']
import logging
import logging.handlers
import sunshine.lib.Singleton as Singleton

class LoggingModule(object):
    """
    log模块封装，警告和错误打到.wf, 其它打入.log
    """

    __metaclass__ = Singleton.Singleton


    def __init__(self):
        self.logger = logging.getLogger()
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical

    def init_log(self, log_path, level=logging.INFO, when="D", backup=7,
                 format="[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] * [%(process)d][%(thread)d]: %(message)s",
                 datefmt="%m-%d %H:%M:%S"):
        """
        init_log - initialize log module

        Args:
        log_path      - Log file path prefix.
                        Log data will go to two files: log_path.log and log_path.log.wf
                        Any non-exist parent directories will be created automatically
        level         - msg above the level will be displayed
                        DEBUG < INFO < WARNING < ERROR < CRITICAL
                       the default value is logging.INFO
        when          - how to split the log file by time interval
                        'S' : Seconds
                        'M' : Minutes
                        'H' : Hours
                        'D' : Days
                        'W' : Week day
                        default value: 'D'
        format        - format of the log
                        default format:
                        %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                        INFO: 12-09 18:02:42: logging_module.py:40 * 139814749787872 HELLO WORLD
        backup        - how many backup file to keep
                        default value: 7

        Raises:
            OSError: fail to create log directories
            IOError: fail to open log file
        """
        formatter = logging.Formatter(format, datefmt)

        self.logger.setLevel(level)

        dir = os.path.dirname(log_path)
        if not os.path.isdir(dir):
            os.makedirs(dir)

        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
                                                            when=when,
                                                            backupCount=backup)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf",
                                                            when=when,
                                                            backupCount=backup)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


if '__main__' == __name__:
    tt = LoggingModule()
    tt.init_log('./tt')
    tt.info('testinfo')
    tt.warning('testinfo')

