#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: GlobalValue.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/03 23:02:24
# Saying: Fight for freedom ^-^ !
#################################################################
import multiprocessing

class GlobalValue(object):
    """
    存放所有的全局变量
    """
    def __init__(self):
        """
        变量创建
        """
        self.val_dict = dict()

    def get(self, key):
        """
        获取KV值
        """
        return self.val_dict.get(key, None)

    def set(self, key, value, force = False):
        """
        写入全局KV值
        @return:
        2:变量已经存在,已经强制写入，覆盖
        1:变量已经存在，不写入
        0:正常写入
        """
        if key in self.val_dict:
            if force:
                self.val_dict[key] = value
                return 2
            else:
                return 1
        else:
            self.val_dict[key] = value
            return 0


if '__main__' == __name__:
    tt = GlobalValue()
    print tt.set('a', 'c')
    print tt.get('a')
    print tt.get('b')
