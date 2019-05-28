## 功能说明

* 获取 Qupital, Capital 等第三方 Invoice 平台数据
* 将获取的数据以及根据业务需求计算的字段展示在 Web 前端

## 进度

1. 已完成

* 登录 & 注册
* 数据库存储及展示

2. 待完成

* 接入数据库
* 前端展示优化

## 需要的库

* flask
* flask_mysql
* flask_bootstrap
* flask_paginate
* flask_sqlalchemy
* flask_excel

## Python 虚拟环境
* 激活：source env/bin/activate
* 退出：env/bin/deactivate

## MySQL 数据库
* 安装：apt-get install mysql-server
* 查看编码：show variables like '%character%';
* 设置编码，其他编码设置类似：set character_set_server = utf8;

## 创建数据
* 激活服务器端 Python 虚拟环境
* 执行 python manage.py shell
* 在 shell 中执行 db.create_all()

## 数据库迁移
1. 初始化

    `python manage.py db init`

    这个命令会在项目下创建 migrations 文件夹，所有迁移脚本都存放其中。
   
2. 创建第一个版本

    `python manage.py db migrate -m "inital migration`
    
    检查migrations\versions，会新建一个版本.py，检查里面表格及字段，此时数据库中会自动创建一个alembic_version表格，用于记录数据库版本信息

3. 运行升级
  
    `python manage.py db upgrade`
    
    会把项目使用的数据库文件，更新为新的表格、字段，同时保留数据
    
## Shell 交互式
* 进入 shell

    `python manage.py shell`
    
* 删除所有的表
  
    `db.drop_all()`
    
* 创建所有的表
  
    `db.create_all()`

## 程序运行
* 创建数据库：handler.py
* 添加执行权限（stop.sh类似）：chmod +x start.sh
* 启动 Web：./start.sh
* 停止 Web：./stop.sh

## Chrome 下载安装
* 下载：wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
* 安装：dpkg -i google-chrome-stable_current_amd64.deb
