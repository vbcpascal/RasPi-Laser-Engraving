# 使用帮助

```bash
$ git clone https://github.com/vbcpascal/RasPi-Laser-Engraving
```

## 文件说明

`EasyDriver.py`：用于通过树莓派控制步进电机；

`LaserCtrl.py`：用于通过树莓派控制激光头；

`ImageReader.py`：用于读取并处理图片，提取轮廓；

`Actions.py`：通过轮廓生成操作，并支持保存与读取；

`Worker.py`：从操作控制雕刻机工作。

详细介绍可见 `Files.md`。

### 使用方法

**一般使用**

``` bash
$ python LaserCtrl.py		# 测试激光头
$ python main.py -m test	# 测试步进电机移动
$ python main.py -m work -f pics/base_shape.png		# 输入图片打印
$ python main.py -m work -f cache/base_shape.png	# 输入操作打印
```

**预览打印效果**

``` bash
$ python ImageReader.py pics/base_shape.png
```

**生成操作**

``` bash
$ python Actions.py pics/base_shape.png		# 生成操作并保存到 cache 文件夹
Load image file: ./pics/base_shape.png
[0, 248, 1785]	# 第一个操作
216				# 总轮廓数
13297			# 总操作数
```

**加载并打印操作文件**

``` bash
$ python main.py -m work -f cache/base_shape.png	# 输入操作打印
```

如果本地环境没有 OpenCV，可以使用`main_lite.py`代替`main.py`处理操作。



## 远程控制

远程控制……只是一个框架，不算完善吧。

### 安装django、nginx、uwsgi

```shell
$ sudo -s
$ pip3 install django
$ apt install nginx
$ pip3 install uwsgi
```

#### 测试uwsgi

新建test.py文件：

```python
# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return ["Hello World"] # python2
    #return [b"Hello World"] # python3
```

执行shell命令：

``` shell
$ uwsgi --http :8001 --plugin python --wsgi-file test.py
```

执行成功在浏览器中打开：[http://localhost:8001/](http://localhost:8001/) 显示Hello World说明uwsgi正常运行。

#### 测试django

```shell
$ cd RasPi-Laser-Engraving/server
$ python3 manage.py runserver
```

访问http://127.0.0.1:8001/ 项目正常（出现上传图片界面）说明django可以正常运行。

#### 连接

```shell
$ uwsgi --http :8001 --plugin python --module server.wsgi
```



## 参考程序

https://github.com/davef21370/EasyDriver
https://github.com/rfverbruggen/easydriverpy


