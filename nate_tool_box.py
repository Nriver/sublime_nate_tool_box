# -*- coding: utf-8 -*-
# @Author: Zengjq
# @Date:   2018-05-24 10:03:35
# @Last Modified by:   Zengjq
# @Last Modified time: 2018-05-24 10:20:49
import sublime
import sublime_plugin
import os
from contextlib import contextmanager
import time
import datetime

# 控制台调试 运行命令
# view.run_command("example")
# window.run_command("exec", {"shell_cmd" : 'dir'})
#

# sublime text 里面无法直接使用系统里面pip安装的模块
# 要使用第三方模块有两种方法

# 第一种是把模块拷贝过来 然后修改sys.path 加上当前路径去搜索模块
# import sys
# if os.path.join(os.path.dirname(__file__)) not in sys.path:
#     sys.path.append(os.path.join(os.path.dirname(__file__)))
# from delegator import delegator

# 第二种是把python3的运行环境加入到sys.path里面


def append_if_not_in(element_list, target_list):
    """
    合并list 去重 保持顺序
    """
    for element in element_list:
        if element not in target_list:
            print("添加系统环境", element)
            target_list.append(element)

# 使用系统模块的方法
import sys
# sys.path.append('C:\\Python36')
# sys.path.append('C:\\Python36\\python36.zip')
# sys.path.append('C:\\Python36\\DLLs')
# sys.path.append('C:\\Python36\\lib')
# sys.path.append('C:\\Python36\\lib\\site-packages')

python_path_list = ['C:\\Python36',
                    'C:\\Python36\\python36.zip',
                    'C:\\Python36\\DLLs',
                    'C:\\Python36\\lib',
                    'C:\\Python36\\lib\\site-packages', ]

append_if_not_in(python_path_list, sys.path)

import delegator
import flask


@contextmanager
def beautiful_tag(tag_name, total_length=56):
    """
    美化输出
    total length的默认值是 sublime text在Consolas的22号字体 一半屏幕能显示的长度
    """
    begin_tag = ''.join([tag_name, ' begin']).center(total_length, '=')
    print(begin_tag)
    yield
    end_tag = ''.join([tag_name, ' end']).center(total_length, '=')
    print(end_tag)


class SvnCompareCommand(sublime_plugin.TextCommand):
    # view.run_command("svn_compare")

    def run(self, edit, paths=None):
        print("I'm here")


class nateToolBoxCommand(sublime_plugin.TextCommand):
    # 测试用的Command
    # view.run_command("nate_tool_box")

    def run(self, edit):
        with beautiful_tag('nate tool box'):
            # self.view.insert(edit, 0, "nate tool box!")
            # print(edit)
            # print(self.view)
            # print(self)

            print('当前运行环境路径', os.getcwd())

            # 获取当前文件的文件路径
            file_path = self.view.file_name()

            # 某些情况下(比如直接切到sublime的console里面去)view会失去焦点 造成读取不到文件
            if file_path is None:
                print('当前未选中文件')
                return

            print('当前文件路径', file_path)
            file_dir = os.path.dirname(file_path)
            print('所属目录', file_dir)
            file_name = os.path.basename(file_path)
            print('文件名', file_name)

            # 当前视图
            view = self.view
            # 当前选择的区域
            sels = view.sel()
            selContent = ''
            if len(sels) > 0:
                # 获取以一个选中区域
                sels = sels[0]
            # 获取选中区域内容
            regionStr = view.substr(sels)
            print('当前选中的文字', regionStr)

            # 读取配置文件
            # sublime的全局配置文件
            settings_sublime = sublime.load_settings("Preferences.sublime-settings")
            font_size = settings_sublime.get("font_size")
            print("读取全局设置")
            print('编辑器字体大小', font_size)

            # 插件自己的配置文件
            settings = sublime.load_settings("nate_tool_box.sublime-settings")
            human_name_list = settings.get('human_name_list', [])
            anime_name_list = settings.get('anime_name_list', [])
            print("读取插件设置 human_name_list", human_name_list)
            print("读取插件设置 anime_name_list", anime_name_list)

            # 使用第三方的插件 直接拷贝到目录下来使用

            # delegator模块 输出当前路径 和getcwd()效果一样
            result = delegator.run('echo %cd%')
            print(result.out)

            # 结束 输出时间
            print(datetime.datetime.now())
