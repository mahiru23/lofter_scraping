# lofter_scraping



`itera_like`：获取所有like文章内容


`change_uni`：处理`itera_like`返回内容，将对应文件夹下所有unicode字符解析为中文


`utils.py`：主要的工具函数，现在从之前获取的所有like信息，提取所有like文章的作者
- 已经修复notitle问题，现在会在触发时等待1s，并重新尝试


`notitle.py`（已废弃）：紧急处理之前代码中的notitle问题，所幸记录了log，`utils.py`被修复后已经无用


`it_user`（已废弃）：获取一个user的所有文章（旧版本，目前已经废弃）


`dict`：打印出来的pair_dict

