# HomePage


Python开发管理后台+Bootstrap响应式官网首页

后端：Python Django

前端：Bootstrap

数据库：MySQL、Redis

服务端：Centos、Nginx、uWSGI、Supervisord


# 计划前端实现功能：

1.首页：响应式导航条、轮播图、基本内容、Footer区块

2.资讯内容：响应式资讯内容管理、热门资讯

3.新闻模块：标题、作者、内容、日期，热门资讯

4.案例：合作相关展示页面

5.关于：Ajax留言板块，百度地图API，常见板式

6.页面访问次数、IP统计数据收集统计分析


# 计划后端实现功能：

1.首页内容管理：Banner轮播图管理，包括：图片管理、超链接配置、标题、内容、启用停用

2.首页资源、资讯、案例：资讯管理、热门资讯管理等

3.新闻：集成KindEditor富文本编辑插件，编辑、修改回调等

4.用户管理、角色权限管理、菜单管理：实现增删改查、菜单路径配置、修改回调、用户权限分配等功能

5.留言管理：基本管理查看功能，新增留言条数显示

6.图标统计模块：按时间段统计页面访问次数，独立IP访问页面数，单日数据分析，分别生成柱状图、饼图、曲线图


# 项目部署调试篇

1.本地调试：根目录运行>python manage.py runserver 0.0.0.0:8080

2.服务器部署篇：

## 运行环境：Centos、Nginx、uWSGI、Supervisord、Redis、Mysql 

备注：Linux环境下需要手动下载并配置字体库，绝对文件路径


Nginx.conf：


        server {
                listen 88;
                server_name localhost;
        location / {
                include /usr/local/nginx/conf/uwsgi_params;
                uwsgi_pass 127.0.0.1:8000;
                }
        location /static {
                alias /var/www/HomePage/static;
                }
        }

		
		
uWSGI.ini:		


	[uwsgi]
	#http = 127.0.0.1:8000
	socket = 127.0.0.1:8000
	chdir = /var/www/HomePage
	module = myapp.wsgi
	master = true
	processes = 2
	threads = 2
	max-requests = 6000
	chmod-socket = 664
	vacuum = true


supervisord.conf:


	[program:HomePage]
	directory = /var/www/HomePage
	command = uwsgi --ini uwsgi.ini



	

## 想做就做呗，╮(╯▽╰)╭     ！！！

