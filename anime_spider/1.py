import requests
import urllib3
import time
import bs4
import re

url = "http://comic.kkkkdm.com/comiclist/2316/"
header = {
    'Host': 'v2.kukudm.com',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

proxies = {
    "https": "https://171.35.169.162:9999",
}

requests.DEFAULT_RETRIES = 50
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
print(time.time())
with requests.session() as req:
    req.keep_alive = False
    res = req.get(url, verify=False)
    print("1")
    res.encoding = res.apparent_encoding
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    temp = soup.find_all("a")
    print("2")
    tempp = []
    for i in temp:
        t = str(i)
        if "comic3" in t:
            tempp.append(i)
    # print(tempp)
    r = r'http:.*htm'
    temppp = []
    for ii in tempp:
        temppp.append(re.findall(r, str(ii)))
    with open("a.txt", 'w') as f:
        for iii in temppp:
            f.writelines(str(iii))
            f.writelines('\n')
print("end")
