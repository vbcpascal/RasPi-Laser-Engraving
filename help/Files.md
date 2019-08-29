## EasyDriver.py

用于通过EasyDriver控制步进电机，包含类EasyDriver。

### 成员函数

```python
__init__(
    pin_step,		# GPIO-pin for the EasyDriver Step
    pin_dir,    	# GPIO-pin for the EasyDriver Direction
    pin_ms1,    	# GPIO-pin for the EasyDriver MicroStep 1
    pin_ms2,    	# GPIO-pin for the EasyDriver MicroStep 2
    pin_slp,    	# GPIO-pin for the EasyDriver Sleep
    pin_rst,    	# GPIO-pin for the EasyDriver Reset
    pin_enable, 	# GPIO-pin for the EasyDriver Enable
    delay,      	# Delay time between steps
    gpio_mode,		# Use "BOARD" or "BCM"
)

step()					# 进行一次移动
dir(dir)				# 调节方向
wait(n=1)				# 进行一次等待（用于短暂停顿）
set_delay(delay)		# 修改步进时间间隔（调节速度）
set_full_step()	
set_half_step()
set_quarter_step()
set_eight_step()
slp()
wake()
enable()
disable()
rst()
finish()
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

### 测试

``` bash
$ python Easydriver.py
```

效果：两个电机分别正向移动并返回。



## LaserCtrl.py

用于通过PWM控制激光。将12V激光头按如下方式连接：

```makefile
Laser:
	PWM -> GPIO 12
	GND -> GPIO 14
```

提供类LaserCtrl。

### 常数

以下常数用于记录激光状态，当且仅当使用 open() 和 close() 时会修改。

``` python
OPENED = True
CLOSED = False
```

### 成员函数

```python
__init__(
    pin_pwm,		# GPIO-pin for PWM
	frequency,		# frequency for PWM
	gpio_mode,		# Use "BOARD" or "BCM"
)
open()					# 打开激光，调节激光强度到预设值（85）
close()					# 关闭激光，调节激光强度到0
get_status()			# 获取激光状态（打开或关闭）
change_duty_cycle(i)	# 调节激光强度
finish()				# 结束
test()					# 进行测试，根据输入调节激光强度
```

### 测试与调节

``` bash
$ python LaserCtrl.py
```

效果：输入（1~100）的整数，调节激光强度。建议在树莓派开启后第一次给激光连通电源时先运行该脚本，并将强度调至为0。



## ImageReader.py

用于读取并提取图片轮廓，提供类 ImageReader。

### 常数

以下常数为图片处理模式：

``` bash
MODE_NONE = 0			# 嘛事不干
MODE_CONTOURS = 1		# 提取轮廓
MODE_GRAY = 2			# 纯黑白（对雕刻机不可使用）
```

### 成员函数

``` python
__init__(
    filename,			# 读入图片名
    work_size=1800		# 调整大小
)

set_mode(mode)			# 设置处理图片模式，目前仅提供 MODE_CONTOURS
get_mode(mode)			# 获取当前处理图片方式
get_contours()			# 提取图片轮廓，返回列表。set_mode后方可使用
get_floyd()				# 将图片转变为纯黑白，暂无后期处理程序
test_draw_contours()	# 显示提取效果，用于打印预览
```

具体使用方式可参考文件中 main 的部分。

### 使用

示例：读取并预览打印效果。

``` bash
$ python ImageReader.py pics/base_shape.png
Load image file: pics/base_shape.png
number of contours:  4
```



## Actions.py

提供“操作列表”以及相关操作，提供类 Actions。

### 常数

以下常数用于表示工作状态：

``` python
ACT_MOVE = 0			# 移动
ACT_WORK = 1			# 移动（工作时）
ACT_OPEN_LASER = 2		# 打开激光
ACT_CLOSE_LASER = 3		# 关闭激光
```

在解析时，ACT_MOVE 与 ACT_WORK 没有差异。

### 成员函数

``` python
push(action, point=None)		# 在工作列表中插入操作action，需要时指定点为point
clear()							# 清除工作列表
top_pop()						# 从工作列表弹出一项并返回
get_len()						# 获取工作步数
get_group_len()					# 获取工作组数
empty()							# 判断工作列表是否为空
save(filename)					# 保存当前工作列表至filename
load(filename)					# 从filename加载至工作列表
add_contours(reader)			# 从ImageReader中提取轮廓加载至工作列表
```

其中，get_len 返回结果为步数，即每个操作视为一步；get_group_len 返回结果为组数，从激光打开到关闭视为一组。组数为操作中关闭激光的数量，即无法保证正确结果。特殊地，当使用 add_contours 加载并未进行修改时，组数即为闭合轮廓数。

### 使用

示例：读取并保存操作至 cache 文件夹

```bash
$ python Actions.py pics/base_shape.png		# 生成操作并保存到 cache 文件夹
Load image file: ./pics/base_shape.png
[0, 132, 113]	# 第一个操作
4				# 总轮廓数(组数)
2645			# 总操作数（步数）
```

也可以通过如下方式生成 npy 文件：

``` python
# test_actions.py
acts = Actions()
acts.push(ACT_MOVE, [1000, 1000])
acts.push(ACT_OPEN_LASER)
acts.push(ACT_WORK, [100, 600])
acts.push(ACT_CLOSE_LASER)
acts.push(ACTS_MOVE, [0, 0])
acts.save('tmp.npy')
```



## Worker.py

提供类 Worker，用于组合以上所有文件。

### 常数

提供常数为移动方向，以及电机停顿时长（速度），后者可以根据实际情况修改。

``` bash
CW = True       # clockwise
CCW = False     # counterclockwise

WORK_DELAY = 0.005
STOP_DELAY = 0.00025
```

### 成员函数

``` bash
__init__(work_size=1800)	# 工作区间，需与ImageReader一致
laser_open()				# 打开激光
laser_close()				# 关闭激光
set_actions(actions)		# 为Worker设定actions，为Actions类对象
move_to(x, y)				# 直线移动至(x, y)位置，使用Bresenham算法
eval_one()					# 根据actions操控步进电机及激光（一步）
eval()						# 根据actions操控步进电机及激光（全部）
test()						# 测试
```

使用方式请参见 main.py



## main.py

### 测试

``` bash
$ python main.py
```

效果为两个电机分别移动 1800 步后返回，此功能不会测试激光。

### 工作

``` bash
$ python main.py -m work -f pics/base_shape.png		# 加载图片并打印
$ python main.py -m work -f cache/base_shape.npy	# 加载工作列表并打印
```

### main_lite.py

考虑到在树莓派上安装 OpenCV 颇为困难，可以在有 OpenCV 环境中生成 actions 的 npy 文件

``` bash
$ python Actions.py pics/base_shape.png
```

传输至树莓派后运行

``` bash
$ python main_lite.py -m work -f cache/base_shape.npy
```



## pics 与 cache

示例图片与对应 actions 文件。

- base_shape：圆、方形、五角星
- github：github logo
- pku & pku2：校徽（仅可用于作为打印示例，不可用于商业用途）
- gzc：作者姓名名章