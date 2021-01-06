from moviepy.editor import *  # 导入moviepy包

path = "C:\\Users\\14196\\1.flv"  # path为要处理的文件的路径
video_clip = VideoFileClip(path)  # 使用函数打开视频文件，创建一个clip切片
audio_clip = video_clip.audio  # 从视频clip里取得音轨
audio_clip.write_audiofile("C:\\Users\\14196\\霜叶之歌.mp3")  # 写文件到磁盘
