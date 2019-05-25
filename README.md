# 使用帮助

```shell
$ git clone https://github.com/vbcpascal/RasPi-Laser-Engraving
```

## 步进电机

### EasyDriver.py

用于通过EasyDriver控制步进电机。包含类EasyDriver：

#### 构造函数参数
```makefile
pin_step:   GPIO-pin for the EasyDriver Step
pin_dir:    GPIO-pin for the EasyDriver Direction
pin_ms1:    GPIO-pin for the EasyDriver MicroStep 1
pin_ms2:    GPIO-pin for the EasyDriver MicroStep 2
pin_slp:    GPIO-pin for the EasyDriver Sleep
pin_rst:    GPIO-pin for the EasyDriver Reset
pin_enable: GPIO-pin for the EasyDriver Enable
delay:      Delay time between steps
gpio_mode:  Use "BOARD" or "BCM"
```
####  成员函数
```python
step(self)
dir(self, dir)
set_full_step(self)
set_half_step(self)
set_quarter_step(self)
set_eight_step(self)
slp(self)
wake(self)
enable(self)
disable(self)
rst(self)
set_delay(self, delay)
finish(self)
```

将EasyDriver驱动板按如下方式连接：

```makefile
Left_Stepper:
  	GND -> GPIO 39
  	DIR -> GPIO 38（BCM 20）
  	STE -> GPIO 40（BCM 21）
Right_Stepper:
  	GND -> GPIO 34
  	DIR -> GPIO 31（BCM 6）
  	STE -> GPIO 33（BCM 13）
```



### LaserCtrl.py

用于通过PWM控制激光。将12V激光头按如下方式连接：

``` makefile
Laser:
	PWM -> GPIO 12
	GND -> GPIO 14
```

提供类LaserCtrl：

#### 构造函数参数

```makefile
pin_pwm:    GPIO-pin for PWM
frequency:  frequency for PWM
gpio_mode:  Use "BOARD" or "BCM"
```

#### 成员函数

```python
ChangeDutyCycle(self, i)
finish(self)
```



## 远程控制

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

#### 链接

```shell
$ uwsgi --http :8001 --plugin python --module server.wsgi
```



## 参考程序

https://github.com/davef21370/EasyDriver
https://github.com/rfverbruggen/easydriverpy



