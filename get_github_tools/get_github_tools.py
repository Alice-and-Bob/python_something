# https://github.com/We5ter/Scanners-Box/blob/master/README_CN.md
# TODO：分析页面内的连接，使用git命令自动爬取clone到本地
"""
 根据源文件的特点，考虑采用正则匹配或是Markdown库自动解析
 整个结构分为：
       1、### 子域名爆破枚举或接管                           主题名称。这个应该使用在某个主题的文件夹的文件夹名上
       2、- https://github.com/lijiejie/subDomainsBrute - 具体工具连接页面，进行加工后按照这个来进行clone操作
       3、**Lijiejie开发的一款使用广泛的子域名爆破枚举工具**    生成一个说明文档，放在以以工具为名的文件夹下
       4、**编程语言**: **Python 2.x**                      编程语言。应该按照语言进行分类以方便使用；或者放在
                                                          说明文档里
"""
import re
import os

# 读一行文件
# ——>匹配三种模式（项目主题、GitHub地址、说明文字）
# ——>按匹配结果来选择三种操作（建立项目文件夹、执行clone操作、进入git文件夹写说明文字到txt）
# ——>结束提示完成
"""
class GitProject:
    project_name = ""
    git_url = ""
    explain_string = ""

    def __init__(self):
"""
str_buff = ""  # str的缓冲区，用于暂存说明文字，统一写入文件


def new_project_folder(pro_name):
    """
        用途：调用os.system()来新建整个主题的文件夹并进入该文件夹,当前主题下的全部Git操作均在这个文件夹里完成
        参数：pro_name : str类型
        返回：无
    """
    pro_name = str(pro_name[0]).replace("### ", "").replace("\n", "")
    cmd = "mkdir " + pro_name  # 建立以项目为名的文件夹
    os.system(cmd)
    print(pro_name + "文件夹已经建立，准备clone本主题下的GitHub仓库")
    return


def exec_git_cmd(url, pro_name):
    """
        用途：打开md文件，使用正则表达式匹配到github的url地址
        参数：url : str类型，GitHub的url地址
        返回：无
    """
    url = url + ".git"
    os.system("cd " + pro_name)  # 进入项目目录
    os.system("git clone " + url + "echo Done!")  # 执行git clone命令
    print(pro_name + "已经clone到本地!")


def new_explain_file(explain_text, pro_path, flag):
    """
        用途：在Git操作完成后，进入相应的目录下新建一个说明txt文档存放
        参数：explain_text : str类型
             pro_path : str类型
             flag : bool类型，用于判断说明文字是否全部获得到
        返回：无
    """
    explain_text = str(explain_text).replace("**", "")
    explain_file = open("README", "w+", encoding='utf-8')


if __name__ == '__main__':
    md_file = open("README_CN.md", 'r', encoding='utf-8')
    md_text = md_file.readline()
    while md_text is not "":
        # 处理单行文件并选择操作
        re_string_project = '### .*\n'  # 项目主题名称
        re_string_git = '- .* -'  # GitHub地址
        re_string_explain = '\*\*(.*)\*\*'  # 说明文字

        project_name = re.findall(re_string_project, md_text)
        git_url = re.findall(re_string_explain, md_text)
        explanation = re.findall(re_string_git, md_text)

        if bool(project_name):  # 如果当前行有项目名称
            new_project_folder(str(project_name))

        if bool(git_url):  # 如果当前行有GitHub地址
            exec_git_cmd(str(git_url), str(project_name))

        if bool(explanation):  # 如果当前行有说明文字
            new_explain_file(str(explanation), pro_path=str(path), )
