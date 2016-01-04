#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: maintask.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/04 13:47:07
# Saying: Fight for freedom ^-^ !
#################################################################
import sys
import traceback
import copy
import importlib
import sunshine.basic.ModConfig as ModConfig
import sunshine.basic.LogModule as LogModule
import sunshine.basic.GlobalValue as GlobalValue
import sunshine.io.IOManager as IOManager
import sunshine.basic.TaskInstance as TaskInstance

def load_config(conf_path):
    """
    导入task-conf
    """
    mod_config = ModConfig.ModConfig()
    mod_config.read(conf_path)
    return mod_config

def init_task_context(global_val_manager, conf, debug):
    """
    初始化任务上下文环境
    """
    #日志名获取
    try:
        log_file_name = conf.get("task_info", "log_name")
    except:
        log_file_name = "framework"
    
    #获取log配置
    log_module = LogModule.LoggingModule()
    log_module.init_log("./log/" + log_file_name)
    global_val_manager.add_attr("log", log_module)
    
    #获取配置任务名
    task_name = conf.get("task_info", "task_name")
    global_val_manager.add_attr("task_name", task_name)

    global_val_manager.add_attr("conf", conf)

    #获取数据库配置相关
    try:
        db_conf_file = conf.get("task_info", "io_conf_path")
    except:
        db_conf_file = "./conf/io/io.ini"

    io_conf = ModConfig.ModConfig()   
    io_conf.read(db_conf_file)

    io_dict = dict()
    for section in io_conf.sections():
        io_dict[section] = io_conf.get_section_dict(section)
    global_val_manager.add_attr("io_conf", io_dict)    

    log_module.info("Application start with conf %s", sys.argv[1])

    return 0

def load_task_conf(global_val_manager):
    """
    加载任务信息
    """
    conf = global_val_manager.conf
    task_info_conf = conf.options('task_info')
    multi_way_dict = {}
    process_way_dict = {}
    #多路向下信息
    global_val_manager.add_attr("multi_way_dict", multi_way_dict)
    #process向下信息
    global_val_manager.add_attr("process_way_dict", process_way_dict)

    #多路配置
    if "muti_way" in task_info_conf:
        multi_way_list = conf.get_conf_list("task_info", "muti_way")
        print multi_way_list
        for item in multi_way_list:
            load_process_conf(global_val_manager, item, item)

    return 0

def load_process_conf(global_val_manager, multi_item, section_name):
    """
    加载多路流中每个流的配置
    """
    conf = global_val_manager.conf
    process_info_list = dict()
    #多路的下一层的流
    process_list = conf.get_conf_list(section_name, "process_list")
    input_flows = conf.get_conf_list(section_name, "input_flows")
    
    process_info_list["process_list"] = process_list
    process_info_list["input_flows"] = input_flows
    
    #保存多路的关系
    global_val_manager.multi_way_dict[multi_item] = process_info_list
    
    #具体的方法调用依据
    for process_item in process_list:
        process_info = {}
        process_info["process_list_name"] = multi_item
        if process_item == process_list[-1]:
            process_info['is_last'] = 1
        else:
            process_info['is_last'] = 0
        global_val_manager.process_way_dict[process_item] = process_info    

    return 0    

def load_input_flows(global_val_manager):
    """
    加载数据源信息
    """
    conf = global_val_manager.conf

    io_manager =  IOManager.IOManager(global_val_manager)
    global_val_manager.add_attr("io_manager", io_manager)
    return 0
    
def get_dependency(global_val_manager):
    """
    获取任务间的依赖关系
    """
    #获取最终的执行序列
    final_sequence = []

    multi_way_dict = global_val_manager.multi_way_dict
    process_way_dict = global_val_manager.process_way_dict
    conf = global_val_manager.conf
    for process_list_name, process_list_info in multi_way_dict.iteritems():
        final_sequence.append(process_list_name)
    global_val_manager.add_attr("final_sequence", final_sequence)    
    return 0

def check_validate(global_val_manager):
    """
    检查配置语法合理性
    """
    multi_way_dict = global_val_manager.multi_way_dict
    final_sequence = global_val_manager.final_sequence

    if len(multi_way_dict) != len(final_sequence):
        print "process list configure error!"
        return 1
    return 0
    
def init_process_circuit(global_val_manager):
    """
    根据配置信息初始化任务处理流程
    """
    multi_way_dict = global_val_manager.multi_way_dict
    conf = global_val_manager.conf
    log = global_val_manager.log

    for process_list_name, process_info_list in multi_way_dict.iteritems():
        process_flows = list()
        process_items = process_info_list['process_list']
        for item in process_items:
            item = item.strip()
            conf_item = conf.get_section_dict(item)

            data_task = TaskInstance.TaskInstance(conf_item, global_val_manager)
            if not data_task.init_flag:
                log.error("init process circuit failed, return")
                return 1
            process_flows.append(data_task)
        multi_way_dict[process_list_name]["process_flows"] = process_flows        

    return 0    
    
def running_task(global_val_manager):
    """
    执行任务
    """
    pass

def finish_task(global_val_manager):
    """
    结束任务
    """
    pass

def main(conf_path, debug = False):
    """
    主流程控制
    conf_path:配置文件路
    """
    try:
        conf = load_config(conf_path)
        #初始化全局变量环境
        global_val_manager = GlobalValue.GlobalValueManage()

        #根据配初始化任务环境
        if 0 != init_task_context(global_val_manager, conf, debug):
            print 'init_task_context fail return !'
            return -1
        global_val_manager.log.info("init_task_context SUCC")

        #加载任务信息
        if 0 != load_task_conf(global_val_manager):
            print 'load_task_conf fail return !'
            return -1
        global_val_manager.log.info("load_task_conf SUCC")
        try:
            #加载数据源信息，并在io中注册
            if 0 != load_input_flows(global_val_manager):
                print "load_input_flows failed return !"
                return -1
            global_val_manager.log.info("load_input_flows SUCC")

            #获取依赖关系
            if 0 != get_dependency(global_val_manager):
                print "get_dependency failed return !"
                return -1
            global_val_manager.log.info("get_dependency SUCC")

            #检查配置语法合理性
            if 0 !=  check_validate(global_val_manager):
                print "check_validate failed return !"
                return -1

            #根据配置信息初始化任务处理流程
            if 0 != init_process_circuit(global_val_manager):
                print "init_process_circuit failed return !"
                return -1
            
            #运行任务
            if 0 != running_task(global_val_manager):
                print "running_task error return !"
                return -1

            #任务结束触发
            if 0 != finish_task(global_val_manager):
                print "finish_task failed"
                return -1

        finally:
            global_val_manager.log.info("task finish")
    except BaseException as e:
        global_val_manager.log.error("Application terminate by exception: {0}".format(e))
        traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])

if '__main__' == __name__:

    if len(sys.argv) == 3 and sys.argv[2] == "debug":
        debug_flag = True
    else:
        debug_flag = False
    if len(sys.argv) < 2:
        conf_path = "./conf/gaia-platform.ini"
    else:
        conf_path = sys.argv[1]
    main(conf_path, debug=debug_flag)

