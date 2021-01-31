from machine import Pin, I2C, PWM, Timer
from ssd1306 import SSD1306_I2C
import utime, math

pwm_freq = 2000
duty_range = 1000
delay_rgs = 2
i = 0
pwm2 = PWM(Pin(2), freq=pwm_freq, duty=i)


def fading_led(t):
    global i
    if not retry:
        t.deinit()
        print("done")
    d = abs(int(1000 * math.sin(math.pi / 1000 * i)))
    pwm2.duty(d)
    i += 2


p = Pin(2, Pin.OUT)
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

retry = 20

tim0 = Timer(0)
tim0.init(period=delay_rgs, mode=Timer.PERIODIC, callback=fading_led)

while retry:
    oled.text("Connecting to network...", 0, 0)
    oled.text("twork...", 0, 8)
    oled.text("Retry times:", 16, 24)
    oled.text(str(retry), 64, 40)
    oled.show()
    oled.fill(0)
    retry = retry - 1
    utime.sleep(3)

if not retry:
    # change to texts() after myssd1306.py have been tested
    oled.text("Cannot connect t", 0, 0)
    oled.text("o given network,", 0, 8)
    oled.text(" check your con ", 0, 16)
    oled.text("fig in boot.py", 0, 24)
    oled.show()

    p.value(0)
