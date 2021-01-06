# 迷之问题，迷之解决……

import os
import re
import time
import threading
from concurrent.futures import ThreadPoolExecutor

import bs4
import requests
import urllib3

lock = threading.Lock()
tag_address = {}  # 章节_页数:图片真实地址


class Http404Exception(Exception):
    pass


def get_pic_addr(html, chp, page):
    domain = "http://comic3.kkkkdm.com/comiclist/2316/"
    middle = html.split('/')[5]
    url = domain + middle + "/" + str(page) + '.htm'
    try:
        time.sleep(0.1)
        r = requests.get(url)
        if r.status_code == 404:
            raise Http404Exception
        r.encoding = 'gbk'
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        temp_string = str(soup.find_all(language="javascript")[2])
        # print(temp_string)
        rr = r'newkuku.*jpg\'></a>'
        ans = re.findall(rr, temp_string)
        rrr = r'newkuku.*jpg'
        anss = re.findall(rrr, ans[0])[0]  # 图片真实地址的低位
        print("获得" + str(chp) + "章" + str(page) + "页图片地址")
        return anss
    except Http404Exception:
        print(str(chp) + "章" + str(page - 1) + "页是当前章节最后一页")
        return None
    except:
        with open("html_error.log", "w+") as error:
            error.writelines(str(chp) + "章" + str(page) + "页未知错误\n")
        return -1


def get_and_process_pic(pic_addr, chp, page):
    pic_domain = "http://s4.kukudm.com/"
    pic_url = pic_domain + pic_addr

    header = {
        'Host': 'v2.kukudm.com',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
                      'Version/11.0 Mobile/15A5341f Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    requests.DEFAULT_RETRIES = 10
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        # print(time.time())
        r = requests.get(pic_url, verify=False, stream=True)
        # print(time.time())
        with open("b\\" + str(chp) + '_' + str(page) + ".jpg", "wb") as pic:
            pic.write(r.content)
        if os.stat("b\\" + str(chp) + '_' + str(page) + ".jpg").st_size < 2000:
            lock.acquire()
            tag = str(chp) + '_' + str(page)
            tag_address[tag] = pic_url
            with open("err.txt", 'a') as e:
                e.writelines(tag + '\n' + tag_address[tag] + '\n')
            lock.release()
        print("success")
    except requests.exceptions.HTTPError:
        with open("html_error.log", "w+") as error:
            error.write(str(chp) + "_" + str(page))
    # finally:
    #     time.sleep(random.randint(1, 3))


if __name__ == '__main__':

    start_time = time.time()

    with open('html.txt', 'r') as f:
        htmls = f.readlines()


    def a(chp):
        page = 1
        while 1:
            print(str(chp + 1), "章", str(page), "页开始")
            addr = get_pic_addr(htmls[chp], chp + 1, page)
            if addr is None:
                break
            elif addr is -1:
                continue
            else:
                get_and_process_pic(addr, chp + 1, page)
            page = page + 1
        print(str(chp), "章爬完")


    # 线程池，多线程爬取
    chps = []
    for i in range(0, 53):
        chps.append(i)
    with ThreadPoolExecutor() as pool:
        pool.map(a, chps)
    print("All done")

    print(time.time() - start_time)
