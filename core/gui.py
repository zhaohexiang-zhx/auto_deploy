#!/usr/bin/python
# coding = utf-8
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mbox
import os, sys
from core.deploy import Deploy
from bean.server import Server
from core.conf import Conf

'''
页面UI
页面相关处理
'''
class GUI():
    # 服务器
    servers = {}
    # 下拉列表
    cbbComp = ''
    # IP
    hostComp = ''
    # port
    portComp = ''
    # 账号
    accountComp = ''
    # 密码
    pwdComp = ''
    # 路径
    targetComp = ''
    # git地址
    gitComp = ''
    # 分支
    branchComp = ''
    # 类型
    typeComp = 1
    # 暂无服务
    noServer = '暂无服务'
    # 提示框提示
    mbtitle = '温馨提示'
    # 缓存路径
    cachepath = ''
    # copyright
    copyRight = 'CopyRight @ 海看研发中心-轻快项目部'

    def __init__(self, server):
        self.servers = server
        # 获取系统设置3
        setting = server['sys-setting']
        # 标题
        self.mbtitle = setting['title']
        # 缓存路径
        self.cachepath = setting['cachepath']
        # 缓存路径判断
        self.setCachePath(self.cachepath)
        # 初始化
        self.init()
        # 处理缓存目录问题

    # 弹框
    def init(self):
        # 弹框
        root = tk.Tk()
        sys = self.servers['sys-setting']
        # 图标
        ico = os.path.abspath(os.path.join(os.getcwd(), 'conf','favicon.ico'))
        root.iconbitmap(ico)
        # 标题
        root.title(sys['title'])
        # 尺寸
        width = int(sys['width'])
        height = int(sys['height'])
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        lignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2 - 40)
        # 设置尺寸+位置
        root.geometry(lignstr)
        # 禁止用户拖动
        root.resizable(0,0)

        frame = tk.Frame(root).place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        # 置顶
        # root.wm_attributes('-topmost',1)
        tk.Label(frame, text = sys['title'], font = ("微软雅黑", 24)).pack(ipady = 35)

        # 服务器
        tk.Label(frame, text = "服务器：").place(x = 60, y = 100, width = 80, height = 60)
        # 下拉列表
        self.cbbComp = ttk.Combobox(root, width = 12, textvariable = self.noServer)
        self.cbbComp['values'] = self.getServers()
        self.cbbComp.place(x = 150, y = 120, width = 300)
        # 默认选中第一个
        self.cbbComp.current(0)
        # 切换下拉列表
        self.cbbComp.bind("<<ComboboxSelected>>",lambda _ : self.comboxListen())
       
        # IP
        tk.Label(frame, text = "　   IP：").place(x = 60, y = 150, width = 80, height = 60)
        self.hostComp = tk.StringVar()
        tk.Entry(frame, width = 28, textvariable = self.hostComp,  relief = 'flat', highlightcolor = 'blue', highlightthickness = 1).place(x = 150, y = 170)
        self.portComp = tk.StringVar()
        tk.Entry(frame, width = 12, textvariable = self.portComp,  relief = 'flat', highlightcolor = 'blue', highlightthickness = 1).place(x = 360, y = 170)

        # 账号
        tk.Label(frame, text = "账　号：").place(x = 60, y = 200, width = 80, height = 60)
        self.accountComp = tk.StringVar()
        tk.Entry(frame, width = 28, textvariable = self.accountComp,  relief = 'flat', highlightcolor = 'blue', highlightthickness = 1).place(x = 150, y = 220)
        # 密码
        tk.Label(frame, text = "密　码：").place(x = 60, y = 250, width = 80, height = 60)
        self.pwdComp = tk.StringVar()
        tk.Entry(frame, width = 28, textvariable = self.pwdComp, show="*", relief = 'flat', highlightcolor = 'blue', highlightthickness = 1).place(x = 150, y = 270)

        # 路径
        tk.Label(frame, text = "路　径：").place(x = 60, y = 300, width = 80, height = 60)
        self.targetComp = tk.StringVar()
        tk.Entry(frame, width = 82, textvariable = self.targetComp,  relief = 'flat', highlightcolor = 'blue', highlightthickness = 1).place(x = 150, y = 320)

        # Git地址
        tk.Label(frame, text = "　  Git：").place(x = 60, y = 350, width = 80, height = 60)
        self.gitComp = tk.StringVar()
        tk.Entry(frame, width = 68, textvariable = self.gitComp,  relief = 'flat', highlightcolor = 'blue', highlightthickness = 1).place(x = 150, y = 370)
        # 分支
        self.branchComp = tk.StringVar()
        tk.Entry(frame, width = 12, textvariable = self.branchComp,  relief = 'flat', highlightcolor = 'blue', highlightthickness = 1).place(x = 640, y = 370)

        # 类型
        tk.Label(frame, text = "类　型：").place(x = 60, y = 400, width = 80, height = 60)
        # 定义变量
        self.typeComp = tk.IntVar()
        tk.Radiobutton(frame, text = "Vue工程", value = 1, variable = self.typeComp, bd = 0).place(x = 150, y = 420)
        tk.Radiobutton(frame, text = "JAVA工程", value = 2, variable = self.typeComp, bd = 0).place(x = 300, y = 420)

        # 处理下拉框选中
        self.comboxListen()

        # 确定
        tk.Button(frame, text = "确定", command = self.sub, bd = 0, cursor = 'hand2', bg = 'blue', fg = 'white').place(x = 450,y = 480, width = 80, height = 30)
        # 保存
        tk.Button(frame, text = "保存", command = self.save, bd = 0, cursor = 'hand2', bg = 'gray', fg = 'white').place(x = 550,y = 480, width = 80, height = 30)
        # 退出登录
        tk.Button(frame, text = "退出", command = self.exit, bd = 0, bg = 'white', cursor = 'hand2').place(x = 650,y = 480, width = 80, height = 30)

        tk.Label(frame, text = self.copyRight, font = ("微软雅黑", 8), fg = 'gray').pack(side = 'bottom', ipady = 20)
        root.mainloop()

    # 获取服务
    def getServers(self):
        serLen = len(self.servers.keys())
        if serLen < 1:
            return (self.noServer)
        sers = []
        for key in self.servers.keys():
            if key.startswith('server-'):
                sers.append(key.replace('server-', ''))
        if len(sers) < 1:
            sers = (self.noServer)
        return sers
    
    # 下拉列表监听
    def comboxListen(self):
        # 获取已选择
        name = self.cbbComp.get()
        if name == self.noServer:
            return
        obj = self.servers['server-' + name]
       
        # 设置显示在输入框内
        # IP
        self.hostComp.set(obj['host'])
        # port
        self.portComp.set(obj['port'])
        # 账号
        self.accountComp.set(obj['account'])
        # 密码
        self.pwdComp.set(obj['pwd'])
        # 路径
        self.targetComp.set(obj['target'])
        # git
        self.gitComp.set(obj['git'])
        # 分支
        self.branchComp.set(obj['branch'])
        # 类型
        self.typeComp.set(obj['type'])
    
    # 点击确定
    def sub(self):

        name = self.cbbComp.get()
        print(name, '----------------------------')
        print(name, '->', '工程开始处理')
        obj = self.servers['server-' + name]
        # 输入验证
        server = self.checkInput()
        if not server:
            print(name, '->', '参数校验有误，结束处理')
            return

        # 环境判断
        if 'env' not in obj.keys():
            print(name, '->', '未配置环境标识[env]，结束处理')
            mbox.showerror(self.mbtitle, '请配置环境标识[env]')
            return
        # 设置环境
        server.setEnv(obj['env'])
        print(name, '->', '参数校验成功')
        # war包目录处理
        if 'warpath' in obj.keys():
            server.setWarpath(obj['warpath'])
        # 处理拉取部署相关
        dep = Deploy(server, self.cachepath)
        print(name, '->', '克隆代码开始')
        # 拉取源码
        status_clone = dep.clone()
        if status_clone:
            print(name, '->', '克隆代码成功，开始编译编译、打包')
            flag_ask = mbox.askquestion(self.mbtitle, "代码克隆成功，是否继续编译、上传")
            if flag_ask == 'no':
                # 暂停
                print(name, '->', '暂停继续编译、上传')
                return
            else:
                # 进行编译、上传
                print(name, '->', '编译、打包开始')
                msg = dep.build()
                # msg = 'success'
                if msg != 'success':
                    print(name, '->', '编译、打包失败，结束处理')
                    mbox.showinfo(self.mbtitle, msg)
                    return
                # 打包成功开始上传
                print(name, '->', '编译、打包成功，开始上传、部署')
                flag_upload = dep.upload()
                msg = '失败'
                if flag_upload:
                    msg = '成功'
                print(name, '->', '上传、部署' + msg)

                # 重启tomcat-zhx
                # flag_tomcatRestart = dep.tomcatRestart()
                # msg = '失败'
                # if flag_tomcatRestart:
                #     msg = '成功'
                # print(name,'->', 'tomcat重启' + msg)

                print(name, '->', '工程处理完成')
                mbox.showinfo(self.mbtitle, '部署' + msg)

        else:
            print(name, '->', '克隆代码失败，结束处理')
            mbox.showerror(self.mbtitle, "代码克隆失败")

    # 保存修改
    def save(self):
        # 输入验证
        server = self.checkInput()
        name = self.cbbComp.get()
        if not server:
            print(name, '->', '参数检验有误，结束处理')
            return
        # 数据验证成功
        print(name, '->', '数据验证成功，进行保存')
        # 写入配置文件
        flag_write = Conf().write(server, name)
        if not flag_write:
            print(name, '->', '写入配置文件失败，结束处理')
            mbox.showerror(self.mbtitle, "保存失败")
            return
        print(name, '->', '写入配置文件完成，保存成功')
        mbox.showinfo(self.mbtitle, '保存成功')
    
    # 检验输入参数
    def checkInput(self):
        host = self.hostComp.get()
        port = self.portComp.get()
        account = self.accountComp.get()
        pwd = self.pwdComp.get()
        target = self.targetComp.get()
        git = self.gitComp.get()
        branch = self.branchComp.get()
        types = self.typeComp.get()
        msg = ''
        if len(host) < 1:
            msg = '服务器IP有误'
        if len(port) < 1:
            msg = '服务器端口号有误'
        if len(account) < 1:
            msg = '服务器账号有误'
        if len(pwd) < 1:
            msg = '服务器密码有误'
        if len(target) < 1:
            msg = '请输入部署路径'
        if len(git) < 1:
            msg = '请输入Git仓库地址'
        if len(branch) < 1:
            msg = '请输入Git分支'
        if types != 1 and types != 2:
            msg = '请选择工程类型'
        if len(msg) > 0:
            mbox.showerror(self.mbtitle, msg)
            return False
        else:
            server = Server()
            server.setHost(host)
            server.setPort(port)
            server.setAccount(account)
            server.setPwd(pwd)
            server.setTarget(target)
            server.setGit(git)
            server.setBranch(branch)
            server.setTypes(types)
            return server
        return False

    # 退出
    def exit(self):
        sys.exit()

    # 处理缓存路径问题
    def setCachePath(self, cachePath):
        # 测试配置文件目录
        profile_test = os.path.join(cachePath, 'profile_test')
        # 配置目录是否存在验证
        if not os.path.exists(profile_test):
            # 配置目录不存在，创建
            os.makedirs(profile_test)
        
        # 生产配置文件目录
        profile_pro = os.path.join(cachePath, 'profile_pro')
        # 配置目录是否存在验证
        if not os.path.exists(profile_pro):
            # 配置目录不存在，创建
            os.makedirs(profile_pro)
