#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: IOBasic.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/03 21:49:05
# Saying: Fight for freedom ^-^ !
#################################################################
import abc

class IOBasic(object):
    """
    所有数据io基类
    功能：支持数据库，数据流
    """
    __meta__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        """
        函数功能：
        """
        pass
    
    def init(self):
        """
        初始化
        """
        pass

    def finish(self):
        """
        释放数据
        """
        pass

    def __del__(self):
        """
        类析构函数
        """
        self.finish()
       

