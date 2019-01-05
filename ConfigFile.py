# coding=utf-8

# =========================================================================
# File Name  : ConfigFile 
# Author     : 刘戈峰
# Create Date: 2019-01-05
# platform   : Linux/Windows
# Comment    : 本脚本用于配置文件读写更新
# History    : 2019-01-05  基本功能开发完成
# =========================================================================

import configparser
import platform
import os

# =========================================================================
# 配置文件管理类
# =========================================================================
class ConfigFile:
    def __init__(self, fileName):
        self.file = fileName.strip()
        self.mParser = configparser.ConfigParser()
        self.readConfigInfo()

    # 读取配置文件所有配置信息
    def readConfigInfo(self):
        # 文件不存在, 则不进行读取
        if not os.path.exists(self.file):
            print("file " + self.file + " not exists!")
            return

        # 读取文件配置信息
        self.mParser.read(self.file)
        return

    # 读取配置文件指定option信息
    def readConfigItem(self, section, option):
        if not self.mParser:
            return ""

        if not self.mParser.has_option(section, option):
            print("property " + section + "->" + option + " not exists!")
            return ""

        return self.mParser.get(section, option)

    # 设置配置项信息
    def setConfigItem(self, section, key, value):
        if not section.strip():
            print("section is empty!")
            return

        if not key.strip():
            print("key is empty!")
            return

        if not value.strip():
            print("key is empty!")
            return

        if self.mParser.has_option(section, key):
            self.mParser.remove_option(section, key)
        else:
            self.mParser.add_section(section)

        self.mParser.set(section, key, value)
        fd = open(self.file, "w")
        self.mParser.write(fd)
        fd.close()
        return

if __name__ == "__main__":
    config = ConfigFile("./test.ini")

