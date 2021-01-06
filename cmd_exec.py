# TODO:调用Windows API，检测系统空闲，当空闲经过预定的时间时，称为准备阶段。在准备阶段时，程序循环检测特定文件夹下
# TODO:有一特定文件，则调用关机程序自动关机

import win32api
import win32con
import time

while 1:
    if win32api.GetAsyncKeyState(ord('a')):
        print("key a")
    time.sleep(5)
    print('no')