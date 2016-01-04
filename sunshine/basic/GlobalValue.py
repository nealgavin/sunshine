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

class GlobalValueManage(object):
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

    def add_attr(self, name, value):
        """
        增加名为name的属性
        """
        self.__setattr__(name, value)

    def del_by_key(self, key):
        """
        去除全局变量管理中的一个key值
        :param key: 索引字段
        :param value: 对应的值
        :return: 返回删除键对应的值
        """
        return self.val_dict.pop(key)

if '__main__' == __name__:
    tt = GlobalValueManage()
    print tt.set('a', 'c')
    print tt.get('a')
    print tt.get('b')
    print tt.del_by_key('help')
