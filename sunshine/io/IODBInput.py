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
    数据库输入的基数
    """
    def __init__(self):
        """
        初始化
        """
        super(IODBInput, self).__init__()
        pass
    

if __name__ == '__main__':
    tt = IODBInput()
    print tt.__class__
    print tt.__class__.__class__
