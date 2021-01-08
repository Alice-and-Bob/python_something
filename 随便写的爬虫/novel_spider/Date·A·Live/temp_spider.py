import requests
from bs4 import BeautifulSoup

f = open("temp.txt", "w+", encoding="utf-8")
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
url = "http://www.qinxiaoshuo.com/book/DATE%20A%20LIVE%e7%ba%a6%e4%bc%9a%e5%a4%a7%e4%bd%9c%e6%88%98"
req = requests.get(url, headers=head).text
soup = BeautifulSoup(req, "html.parser")
a = soup.find_all(name="a")
for i in a:
    f.write(str(i))
    f.write('\n')
