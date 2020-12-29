#!/usr/bin/python
# coding = utf-8
from core.conf import Conf
from core.gui import GUI

def main():
    print('HKAD-main函数')
    # 配置文件操作
    cfg = Conf()
    # 配置文件初始化
    cfg.init()
    # UI处理
    GUI(cfg.sections)

if __name__ == "__main__":
    main()