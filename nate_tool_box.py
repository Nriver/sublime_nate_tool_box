# -*- coding: utf-8 -*-
# @Author: Zengjq
# @Date:   2018-05-24 10:03:35
# @Last Modified by:   Zengjq
# @Last Modified time: 2018-08-15 13:00:17
import sublime
import sublime_plugin
import os
from contextlib import contextmanager
import time
import datetime
import re
import itertools
import subprocess
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


# def append_if_not_in(element_list, target_list):
#     """
#     合并list 去重 保持顺序
#     """
#     for element in element_list:
#         if element not in target_list:
#             print("添加系统环境", element)
#             target_list.append(element)

# # !!! 十分不稳定 建议不要使用 !!!
# #  !!!   使用系统模块的方法 !!!
# import sys
# # sys.path.append('C:\\Python36')
# # sys.path.append('C:\\Python36\\python36.zip')
# # sys.path.append('C:\\Python36\\DLLs')
# # sys.path.append('C:\\Python36\\lib')
# # sys.path.append('C:\\Python36\\lib\\site-packages')

# import platform
# if platform.system() == 'Windows':
#     python_path_list = ['C:\\Python36',
#                         'C:\\Python36\\python36.zip',
#                         'C:\\Python36\\DLLs',
#                         'C:\\Python36\\lib',
#                         'C:\\Python36\\lib\\site-packages', ]
# elif platform.system() == 'Darwin':
#     # python_path_list = ['/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/',
#     #                     '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/',
#     #                     '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/', ]
#     python_path_list = ['/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/',
#                         '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/',
#                         '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6',
#                         '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/', ]
# elif platform.system() == 'Linux':
#     python_path_list = []

# append_if_not_in(python_path_list, sys.path)

# delegator.py
# sublime会找不到模块

# # flask服务 可以用非debug模式启动 但是整个sublime会被卡死
# import flask
# from flask import Flask, request
# app = Flask(__name__)
# listen_IP = 'localhost'
# listen_port = 19998
# debug = False
# @app.route("/")
# def hello():
#    remote_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
#    print(remote_ip)
#    return remote_ip
# app.run(host=listen_IP, port=int(listen_port), debug=debug)


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


class FileNameInputHandler(sublime_plugin.TextInputHandler):

    def __init__(self, view):
        self.view = view

    def name(self):
        return "new_name"

    def placeholder(self):
        return "New File Name"

    def initial_text(self):
        old = self.view.file_name()

        if old is None:
            return self.view.name()
        else:
            branch, leaf = os.path.split(old)
            return leaf

    def validate(self, name):
        if self.view.file_name() is None:
            return True
        else:
            return len(name) > 0


class nateToolBoxRender(sublime_plugin.TextCommand):

    def run(self, edit, results):
        self.edit = edit
        self.results = results
        self.rview = self.get_view()
        self.draw_header()
        self.draw_results()
        self.window.focus_view(self.rview)

    def get_view(self):
        self.window = sublime.active_window()
        for view in self.window.views():
            if view.settings().get('search_results', False):
                view.erase(self.edit, sublime.Region(0, view.size()))
                return view
        view = self.window.new_file()
        view.set_name('Search Result')
        view.set_scratch(True)
        view.settings().set('search_results', True)
        view.settings().set('command_mode', True)
        return view

    def draw_header(self):
        res = '// ' + str(datetime.datetime.now().strftime('%A %m/%d/%y at %I:%M:%S%p')) + '\n'
        self.rview.insert(self.edit, self.rview.size(), res)

    def draw_results(self):
        data = [[], []]
        for items in self.results:
            res = '\n## 搜索结果 (%n)\n'.replace('%n', str(len(items)))
            self.rview.insert(self.edit, self.rview.size(), res)
            for idx, item in enumerate(items, 1):
                start = self.rview.size()
                self.rview.insert(self.edit, start, str(idx) + '. ' + self.draw_file(item) + '\n')
                region = sublime.Region(start, self.rview.size())
                data[0].append(region)
                data[1].append(item)
        self.rview.add_regions('results', data[0], '')
        d = dict(('{0},{1}'.format(k.a, k.b), v) for k, v in zip(data[0], data[1]))
        self.rview.settings().set('review_results', d)

    def draw_file(self, item):
        return item['file'] + ':' + str(item['line'])


class nateToolBoxCommand(sublime_plugin.TextCommand):
    # 测试用的Command
    # view.run_command("nate_tool_box")

    def run(self, edit):
        with beautiful_tag('nate tool box'):
            # self.view.insert(edit, 0, "nate tool box!")
            # print(edit)
            # print(self.view)
            # print(self)

            # print('当前运行环境路径', os.getcwd())

            # 获取当前文件的文件路径
            file_path = self.view.file_name()

            # 某些情况下(比如直接切到sublime的console里面去)view会失去焦点 造成读取不到文件
            if file_path is None:
                pass
                # print('当前未选中文件')
            else:
                # print('当前文件路径', file_path)
                file_dir = os.path.dirname(file_path)
                # print('所属目录', file_dir)
                file_name = os.path.basename(file_path)
                # print('文件名', file_name)

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
            # print('当前选中的文字', regionStr)

            # 读取配置文件
            # sublime的全局配置文件
            settings_sublime = sublime.load_settings("Preferences.sublime-settings")
            font_size = settings_sublime.get("font_size")
            # print("读取全局设置")
            # print('编辑器字体大小', font_size)

            # 插件自己的配置文件
            settings = sublime.load_settings("nate_tool_box.sublime-settings")
            human_name_list = settings.get('human_name_list', [])
            anime_name_list = settings.get('anime_name_list', [])
            # print("读取插件设置 human_name_list", human_name_list)
            # print("读取插件设置 anime_name_list", anime_name_list)

            # 使用第三方的插件 直接拷贝到目录下来使用

            # delegator模块 输出当前路径 和getcwd()效果一样
            # print("使用第三方的插件")
            # result = delegator.run('echo %cd%')
            # print(result.out)

            # dirty hack
            search_string = 'redis'

            def search_files(keyword):
                if keyword == '':
                    return []
                # 遍历snippet文件夹
                code_snippet_folders = settings.get('code_snippet_folders', [])
                ignore_folders = settings.get('ignore_folders', [])
                ignore_folders_pattern = re.compile('|'.join(ignore_folders))
                # 找出python文件有哪些
                py_file_paths = []
                search_result_list = []
                for code_snippet_folder in code_snippet_folders:
                    for index, (dirpath, dirnames, filenames) in enumerate(os.walk(code_snippet_folder)):
                        # print(index)
                        # print('路径', dirpath)
                        # print('包含文件夹', dirnames)
                        # print('包含文件', filenames)
                        ignore_current_path = re.search(ignore_folders_pattern, dirpath)
                        # 排除忽略的文件夹
                        if (ignore_current_path):
                            # print('忽略文件夹', dirpath)
                            continue
                        # 获取文件夹下.py文件路径
                        for filename in filenames:
                            if filename.endswith('.py'):
                                py_file_paths.append(os.path.join(dirpath, filename))
                # print(py_file_paths)
                # print(str(len(py_file_paths)) + '个python文件')

                # 从文件列表里查找内容
                encoding = settings.get('encoding', 'utf-8')
                stop_searching_flag = False
                for py_file_path in py_file_paths:
                    with open(py_file_path, 'r', encoding=encoding) as f:
                        for num, line in enumerate(f, 1):
                            if keyword in line:
                                search_result = {}
                                search_result['file'] = py_file_path
                                search_result['line'] = num
                                search_result_list.append(search_result)
                            if len(search_result_list) >= 20:
                                break
                        else:
                            continue
                        break
                return search_result_list

            # 获取输入
            def on_done(input_string):
                pass
                # print('finish with', input_string)

            def on_change(input_string):
                # print('changed', input_string)
                self.view.run_command('nate_tool_box_render', {
                    "results": [search_files(input_string)]
                })

            def on_cancel():
                pass
                # print('end')

            window = self.view.window()
            window.show_input_panel("Text to search:", "", on_done, on_change, on_cancel)

            # yes no
            # a = sublime.ok_cancel_dialog('啊啊啊啊')
            # print('a is', a)
            # 结束 输出时间
            print(datetime.datetime.now())


class nateToolBoxResults(sublime_plugin.TextCommand):

    def run(self, edit, **args):
        self.settings = self.view.settings()
        if not self.settings.get('review_results'):
            return
        if args.get('open'):
            window = self.view.window()
            index = int(self.settings.get('selected_result', -1))
            result = self.view.get_regions('results')[index]
            coords = '{0},{1}'.format(result.a, result.b)
            i = self.settings.get('review_results')[coords]
            p = "%f:%l".replace('%f', i['file']).replace('%l', str(i['line']))
            view = window.open_file(p, sublime.ENCODED_POSITION)
            window.focus_view(view)
            return
        if args.get('refresh'):
            self.view.run_command('nate_tool_box')
            self.settings.erase('selected_result')
            return
        if args.get('direction'):
            d = args.get('direction')
            results = self.view.get_regions('results')
            if not results:
                return
            start_arr = {
                'down': -1,
                'up': 0,
                'down_skip': -1,
                'up_skip': 0
            }
            dir_arr = {
                'down': 1,
                'up': -1,
                'down_skip': 10,
                'up_skip': 10 * -1
            }
            sel = int(self.settings.get('selected_result', start_arr[d]))
            sel = sel + dir_arr[d]
            if sel == -1:
                target = results[len(results) - 1]
                sel = len(results) - 1
            if sel < 0:
                target = results[0]
                sel = 0
            if sel >= len(results):
                target = results[0]
                sel = 0
            target = results[sel]
            self.settings.set('selected_result', sel)
            region = target.cover(target)
            self.view.add_regions('selection', [region], 'selected', 'dot')
            self.view.show(sublime.Region(region.a, region.a + 5))
            return
