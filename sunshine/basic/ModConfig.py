#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: ModConfig.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/04 12:04:39
# Saying: Fight for freedom ^-^ !
#################################################################

import ConfigParser
import re
import sys
import os
try:
    from collections import OrderedDict as _default_dict
except:
    # fallback for setup.py which hasn't yet built _collections
    _default_dict = dict

class ConfigReader:
    def __init__(self, filenames):
        """
        初始化文件列表并打开文件
        """
        if isinstance(filenames, str):
            self.filenames = [filenames]
        else:
            self.filenames = filenames
        self.fp_index = 0
        self.fp = self.open()
        self.pre_section = []

    def open(self):
        """
        打开一个文件
        :return
            如果文件存在返回 File Object
            如果文件不存在，尝试打开下一个文件
            如果没有可打开的文件，返回None
        """
        while (self.fp_index < len(self.filenames)):
            if (os.path.exists(self.filenames[self.fp_index])):
                return open(self.filenames[self.fp_index])
            self.fp_index += 1
        return None

    def readline(self):
        """
        读取文件中的下一行，并补齐section的相对层级关系
        :return
            文件中的下一行
            如果文件结束，尝试打开下一个文件
        """
        if self.fp is None:
            return ''

        while (self.fp is not None):
            line = self.fp.readline()
            if len(line) == 0:
                self.fp_index += 1
                self.fp.close()
                self.fp = self.open()
            else:
                break

        return self.parse_hierarchy(line)

    def parse_hierarchy(self, line):
        """
        补齐section_name的层次信息，将相对层次"."替换为绝对层次
        """
        m = re.match('\[(.*)\]', line.strip())
        if m is not None:
            section = m.group(1)
            # 替换相对层次
            if section.startswith('.'):
                # 计算绝对层次
                i = len(section) - len(section.lstrip('.'))
                if i > len(self.pre_section):
                    print >> sys.stderr, "Config Error: missing hierarchy for [%s]" % (section)
                    sys.exit(1)
                _section = '.'.join(self.pre_section[0:i]) + '.' + section[i:]

                # section出栈
                self.pre_section = self.pre_section[0:i]

                line = line.replace(section, _section)

                # 当前section入栈
                self.pre_section.append(section[i:])
            # 绝对层次
            else:
                self.pre_section = section.split('.')
        return line

class SampleConfig(ConfigParser.ConfigParser):
    def __init__(self, defaults=None, dict_type=_default_dict, allow_no_value=False):
        ConfigParser.ConfigParser.__init__(self, defaults, dict_type, allow_no_value)

    def get_default(self, section, key, default_value):
        """
        获取配置项中section部分key=key的值，如果获取不成功返回default_value，
        :param section: 配置中section值
        :param key: section中的key
        :param default_value: 如果获取不成功返回的default_value
        :return: 返回值或是default_value
        """
        try:
            config_value = self.get(section, key)
        except ConfigParser.Error:
            config_value = default_value
        return config_value

    def get_boolean_default(self, section, option, default_value):
        """
        获取配置项中section部分key=key的bool值，如果获取出错返回bool(default_value)值
        :param section:
        :param option:
        :param default_value:
        :return:配置中的bool值, 当获取失败返回default_value，
        :raise:
        或是获取失败后无法将default value转化为float值会raise ValueError
        """
        try:
            config_value = self.getboolean(section, option)
        except ConfigParser.Error:
            config_value = bool(default_value)
        return config_value

    def get_float_default(self, section, option, default_value):
        """
        获取配置项中section部分key=key的bool值，如果获取出错返回float(default_value)值
        :param section:
        :param option:
        :param default_value:
        :return: 获取配置中的float值，当获取失败时返回default_value
        :raise:当配置中的值不为float，
        或是获取失败后无法将defaultvalue转化为floas值会raise ValueError
        """
        try:
            config_value = self.getfloat(section, option)
        except ConfigParser.Error:
            config_value = float(default_value)
        return config_value

    def get_int_default(self, section, option, default_value):
        """
        获取配置项中section部分key=key的int值，如果获取出错返回int(default_value)值
        :param section:
        :param option:
        :param default_value:
        :return: 配置中的int值，当获取失败时返回default_value
        :raise:当配置中的值无法转化为int时
        或是获取失败后无法获取int(default_value)值会raise ValueError
        
        """
        try:
            config_value = self.getint(section, option)
        except ConfigParser.Error:
            config_value = int(default_value)
        return config_value

    def get_section_dict(self, section):
        """
        直接获取某个section_dict配置
        :param section:
        :return:
        """
        _config = dict()
        try:
            section_config = self.items(section)
            for item in section_config:
                if len(item) == 2:
                    _config[item[0]] = item[1]
            _config['section_name'] = section
        except ConfigParser.NoOptionError:
            pass
        return _config

    def get_conf_list(self, section, option):
        """
        获取一个配置项中配置，返回以一个list方式返回
        """
        _config = list()
        try:
            config = self.get(section, option)
        except ConfigParser.NoOptionError:
            return _config
        pattern = re.compile(u'[,， ]')
        items = pattern.split(config)
        for item in items:
            if item.strip() != "":
                _config.append(item.strip())
        return _config
                                        
class ModConfig(SampleConfig):
    """
    封装的配置函数解析类，解析配置文件
    """
    def __init__(self, defaults=None, dict_type=_default_dict, allow_no_value=False):
        SampleConfig.__init__(self, defaults, dict_type, allow_no_value)
        self.optionxform = str

    def _process_ref(self):
        """
        处理引用关系，引用表示方法有两种：
        &ref = section_name 表示当前section引用目标section的内容，不覆盖现有option
        option = &section_name 表示option引用目标section内容，option的值变为一个dict类型
        """
        for section in self.sections():
            for key, value in self.items(section):
                # &ref = section_name
                if key == '&ref':
                    if not self.has_section(value):
                        print >> sys.stderr, "Config Error: ref section not found [%s]" % (value)
                        sys.exit(1)
                    self.remove_option(section, key)
                    for tk, tv in self.items(value):
                        if not self.has_option(section, tk):
                            self.set(section, tk, tv)

                # option = &section_name
                elif isinstance(value, basestring) and value.startswith('&'):
                    value = value[1:]
                    if not self.has_section(value):
                        print >> sys.stderr, "Config Error: ref section not found [%s]" % (value)
                        sys.exit(1)
                    self.set(section, key, self.get_section_dict(value))

    def _process_dict(self, update=False):
        """
        根据层次关系拼装dict
        :update 是否提换重复的section及子section
        """
        for section in self.sections():
            arr = section.split('.')
            if len(arr) == 1:
                continue
            if len(arr) == 2:
                # put top level dict
                if self.has_option(arr[0], arr[1]) and update == False:
                    print >> sys.stderr, "Config Error: duplicate sub section [%s]" % (arr[1])
                    sys.exit(1)
                else:
                    self.set(arr[0], arr[1], self.get_section_dict(section))

            elif len(arr) > 2:
                # put into top level dict
                if self.has_option(arr[0], arr[1]):
                    conf_dict = self.get(arr[0], arr[1])
                    for name in arr[2:-1]:
                        if name not in conf_dict:
                            print >> sys.stderr, "Config Error: missing parent for [%s]" % (name)
                            sys.exit(1)
                        conf_dict = conf_dict[name]
                    if arr[-1] in conf_dict and update == False:
                        print >> sys.stderr, "Config Error: duplicate sub dict [%s]" % (arr[-1])
                        sys.exit(1)
                    conf_dict[arr[-1]] = self.get_section_dict(section)

                # put into parent dict
                # _section = '.'.join(arr[0:-1])
                # if self.has_section(_section):
                #     self.set(_section, arr[-1], self.get_section_dict(section))
            self.remove_section(section)

    def copy(self, conf):
        """
        复制另一个ModConfig的配置
        :conf ModConfig实例
        """
        for section in conf.sections():
            if self.has_section(section):
                print >> sys.stderr, "Config Error: duplicate section [%s]" % (section)
                sys.exit(1)
            self.add_section(section)
            for key, value in conf.items(section):
                self.set(section, key, value)

    def _read_inner(self, filenames, include_depth=1):
        """
        内部读取配置文件，不处理引用和拼装dict
        :filenames 文件名list
        :include_depth 文件读取深度，默认为1，仅读取当前文件的引用文件
        """
        reader = ConfigReader(filenames)
        ConfigParser.ConfigParser.readfp(self, reader)

    def read(self, filenames, include_depth=1):
        """
        读取配置文件
        :filenames 文件名list
        :include_depth 文件读取深度，默认为1，仅读取当前文件的引用文件
        """
        conf = ModConfig()
        conf._read_inner(filenames, include_depth)
        self.copy(conf)

        if include_depth > 0 and self.has_section('include'):
            include_path = self.get_default('include', 'include_path', './conf') + '/'
            for include_file in self.get_conf_list('include', 'include_file_list'):
                conf = ModConfig()
                conf._read_inner([include_file, include_path + include_file], include_depth - 1)
                self.copy(conf)

        self._process_ref()
        self._process_dict()

    def __str__(self):
        """
        打印配置处理的结果
        """
        import json
        buf = ''
        for section in self.sections():
            buf += "\n[" + section + "]\n"
            for key, value in self.items(section):
                if isinstance(value, str):
                    buf += "  " + key + " : " + value + "\n"
                else:
                    buf += "  " + key + " => " + json.dumps(value, indent=4) + "\n"
        return buf
