#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: Singleton.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/04 11:13:55
# Saying: Fight for freedom ^-^ !
#################################################################

import sys

class Singleton(type):
    """
    单例模式
    """
    def __call__(cls, *args, **kwargs):
        """
        call
        """
        if '_instance' not in vars(cls):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

def Test():
    class DemoSingleton(object):

        __metaclass__ = Singleton

        def __init__(self, indata):
            self.indata = indata
    
    x = DemoSingleton('x')
    y = DemoSingleton('y')
    print id(x), x, vars(x)
    print id(y), y, vars(y)

if '__main__' == __name__:
    ret = Test()
    sys.exit(ret)
