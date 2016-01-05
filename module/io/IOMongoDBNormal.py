#!/usr/bin/env python
# coding=utf-8
#################################################################
# File: IOMongoDBNormal.py
# Author: Neal Gavin
# Email: nealgavin@126.com
# Created Time: 2016/01/05 16:15:54
# Saying: Fight for freedom ^-^ !
#################################################################
import sys
import os
path = os.path.dirname(os.path.abspath(__file__))
sys.path += [path + "/../../"]

import sunshine.io.IOMongoDbInput as IOMongoDbInput
import json

class IOMongoDBNormal(IOMongoDbInput.IOMongoDbInput):
    """
    正常mogo读入
    """
    def __init__(self, conf):
        """
        conf
        """
        super(IOMongoDBNormal, self).__init__(conf)

    def build_query(self, query_text):
        """
        build_query
        """
        query_text = json.loads(query_text)
        return query_text
