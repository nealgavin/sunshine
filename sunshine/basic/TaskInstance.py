#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: TaskInstance.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/04 20:13:41
# Saying: Fight for freedom ^-^ !
#################################################################

import sys
import os
#path = os.path.dirname(os.path.abspath(__file__))
#sys.path += [path + "/../../module/"]
import importlib
import re
import hashlib

class TaskInstance(object):
    """
    一个process的托管，采用了委托的设计模式
    系统实际调度的是该类的实现，由该类决定如何调度用户的程序
    三个优点，方便任务流优化组合，方便平台调度管理。
    也实现了相关数据的解耦。
    """
    def __init__(self, conf, global_val_manager):
        """
        init
        """
        self.external_data = dict()
        self.name = conf["section_name"]
        class_name = conf["class_name"]
        self.input_flows = conf.get("input_flows", [])
        print conf ,"mygod"

        #实例化相关处理类
        task_info = global_val_manager.conf.get_section_dict("task_info")
        if class_name.startswith("sunshine."):
            module_path = class_name
        else:
            module_path = ".".join(["module", class_name])
        process_module = importlib.import_module(module_path)    
        class_name = class_name.split('.')[-1]
        process_class = getattr(process_module, class_name)
        process_instance = process_class(task_info, conf, io_conf=global_val_manager.io_conf )
        process_instance.init()
        
        #获取该步任务的并发数

        # 处理该模块所需要的输入输出
        self.global_val_manager = global_val_manager
        self.io_manager = global_val_manager.io_manager

        self.input_flows = conf.get("input_flows", [])
        input_name_list = conf.get("input", None)

        if input_name_list:
            pattern = re.compile(u'[,， ]')
            items = pattern.split(input_name_list)
            for item in items:
                input_name = item.strip()
                if input_name != "":
                    input_conf = self.global_val_manager.conf.get_section_dict(input_name)
                    if not input_name in self.io_manager.io_manager_dict:
                        register_result = self.io_manager.register(input_name, input_conf)

                        if register_result:
                            self.global_val_manager.log.info("input source %s register SUCC", input_name)
                        else:
                            self.global_val_manager.log.info("input source %s register failed", input_name)
                    
                    io_instance = self.io_manager.get_input_source(item)
                    if input_name not in self.input_flows:
                        self.external_data[input_name] = io_instance

        self.instance = process_instance                
        self.init_flag = True

    def run(self, data=None):
        """
        函数功能：运行具体任务的逻辑
        """
        self.run_task(data)
    
    def run_task(self, data):
        """
        一个task处理的真正执行函数
        stream_data: 上游数据，或是input_flows的数据
        一个处理过程的真正执行函数
        stream_data: 上游的数据，或者input_slot中的数据, 流式任务中就是Dstream中的rdd
        external_data: input中，且非input_slot中的db
        """
        print ("%s start running") % (self.name)

        if data is None:
            data = []
        elif not isinstance(data, list):
            data = [data]
        
        #加入输入流数据
        data.extend(self.input_flows)
        #获取输入数据
        stream_data = self.get_data_list(data)
        print "stream_data", stream_data
        external_data = self.get_data_list(self.external_data)

        #将多个输入源归并到一个输入
        data = []
        for elems in stream_data:
            if isinstance(elems, list):
                for elem in elems:
                    data.append(elem)
            else:
                data.append(elem)

        for elems in external_data:
            if isinstance(elems, list):
                for elem in elems:
                    data.append(elem)
            else:
                data.append(elem)
                

        # 执行任务
        result = self.instance.process(data)
        # 数据落地
        self.instance.data_landed(result)
        
        print ("%s running finish " % self.name)
        print data, "gavin input_ist"

        return result
       
    def get_data_list(self, input_list):
        """
        取列表中指定的数据源
        """
        data = []
        for input_name in input_list:
            #是stream_data, 输入源数据
            if isinstance(input_name, basestring):
                io_instance = self.io_manager.get_input_source(input_name)
            else:
                io_instance = input_name
            data.append(io_instance)    
        print data, "instance get_data_list"
        return  data




        
