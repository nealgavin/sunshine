#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: IOManager.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/04 17:12:13
# Saying: Fight for freedom ^-^ !
#################################################################
import sys
import os
path = os.path.dirname(os.path.abspath(__file__))
sys.path += [path + '/../../']
import importlib
import sunshine.io.IODBInput as IODBInput

class IOManager(object):
    """
    IO管理类，负责管理框架的输入输出
    每一个输入源会在该类中进行注册
    """

    def __init__(self, global_val_manager):
        """
        fuction:
        """
        self.io_manager_dict = dict()
        self.global_val_manager = global_val_manager

    def register(self, name, db_conf):
        """
        注册数据源，会根据配置自动的加载相关的类库实现
        """
        #处理数据源的class
        class_name = db_conf.get("db_class", None)

        if class_name:
            if class_name.startswith('sunshine'):
                module_path = class_name
            else:
                module_path = ".".join(["module", "io", class_name])

            io_module = importlib.import_module(module_path)    
            class_name = class_name.split('.')[-1]
            io_class = getattr(io_module, class_name)

            db_source = db_conf.get("db_source")

            io_instance = io_class(db_conf)
            self.io_manager_dict[name] = io_instance
            return True
        else:
            return False
        

