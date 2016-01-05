#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: IODBInput.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/03 22:49:36
# Saying: Fight for freedom ^-^ !
#################################################################

import IOBasic
class IODBInput(IOBasic.IOBasic):
    """
    数据库输入的基类
    """
    def __init__(self, conf):
        """
        初始化
        """
        super(IODBInput, self).__init__(conf)
        self.init()

    def init(self):
        """
        init
        """
        pass

    def connect(self):
        """
        连接数据库
        """
        pass

    def query(self, line):
        """
        请求数据库数据
        """
        pass

    def disconnect(self):
        """
        关闭数据库连接
        """
        pass

    def finish(self):
        """
        关闭数据库连接
        已经在基类中的__del__调用
        """
        pass

    def process(self):
        """
        数据处理主要流程
        """

    
if __name__ == '__main__':
    
    tt = IODBInput("gg")
    print tt.__class__
    print tt.__class__.__class__
