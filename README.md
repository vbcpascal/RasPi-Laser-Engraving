## easydriver.py

### 构造函数参数
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
###  成员函数
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

## stepper.py
### Easydriver连接
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

## 参考程序
https://github.com/davef21370/EasyDriver
https://github.com/rfverbruggen/easydriverpy