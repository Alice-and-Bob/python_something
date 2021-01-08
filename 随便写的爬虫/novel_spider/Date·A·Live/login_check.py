import requests
from bs4 import BeautifulSoup
import json

'''
TODO: 从文件里读取用户名和密码，利用requests库的session方法登录，
      通过访问分数网页获得分数，将分数写到json格式的文件里
'''


def read_account(file):  # 从文件读取账号密码
    pass


def login(username, passwd):  # 登录wechall，保持会话状态
    pass


def get_score(user):  # 访问分数页面获取分数
    pass


def write_score():  # 写入json格式用户信息
    pass


if __name__ == '__main__':
    account = open("账号密码.txt", "r")
    end = account.readline()
    line = 1
    while end is not 0x26:
        if line % 2 is 0:
            username = end
        else:
            passwd = end
        line = line + 1
