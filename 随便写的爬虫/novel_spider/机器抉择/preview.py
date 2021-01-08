import requests


# url = "https://www.huaxiangju.com/26134/6916687.html"
def preview():
    url = input("输入url，预览HTML代码，保存在当前目录下'/data/preview.txt'里")
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    f = open("preview.txt", "w", encoding='utf-8')
    print(r.text)
    f.write(r.text)
