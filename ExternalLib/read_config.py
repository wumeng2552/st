# -*- coding: utf-8 -*-
import os
# import pandas as pd
import configparser
import datetime
import codecs

# pd.set_option('display.width', 5000)
proDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(proDir, "config")
# test_data_path = os.path.join(proDir, "test_data")


class ReadConfig:
    def __init__(self):
        # self.path=config_path+file_name
        # self.conf = configparser.ConfigParser()
        self.conf = configparser.RawConfigParser()   # iniµÄÄÚÈÝÖÐ°üº¬ÁË%ºÅÕâÖÖÌØÊâ·ûºÅ
        # self.conf.read(self.path,encoding='utf-8')
        # self.conf.read(self.path)


    def read_ini_config(self, ini_file, connect_file_option):
        cn_config_path = config_path + "/" + ini_file
        self.conf.read(cn_config_path, encoding='utf-8')
        # option_name = moudl_name + '_' + option
        try:
            sections_value = {i[0]: i[1] for i in self.conf.items(connect_file_option)}
        except Exception as e:
            sections_value = None
        return sections_value

if __name__ == "__main__":
    r = ReadConfig()

