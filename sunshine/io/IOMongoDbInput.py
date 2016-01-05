#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: IOMongoDbInput.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/05 15:02:03
# Saying: Fight for freedom ^-^ !
#################################################################
import sys
import os
path = os.path.dirname(os.path.abspath(__file__))
sys.path += [path + "/../../"]

import pymongo
import sunshine.io.IODBInput as IODBInput

import abc
import time
import collections

class IOMongoDbInput(IODBInput.IODBInput):
    """
    class for mongodb
    """
    def __init__(self, conf):
        """
        根据配置初始化数据库信息
        """
        super(IOMongoDbInput, self).__init__(conf)
        #load db conf
        self.db_uri = conf["db_uri"]
        self.db_name = conf["db_name"]
        self.col_name = conf["col_name"]
        self.db_client = None
        self.query_text = conf["query"]
        print "IOMongoDbInput:", self.db_uri, self.db_name, self.col_name
        self.process()
    
    def connect(self):
        """
        连接数据库
        """
        try:
            self.db_client = pymongo.MongoClient(self.db_uri)
        except (pymongo.errors.ConnectionFailure, TypeError):
            return None

        db = self.db_client[self.db_name]
        col = db[self.col_name]
        
        return col
    
    @abc.abstractmethod
    def build_query(self, query_text):
        """
        build_query
        """
        return query_text
        
    
    def formart_data(self, indata):
        """
        格式化数据
        """
        return indata

    def process(self):
        """
        整个处理流程入口
        """
        data = []
        conn = self.connect()
        query_text = self.build_query(self.query_text)
        data = self.query(conn, query_text)
        print data
        return data

    def query(self, conn, query_text):
        """
        query
        """
        out_data = []
        if isinstance(query_text, list):
            for item in query_text:
                res = conn.find(item)
                for res_item in res:
                    data = self.formart_data(res_item)
                    if data:
                        out_data.append(data)
        else:
            res = conn.find(query_text)
            for res_item in res:
                print res_item
                data = self.formart_data(res_item)
                if data:
                    out_data.append(data)
        return out_data            


    def finish(self):
        """
        关闭数据    
        """
        if self.db_client != None:
            self.db_client.close()
