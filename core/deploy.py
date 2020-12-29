#!/usr/bin/python
# coding = utf-8
import git
from git import Repo
import os,stat
import shutil
from bean.server import Server
from utils.sshclient import SSHClient
from utils.util import Util

'''
处理部署相关
'''
class Deploy():
    server = Server()
    # 缓存路径
    cachepath = ''
    # 工程名
    proTitle = ''

    def __init__(self, server, cachepath):
        self.server = server
        self.cachepath = cachepath
    
    # 拉取git代码
    def clone(self):
        try:
            # git地址
            gitUrl = self.server.getGit()
            # 获取工程名
            self.proTitle = self.getProjectTitle(gitUrl)
            # 目标暂存地址
            cachepath = os.path.join(self.cachepath, self.proTitle)
            if os.path.exists(cachepath):
                # 清空文件夹 shutil.rmtree抛异常，直接使用RD /S /Q
                os.system('RD /S /Q ' + cachepath)
                # shutil.rmtree(cachepath, onerror= self.modifyPermission)
                # os.mkdir(cachepath)
            else:
                os.makedirs(cachepath)
                # os.chmod(self.cachepath, stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
            # clone_repo = git.Repo.clone_from(gitUrl, cachepath)
            # remote = clone_repo.remote()
            # # 拉取
            # remote.pull(self.server.getBranch())
            Repo.clone_from(gitUrl, to_path=cachepath, branch=self.server.getBranch())
        except Exception as e:
            print(e)
            return False
        else:
            return True

    # 编译 需区分工程类型
    def build(self):
        types    = self.server.getTypes()
        path = os.path.join(self.cachepath, self.proTitle)
        if not(os.path.exists(path)):
            return '工程目录不存在'
        # 覆盖配置
        profile_dir = 'profile_' + self.server.getEnv()
        profile = os.path.join(self.cachepath, profile_dir, self.proTitle)
        if os.path.exists(profile):
            # 已设置配置文件，需覆盖
            # 复制
            print('存在配置文件，进行覆盖操作开始')
            flag_copy = Util.copy(profile, self.cachepath, profile_dir + '\\')
            if not flag_copy:
                msg = '配置文件覆盖操作异常'
                print(msg)
                return msg
            print('配置文件覆盖操作完成')
        # 切换到项目目录
        os.chdir(path)
        # 默认失败
        flag_cmd = -1
        if types == 1:
            # Vue 工程
            # 执行npm install
            os.system('cnpm install')
             # 重新编译 node-sass
            os.system('npm rebuild node-sass')
            # npm run build
            flag_cmd = os.system('npm run build')
        if types == 2: 
            # Java工程
            # maven打包
            # 区分测试环境和正式环境，配置文件不同
            if env == 'test':
                flag_cmd = os.system('mvn clean package -P dev -Dmaven.test.skip=true')

            if env == 'pro':
                flag_cmd = os.system('mvn clean package -P prod -Dmaven.test.skip=true')
            # 打包成功
            if flag_cmd == 0:
                # 将war包复制放入dist
                # 本地war路径
                local = os.path.join(path, self.server.getWarpath())
                # 目标路径
                target = os.path.join(path, 'dist')
                # 创建目标路径
                os.mkdir(target)
                # 复制
                shutil.copy(local, target)
        
        # 退出当前工程目录
        os.chdir(self.cachepath)
        if flag_cmd != 0:
            return '打包失败，请重试'
        # 打包成功，开始上传
        return 'success'

    # 获取工程名
    def getProjectTitle(self, gitUrl):
        if len(gitUrl) < 1:
            return ''
        index = gitUrl.rfind("/")
        title = gitUrl[index + 1: len(gitUrl)]
        title = title.split('.')[0]
        return title
    
    # 上传部署
    def upload(self):
        try:
            localPath = os.path.join(self.cachepath, self.proTitle, 'dist')
            # 判断路径问题
            if not os.path.exists(localPath):
                print('本地文件不存在')
                return False
            targetPath = self.server.getTarget()
            # 创建连接
            client = SSHClient(self.server)
            # 初始化
            client.init()
            # 上传
            client.upload(localPath, targetPath)
            # 关闭
            client.close()
        except Exception as e:
            # 连接出错
            print(e)
            return False
        else:
            return True

    #重启tomcat-zhx 需区分工程类型
    def tomcatRestart(self):
        types = self.server.getTypes()
        if types == 2:
            # 创建连接
            client = SSHClient(self.server)
            # 初始化
            client.init()
            # 关闭tomcat
            client.tomcatRestart()
            # 关闭连接
            client.close()

    # 设置权限
    def modifyPermission(self, func, path, execinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

        
