# coding:utf-8

import requests
from bs4 import BeautifulSoup
import os
import time
import threading


# www.qinxiaoshuo.com/read/0/1071/5d77c6ac56fec85e5b0fbd**.com
# 从58开始，以十六进制加，59，60,6a……
def get_content(url):
    # 用途：请求连接，获得网页源代码
    # 参数：url：str的网站链接
    head = {'Host': 'www.qinxiaoshuo.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.qinxiaoshuo.com/book/DATE%20A%20LIVE%E7%BA%A6%E4%BC%9A%E5%A4%A7%E4%BD%9C%E6%88%98',
            'Cookie': 'Hm_lvt_670dc4f892f02bdafabb0500f3a778a0=1555589067; '
                      'Hm_lpvt_670dc4f892f02bdafabb0500f3a778a0=1555589299; _ga=GA1.2.93717897.1555589068; '
                      '_gid=GA1.2.1985632109.1555589068',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'}
    a = requests.get(url, timeout=30, headers=head)
    return a


def process_text(source_code):
    # 用途：处理源文件
    # 参数：source_code：网页源代码
    pass


'''
    try:
        main_file = open('约会大作战.txt', 'a', encoding='utf-8')  # 总文件
        main = open('主线.txt', 'a', encoding='utf-8')  # 主线文件
        branch = open('安可短篇集.txt', 'a', encoding='utf-8')  # 安可文件
        # 解析html文件
        soup = BeautifulSoup(source_code, "html.parser")
        head = soup.title.string
        fiction = soup.find(id="chapter_content")
        # 遇到插画页面则跳过
        if '插画' in head:
            main_file.close()
            main.close()
            branch.close()
            return
        # 写入主文件
        main_file.write(fiction)
        main_file.flush()
        # 短篇和主线分别写入不同文件
        if '卷' in head:
            main.write(fiction)
            main.flush()
        else:
            branch.write(fiction)
            branch.flush()
    except IOError as file_error:
        print("文件读写发生错误")
    except requests.exceptions.ConnectionError:
        # 当连接超时时，应该重新连接爬取当前章节
        # relink(url)
        requests.exceptions.ConnectionError: ('Connection aborted.', TimeoutError(10060, 
        '由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。', None, 10060, None)) 

    except requests.exceptions.ReadTimeout:
        print("连接超时")
    finally:
        main_file.close()
        main.close()
        branch.close()
'''


def relink(url):
    # 用途：用于网站超时重连
    # 参数：url：当前爬取的url连接
    pass


'''
    req = get_content(url)
    process_text(req, url)
'''

'''def end_captcha(text):
    if '本章未完' in text:
        return True
    elif '本章已完' in text:
        return True
    else:
        return False
'''


def renew_url(_chapter, _page):
    # 用途：每次爬取完当前页面之后，在main函数里调用这个函数返回下一个url
    # 参数：_chapter：当前章节数
    #      _page：当前页数
    pass


'''
    URL = 'https://www.qinxiaoshuo.com/read/0/DATE%20A%20LIVE%E7%BA%A6%E4%BC%9A%E5%A4%A7%E4%BD%9C%E6%88%98/' \
          + str(_chapter) + '.html?xiaoshuo=' \
          + str(_page)
    return URL
'''


def shutdown():
    # 用途：用于在长时间爬取任务结束后自动关机
    # 参数：无
    cmd = 'shutdown -s -f -t 00'
    os.system(cmd)


def main_threading(chapter):
    pass


'''
    # 爬取开始
    logs = open('爬取记录.log', 'w')
    page = 1
    url = renew_url(chapter, page)
    req = get_content(url)
    # 爬取第chapter章的所有页
    while end_captcha(req):
        process_text(req, url)
        print("第", chapter, "章 第", page, "页已经爬取完毕")

        log = "第", chapter, "章 第", page, "页已经爬取完毕"
        logs.write(log)  # 写日志
        logs.flush()

        page = page + 1
        url = renew_url(chapter, page)
        req = get_content(url)
        time.sleep(0.5)
    # 在每一章之间加上分隔
    with open('约会大作战.txt', 'a') as main_file, open('主线.txt', 'a') as main, open('安可短篇集.txt', 'a') as branch:
        main_file.write('\n\n\n\n\n\n')
        main.write('\n\n\n\n\n\n')
        branch.write('\n\n\n\n\n\n')
    print("本章已经爬取完毕")
    logs.close()
'''

if __name__ == '__main__':
    # 取得连接，返回网页数据
    # 网页源数据处理，写入文件

    '''
    flag = input("0从头爬取，否则输入日志文件中显示的章节和页面的值断点续传")
    if flag is 0:  # 从头爬取
        for chapter in range(1, 342):
            main_threading(chapter)
            if chapter % 3 == 0:
                time.sleep(3)
            else:
                pass
        shutdown()
    else:
        chapter = input("输入章节数")
        page = input("输入页面数")

        # 爬取偶数章节
        odd_number = threading.Thread(target=main_threading, args=(chapter + 1,))
        # 爬取奇数章节
        even_number = threading.Thread(target=main_threading, args=(chapter,))
        chapter = chapter + 2
        odd_number.start()
        even_number.start()
        

print("Finished!")'''
# TODO：断点恢复，多线程爬取
