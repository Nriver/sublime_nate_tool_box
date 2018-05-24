# sublime_nate_tool_box  
Nate 的 Sublime Text 自制插件

# 文件结构

Default (Windows).sublime-keymap  
sublime text的快捷键设置  
alt+z 快速触发插件的函数  

Main.sublime-menu  
是设置菜单在sublime text主界面的  
首选项 -> package settings 里面添加一个菜单

nate_tool_box.py  
插件的主要执行文件  
插件目录下的所有.py文件都会被扫描一遍  
插件每次保存都会触发reload

nate_tool_box.sublime-settings  
插件的配置

nate_tool_box_2.py  
次要执行文件

package-metadata.json  
是一个描述文件 在list package的时候会显示描述信息