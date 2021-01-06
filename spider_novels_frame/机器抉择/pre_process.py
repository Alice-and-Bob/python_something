"""
    pre_process.py
    对于url数据来源的一个预处理，不是固定的，需要根据源数据做改动
"""

f = open("source.txt", encoding="utf-8")
uf = open("urls.txt", "w", encoding="utf-8")
nf = open("names.txt", "w", encoding="utf-8")

ef = open("name_error.txt", "w", encoding="utf-8")
url_list = []
name_list = []
chapter_list = []

a = f.readline()
i = 1
while a is not '\n':
    if i % 2 is 1:  # url
        url_list.append(a)
    else:  # name
        name_list.append(a)
    a = f.readline()
    i = i + 1

url_list.reverse()
name_list.reverse()

for url in url_list:
    uf.write(str(url))
for name in name_list:
    nf.write(str(name))
    if "..." in name:
        ef.write(str(name))

f.close()
nf.close()
uf.close()
ef.close()
