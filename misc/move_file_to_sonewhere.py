# TODO:在要移动的文件夹里使用，填写要移动的文件的匹配和目标文件夹，实现按照匹配文件并剪切/复制到目标文件夹
import os

py_path = "E:\\steam\\steamapps\\workshop\\content\\431960"
# py_path = os.path.dirname(__file__)  # path是Python文件的工作目录

# dirpath 当前目录下全部的子文件夹的绝对路径
# dirnames 当前目录下全部的文件夹名称
# filenames 当前目录下全部文件的名称
for dirpath, dirnames, filenames in os.walk(py_path):
    if '.mp4' in filenames:
        pass