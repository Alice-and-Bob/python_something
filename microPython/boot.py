import gc
import math
import webrepl
import network
import utime
from machine import Pin, PWM, Timer, I2C
from ssd1306 import SSD1306_I2C

webrepl.start()
gc.collect()
# pwm初始化设置
pwm_freq = 2000
duty_range = 1000
delay_rgs = 2
i = 0
pwm2 = PWM(Pin(2), freq=pwm_freq, duty=i)
# WLAN初始化设置
SSID = ""
password = ""
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


def fading_led(t):
    global i
    if wlan.isconnected:
        t.deinit()
    d = abs(int(1000 * math.sin(math.pi / 1000 * i)))
    pwm2.duty(d)
    i += 2


def connect_wifi():
    tim0 = Timer(0)
    tim0.init(period=delay_rgs, mode=Timer.PERIODIC, callback=fading_led)

    p = Pin(2, Pin.OUT)
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)

    retry = 20
    while retry:
        if wlan.isconnected():
            oled.text("---CONNECTED!---", 0, 0)
            string = str(wlan.ifconfig()[0])
            oled.text("IP:", 0 * 8, 1 * 8)
            oled.text(string, 3 * 8, 3 * 8)
            string = str(wlan.ifconfig()[1])
            oled.text("Subnet Mask:", 0 * 8, 5 * 8)
            oled.text(string, 3 * 8, 7 * 8)
            oled.show()
            p.value(0)
            utime.sleep(3)
            p.value(1)
            break
        else:
            oled.text("Connecting to network...", 0, 0)
            oled.text("twork...", 0, 8)
            oled.text("Retry times:", 16, 24)
            oled.text(str(retry), 64, 40)
            oled.show()

            wlan.connect(SSID, password)

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

        p.value(1)


connect_wifi()
gc.collect()
