#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: xxx.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/04 20:52:32
# Saying: Fight for freedom ^-^ !
#################################################################

import sunshine.module.BasicProcess as BasicProcess
class xxx(BasicProcess.BasicProcess):
    """

    """
    def __init__(self, task_info, conf, **kwargs):
        """

        """
        super(xxx, self).__init__(task_info, conf)
        print "xxx create yes"
        print task_info
        pass

    def init(self):
        """
        init
        """
        print "init"

    
    def process(self, data):
        """
        主处理流程
        """
        print data, "task data"

        return data

    def data_landed(self, data):
        """
        data_landed
        """
        pass
