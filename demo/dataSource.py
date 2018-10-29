#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import json
class DataSource(object):
    def __init__(self):
        pass

    def processData(self,list):
        reslut = json.dumps(list)


    # def get__dataTime(self):
    #     return self.__dataTime
    #
    # def get__number(self):
    #     return self.__number
    #
    # def get__type(self):
    #     return self.__type

    # def get__string(self):
    #     return '{'+'dataTime:'+str(self.__dataTime)+','+'number:'+str(self.__number)+','+'type:'+str(self.__type)+'}'