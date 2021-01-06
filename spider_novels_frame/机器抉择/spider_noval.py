import requests
import time
from bs4 import BeautifulSoup as bs
import random

""" 最初访问小说章节目录页面
GET /26134/ HTTP/1.1
Host: www.huaxiangju.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
"""

""" 访问第一章具体内容
GET /26134/6916687.html HTTP/1.1
Host: www.huaxiangju.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://www.huaxiangju.com/26134/
Cookie: jieqiVisitId=article_articleviews%3D26134; Hm_lvt_dcf50d7170c681fffd149795c78eda7a=1572487520; Hm_lpvt_dcf50d7170c681fffd149795c78eda7a=1572487534; Hm_lvt_a56cc74e74f5ef145e68487ce4daed79=1572487520; Hm_lpvt_a56cc74e74f5ef145e68487ce4daed79=1572487534
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
"""

""" 访问第二章具体内容
GET /26134/6916692.html HTTP/1.1
Host: www.huaxiangju.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://www.huaxiangju.com/26134/
Cookie: jieqiVisitId=article_articleviews%3D26134; Hm_lvt_dcf50d7170c681fffd149795c78eda7a=1572487520; Hm_lpvt_dcf50d7170c681fffd149795c78eda7a=1572487648; Hm_lvt_a56cc74e74f5ef145e68487ce4daed79=1572487520; Hm_lpvt_a56cc74e74f5ef145e68487ce4daed79=1572487648
Connection: close
Upgrade-Insecure-Requests: 1
"""

# cookies字段会变化，但是去掉后访问依然正常

URL = "https://www.huaxiangju.com"


def pre_process():
    # 预处理，用来模拟浏览器的请求头
    head = {
        'Host': 'www.huaxiangju.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.huaxiangju.com/26134/',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    return head


def get_web_page(head, url, i):
    # 发送请求，获得网页HTML代码
    r = requests.get(url=URL + url, headers=head)
    if r.status_code is not 200:
        r.raise_for_status()
        exit()
    r.encoding = r.apparent_encoding
    with open("data/names.txt", encoding='utf-8') as name:
        a = name.readlines()
        print(a[i - 1] + "已经爬取")
    with open("log.txt", "a+", encoding='utf-8') as log:
        log.write(time.asctime(time.localtime(time.time())) + str(a[i - 1]).replace('\n', '') + str("\t已经爬取\n"))

    time.sleep(random.uniform(1, 5))
    return r.text


def handle_html(text):
    # 处理HTML页面代码，获得想要的格式和输出
    novel = ""
    soup = bs(text)
    title = soup.find_all("h2")
    # print(title)
    novel += title[0].string.replace("<h2>", "").replace("</h2>", "")

    content = soup.findAll(name="div", attrs={"class": "articleCon"})
    # print(str(content[0]))

    dirty_words = ['<div class="articleCon">',
                   '<p>花香居提供女生言情小说在线阅读，言情小说免费阅读，言情小说TXT下载，言情小说阅读之家。https://www.huaxiangju.com/',
                   '本书连载自免费原创小说网站”花香居”www.huaxiangju.com，中国最有爱的年轻小说网站！各大市场下载官方免费APP，享最快更新。',
                   '<br>花香居提供女生言情小说在线阅读，言情小说免费阅读，言情小说TXT下载，言情小说阅读之家。https://www.huaxiangju.com/</br></p>',
                   '</div>']
    a = str(content[0]) \
        .replace(dirty_words[0], '') \
        .replace(dirty_words[1], '') \
        .replace(dirty_words[2], '') \
        .replace(dirty_words[3], '') \
        .replace(dirty_words[4], '') \
        .replace("<br/>", "\n") \
        .replace("    ", "")
    novel += a
    # rint(novel)

    with open("temp.txt", "w", encoding='utf-8') as ff:
        ff.writelines(novel)

    return novel


def save_content(novel):
    file = open("机器抉择.txt", "a+", encoding='utf-8')
    file.writelines(novel)

    return


if __name__ == '__main__':
    head = pre_process()
    text = ""
    with open("data/urls.txt") as a:
        urls = a.readlines()
        i = 1
        for url in urls:
            text = get_web_page(head=head, url=url, i=i)
            i = i + 1
            novel = handle_html(text)
            save_content(novel)

            if i % 5 is 0:
                time.sleep(5)
