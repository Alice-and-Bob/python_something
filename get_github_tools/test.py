import re
import os

# md_file = open("README_CN.md", encoding='utf-8')
# md_text = md_file.readline(3)

"""
### 子域名爆破枚举或接管

- https://github.com/lijiejie/subDomainsBrute - **Lijiejie开发的一款使用广泛的子域名爆破枚举工具**

> **评分**: 🌟🌟🌟🌟🌟         |         **编程语言**: **Python 2.x**         |         **仍在维护**: ✖️

"""

md_text = ["### 子域名爆破枚举或接管",
           "",
           "- https://github.com/lijiejie/subDomainsBrute - **Lijiejie开发的一款使用广泛的子域名爆破枚举工具**",
           "",
           "> **评分**: 🌟🌟🌟🌟🌟         |         **编程语言**: **Python 2.x**         |         **仍在维护**: ✖",
           ""]

# re_string = '### .*\n'  # 项目主题题目
# re_string = '- .* -'  # github地址
re_string = '\*\*(.*)\*\*'  # 说明文字

for i in md_text:
    ans = re.findall(re_string, str(i))
    print(ans)


def a():
    os.system("mkdir aaa")
    os.system("cd aaa")


def b():
    os.system("ls")


a()
b()
"""
pro_name = ['### 子域名爆破枚举或接管\n']
pro_name = str(pro_name[0]).replace("### ", "").replace("\n", "")
cmd = "mkdir " + pro_name  # 建立以项目为名的文件夹
os.system(cmd)
"""
