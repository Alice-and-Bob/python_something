# 调用api爬取整个up的视频简介并储存下来。全部视频av号也是用api爬。
# https://github.com/fython/BilibiliAPIDocs
# http://docs.kaaass.net/showdoc/web/#/2?page_id=3

# https://api.kaaass.net/biliapi/video/info使用这个API来返回视频信息
# http://docs.kaaass.net/showdoc/web/#/2?page_id=14 这个页面是API的接口描述信息

# http://docs.kaaass.net/showdoc/web/#/2?page_id=106
# https://api.kaaass.net/biliapi/user/contribute
# 这个API传入用户UID来获取用户全部投稿的视频信息，可以获取到av号但是无法获得视频简介

import requests
import json
import time


def get_av_num():
    # 用途：获得up主个人主页投稿数据，爬取到个人所有投稿的av号
    # 参数：无
    # 返回：list类型的av号集合
    API = "https://api.kaaass.net/biliapi/user/contribute"
    payload = {'id': '1523132',
               'page': '1',
               'pageCount': '10'  # 一页默认爬取9个视频数据
               }
    avs = []
    for p in range(1, 11):  # range()的范围是，[a, b)
        payload['page'] = p
        r = requests.get(API, params=payload)
        r.encoding = r.apparent_encoding
        if r.status_code is not 200:
            print("Error occur!")
        else:

            try:
                txt = json.loads(r.text)  # loads()方法用于反序列化一串json字符串；load()方法用于一个json文件
                for i in range(0, len(txt['data'])):
                    avs.append(txt['data'][i]['id'])
            except json.decoder.JSONDecodeError as noerror:
                print("Oops! Something bad happened!")
    return avs


def get_msg(av):
    # 用途：根据传入的av号调用API来获得视频的简介部分，使用json解析并存储下来
    # 参数：av：str类型，标明要爬取的视频号
    # 返回：无
    API = "https://api.kaaass.net/biliapi/video/info"
    payload = {"id": av}
    r = requests.get(API, params=payload)
    r.encoding = r.apparent_encoding

    with open("南北.txt", "a", encoding='utf-8') as f:
        try:
            json_array = json.loads(r.text)
            video_msg = str(json_array['data']['description'])
            f.write(video_msg)
            f.write("\n\n\n\n\n")

        except json.decoder.JSONDecodeError as noerror:
            print("只有会员知道的世界~")
            f.write("av" + str(av) + "是只有会员才能知道的世界~")


if __name__ == '__main__':
    avs = get_av_num()
    # print('zzz')
    for av in avs:
        get_msg(av)
        print('av' + str(av) + 'Done!')
        time.sleep(0.1)
    print("ALL Done!")
