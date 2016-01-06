#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: BasicProcess.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/06 10:50:14
# Saying: Fight for freedom ^-^ !
#################################################################
import abc

class BasicProcess(object):
    """
    任务处理基类
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, task_info, conf, **kwargs):
        """
        init
        """
        pass
    
    @abc.abstractmethod
    def process(self, data):
        """
        主任务处理流程
        """
        pass

    def data_landed(self, data):
        """
        数据落地
        """
        pass

