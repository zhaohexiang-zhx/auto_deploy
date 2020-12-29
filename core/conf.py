#!/usr/bin/python
# coding = utf-8
import configparser
import os, sys

'''
数据初始化
读取配置文件
'''

class Conf():
    sections = {}
    confPath = ''
    file = None
    def __init__(self):
        # 获取绝对路径 需复制到dist/main/conf/目录内
        self.confPath = os.path.abspath(os.path.join(os.getcwd(), 'conf', 'hkad.ini'))
        self.file = configparser.RawConfigParser()
        self.file.read(self.confPath, encoding="utf-8-sig")
    # 配置文件初始化
    def init(self):
        print('HKAD-读取配置文件开始')
        # 获取默认
        # defaults = self.file.defaults()
        # 读取所有的section
        sections = self.file.sections()
        for s in sections:
            options = self.file.options(s)
            params = {}
            for op in options:
                val = self.file.get(s, op)
                params[op] = val
            self.sections[s] = params
        print('HKAD-读取配置文件结束')

    # 写入配置文件
    def write(self, server, name):
        try:
            print('HKAD-写入配置文件开始')
            section = 'server-' + name
            # host
            self.file.set(section, 'host', server.getHost())
            # port
            self.file.set(section, 'port', server.getPort())
            # account
            self.file.set(section, 'account', server.getAccount())
            # pwd
            self.file.set(section, 'pwd', server.getPwd())
            # target
            self.file.set(section, 'target', server.getTarget())
            # git
            self.file.set(section, 'git', server.getGit())
            # branch
            self.file.set(section, 'branch', server.getBranch())
            # type
            self.file.set(section, 'type', server.getTypes())
            # 写入
            self.file.write(open(self.confPath, "w", encoding = 'utf-8-sig'))
            print('HKAD-写入配置文件结束')
        except Exception as e:
            print(e)
            return False
        else:
            return True