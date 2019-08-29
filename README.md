# 使用帮助

```bash
$ git clone https://github.com/vbcpascal/RasPi-Laser-Engraving
```

**注意：使用激光请佩戴防护镜，避免直射及直接观察！！**



## 连线说明

**底部电机 stepper_x 对应驱动板**

​	电压：5V

​	GND -> GPIO 39（GND）

​	STP -> GPIO 40（BCM 21）

​	DIR -> GPIO 38（BCM 20）

**上方电机 stepper_y 对应驱动板**

​	电压：5V

​	GND -> GPIO 34（GND）

​	STP -> GPIO 33（BCM 13）

​	DIR -> GPIO 31（BCM 6）

**激光 laser**

​	电压：12V

​	PWM $\to$ GPIO 12

​	TTL- $\to$ GPIO 14（GND）



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
```

**加载并打印操作文件**

``` bash
$ python main.py -m work -f pics/base_shape.png	# 输入操作打印
```

如果本地环境没有 OpenCV，可以使用`main_lite.py`代替`main.py`处理操作。



## 常见问题说明

**Q：下方电机移动明显减慢**

A：移除电机上方较大块亚克力板，减轻负重（推荐）；或适当增大电压；

**Q：打印圆不圆，或封闭处衔接不到位**

A：电机精确度有限，属于正常现象；

**Q：打印出来痕迹不清晰，或纸被烧漏**

A：根据材料修改 `LaserCtrl.py` 文件中 `self.change_duty_cycle(85)` 的数值（从1至100），其实这本应该是一个可指定的参数。



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


