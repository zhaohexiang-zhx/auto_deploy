#!/usr/bin/python
# coding = utf-8
import os
import shutil

class Util():
    # 复制
    def copy(local, target, profileName):
        try:
            if not os.path.exists(local) or not os.path.exists(target):
                return False
            for root, dirs, files in os.walk(local):
                for file in files:
                    # 文件复制
                    localPath = os.path.join(root, file)
                    targetPath = os.path.join(target, root.split(profileName)[1])
                    shutil.copy(localPath, targetPath)
        except Exception as e:
            print(e)
            return False
        else:
            return True

                