#!/usr/bin/python
# coding = utf-8

import paramiko
import os
import time

'''
处理网络请求
'''
class SSHClient():
    # 服务信息
    server = None
    # 连接对象
    __transport = None
    def __init__(self, server):
        self.server = server
        # 初始化，创建连接
        # self.init()

    # 初始化创建连接
    def init(self):
        print('HKAD-创建连接开始')
        # 设置SSH连接的远程主机地址和端口
        self.__transport = paramiko.Transport(self.server.getHost(), int(self.server.getPort()))
        # 通过用户名和密码连接SSH服务端
        self.__transport.connect(username = self.server.getAccount(), password = self.server.getPwd())
        print('HKAD-创建连接成功')
    
    # 上传
    def upload(self, localPath, targetPath):
        # 判断路径问题
        if not os.path.exists(localPath):
            return print('HKAD-本地文件不存在')

        print('HKAD-文件上传中...')
        # 实例化一个 sftp 对象,指定连接的通道
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 本地路径转换，将windows下的 \ 转成 /
        localPath = '/'.join(localPath.split('\\'))
        # 递归上传文件
        self.uploadFile(sftp, localPath, targetPath)

        print('HKAD-文件上传完成...')
        # 关闭连接
        self.close()
        return True

    # 上传文件
    def uploadFile(self, sftp, localPath, targetPath):
        # 判断当前路径是否是文件夹
        if not os.path.isdir(localPath):
            # 如果是文件，获取文件名
            file_name = os.path.basename(localPath)
            # 检查服务器文件夹是否存在
            self.checkRemoteDir(sftp, targetPath)
            # 服务器创建文件
            target_file_path = os.path.join(targetPath, file_name).replace('\\', '/')
            print(localPath, '->',target_file_path)
            # 上传到服务器
            sftp.put(localPath, target_file_path, self.sftpCallBack)
        else:
            # 查看当前文件夹下的子文件
            file_list = os.listdir(localPath)
            # 遍历子文件
            for p in file_list:
                # 拼接当前文件路径
                current_local_path = os.path.join(localPath, p).replace('\\', '/')
                # 拼接服务器文件路径
                current_target_path = os.path.join(targetPath, p).replace('\\', '/')
                # 如果已经是文件，服务器就不需要创建文件夹了
                if os.path.isfile(current_local_path):
                    # 提取当前文件所在的文件夹
                    current_target_path = os.path.split(current_target_path)[0]
                # 递归判断
                self.uploadFile(sftp, current_local_path, current_target_path)

    # 创建服务器文件
    def checkRemoteDir(self, sftp, targetPath):
        try:
            # 判断文件夹是否存在
            sftp.stat(targetPath)
        except IOError:
            # 创建文件夹
            self.exec(r'mkdir -p %s ' % targetPath)

    # 重启tomcat-zhx
    def tomcatRestart(self):
        print('HKAD-kill process...')
        self.exec('ps -ef | grep tomcat8 | grep -v grep | awk \'{print $2}\' | xargs kill -15')
        print('HKAD-process killed')
        time.sleep(3)
        print('HKAD-启动tomcat...')
        self.exec('/webapp/tomcat8/bin/startup.sh')

        print('HKAD-tomcat已启动')



    # 创建文件夹
    def exec(self, command):
        # 创建 ssh 客户端
        ssh = paramiko.SSHClient()
        # 指定连接的通道
        ssh._transport = self.__transport

        # 调用 exec_command 方法执行命令
        stdin, stdout, stderr = ssh.exec_command(command)

        # 获取命令结果，返回是二进制，需要编码一下
        res = stdout.read().decode('utf-8')
        # 获取错误信息
        error = stderr.read().decode('utf-8')
        print(res)
        # 如果没出错
        if error.strip():
            # 返回错误信息
            return error
        else:
            # 返回结果
            return res



    # 上传回调
    def sftpCallBack(self, start, end):
        process = (float(start) / end) * 100
        print('[','%.2f %%' % process, ']', end='\r', flush=True)
        if process == 100:
            print(end='\n')

    # 关闭
    def close(self):
        self.__transport.close()


    