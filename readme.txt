UI原型文件系统文档说明
一、主页
http://10.10.11.210:5555/----主页

二、启动：
1.nohup python3 main.py &------启动主程序
2.nohup python3 -m http.server 5556 &------启动静态服务（必须在这个目录下启动：uiSystemFiles/UI/ui）

三、启动前先查看进程是否有启动：
查看：ps -aux|grep python3
杀进程：kill -9 pid

四、备注
目前只支持zip压缩包