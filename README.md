# sublime_nate_tool_box  
Nate 的 Sublime Text 自制插件

# 文件结构

#### .gitignore  
git 提交忽略文件列表  

#### .no-sublime-package
防止sublime text把插件以.sublime-package的压缩包形式发布插件

#### .release-it.json
release-it的配置文件 禁用交互

#### command_commit_and_push.sh
git add & git commit & git push

#### Default (OSX).sublime-keymap
mac 系统下的快捷键

#### Default (Windows).sublime-keymap  
sublime text的快捷键设置  
alt+z 快速触发插件的函数  

#### do_release.sh
使用release-it在github上发布release版本

#### Main.sublime-menu  
是设置菜单在sublime text主界面的  
首选项 -> package settings 里面添加一个菜单

#### nate_tool_box.py  
插件的主要执行文件  
插件目录下的所有.py文件都会被扫描一遍  
插件每次保存都会触发reload

#### nate_tool_box.sublime-settings  
插件的配置

#### nate_tool_box_2.py  
次要执行文件

#### package-metadata.json  
是一个描述文件 在list package的时候会显示描述信息

#### package.json
release-it的配置文件 发布版本的版本号信息
