#!/usr/bin/python
# coding = utf-8

class Server():
    host = ''
    port = ''
    account = ''
    pwd = ''
    warpath = ''
    target = ''
    git = ''
    branch = ''
    types = ''
    env = ''

    def setHost(self, host):
        self.host = host

    def setPort(self, port):
        self.port = port

    def setAccount(self, account):
        self.account = account

    def setPwd(self, pwd):
        self.pwd = pwd

    def setWarpath(self, warpath):
        self.warpath = warpath

    def setTarget(self, target):
        self.target = target

    def setGit(self, git):
        self.git = git

    def setBranch(self, branch):
        self.branch = branch
    
    def setTypes(self, types):
        self.types = types

    def setEnv(self, env):
        self.env = env

    def getHost(self):
        return self.host
    
    def getPort(self):
        return self.port

    def getAccount(self):
        return self.account
    
    def getPwd(self):
        return self.pwd
    
    def getWarpath(self):
        return self.warpath

    def getTarget(self):
        return self.target
    
    def getBranch(self):
        return self.branch

    def getTypes(self):
        return self.types
    
    def getGit(self):
        return self.git

    def getEnv(self):
        return self.env
