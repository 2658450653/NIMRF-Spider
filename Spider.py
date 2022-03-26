import os
import random
import re
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from monopt.insert import insert, flush

from pathlib import Path

items = []

"""
@author: lzw
@date: 2021-10-24
This Spider Program is adapted to NIMRF database website, so there are many module fit the website
therefore they maybe are not fit in other website. 
"""

"""
Request Head: contain some message to verify identify
"""
header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'
}

"""
User Agent: decorate your real ip address in order to enter any internet gate
(1) its first method for avoid Crawler prevention strategy, but no enough
"""
user_agent = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

data = {
    "pageNo": 1,
    "pageSize": 1000,
    "zym": None,
    "office.id": None,
    "cd": None,
    "zyglbm.id": None,
    "zydlId": None
}

root = "http://www.nimrf.net.cn/"


def loadStartPage(file):
    return open(file, encoding="utf-8").read()


start = None

"""
its a entrance for dfs algorithm function, in order to deal with the border situation
"""

# pwd = "/dev/lzw/dataset/Rock/"
pwd = "."


def entrance(spage: BeautifulSoup, level=0):
    li = spage.find("li", {"class": f"level{level}"})
    pre = getSpanNamefromLi(li)
    dfs(li, pre=pwd + pre, level=level + 1)


def getSpanNamefromLi(li: BeautifulSoup):
    return li.find("span", {"id": f"{li.get('id')}_span"}).text


def dfs(li: BeautifulSoup, level=0, pre="", path_dict={}):
    if not os.path.exists(str(pre).replace('(', '').replace(')', '')):
        pass
        #os.mkdir(str(pre).replace('(', '').replace(')', ''))
    sub_li_list = li.findAll("li", {"class": f"level{level}"})
    if len(sub_li_list) < 1:
        # print(li)
        # print('level:',level)
        print(pre)
        try:
            download_image_info(li, pre)
            pass
        except Exception as e:
            print("Connection is broken, now sleep 5 second then continue.")
            time.sleep(5)
            try:
                download_image_info(li, pre)
            except Exception as e:
                print("Connection is broken, now sleep 5 second then continue.")
                time.sleep(5)
                download_image_info(li, pre)
        return
    for sub_li in sub_li_list:
        dfs(sub_li,
            pre=pre + "/" + getSpanNamefromLi(sub_li),
            level=level + 1)


def di_info(page_id, page_size, href, path, limit):
    count = 0
    print(f"page: {page_id}")
    data["pageNo"] = page_id
    next_page = requests.post(root + href, data=data,
                              verify=False, headers={'User-Agent': random.choice(user_agent)})
    next_page = BeautifulSoup(next_page.text, "lxml")
    if next_page is None:
        return
    tr_list = next_page.find("table", {"id": "contentTable"}).find("tbody").find_all("tr")
    for tr in tr_list:
        ref_id = re.search(string=str(tr), pattern=r"<td>(\w*)</td>").group(1)
        # <a href="/ept/detail?id=90078" title="石榴二辉橄榄岩" target="_blank">石榴二辉橄榄岩</a>
        name = re.search(string=str(tr), pattern=r'target="_blank" title="(.*)">')
        if name:
            name = name.group(1)
        # <td title="橄榄岩">橄榄岩</td>
        #nclass = re.search(string=str(tr), pattern=r'title=".*岩">(.*岩)</td>').group(1)
        # <td title="KCLK2">KCLK2</td>
        uid = tr.find_all("td")[-1].text
        print(path)
        item = {
            'src_code': uid,
            'src_id': ref_id,
            'name': name,
            'Class':{
                'Class_of_n': path.split('/')[3],
                'Class_of_m': path.split('/')[2],
                'Class_of_3': path.split('/')[1],
            }
        }
        insert(item)
        count += 1
        if count >= limit:
            print("limit")
            time.sleep(1)
            return
    flush()


def download_image_info(li: BeautifulSoup, path, limit=99999):
    href = li.find("a").get("href")
    # page = requests.get(root + href, headers={'User-Agent': random.choice(user_agent)})
    data["pageNo"] = 1
    next_page = requests.post(root + href, data=data,
                verify=False, headers={'User-Agent': random.choice(user_agent)})
    page = BeautifulSoup(next_page.text, "lxml")
    size = re.findall(string=str(page), pattern=r"\);\">(\d+)</a>")
    if len(size) < 1:
        page_size = 1
    else:
        page_size = eval(size[-1])
        print("page_size:", page_size)
    for page_id in range(1, page_size + 1):
        try:
            di_info(page_id, page_size, href, path, limit)
        except Exception as e:
            print("Connection is broken, now sleep 5 second then continue.")
            time.sleep(5)
            di_info(page_id, page_size, href, path, limit)
        time.sleep(0.5)


def download_image(li: BeautifulSoup, path, limit=99999):
    global items
    count = 0
    href = li.find("a").get("href")
    page = requests.get(root + href, headers={'User-Agent': random.choice(user_agent)})
    page = BeautifulSoup(page.text, "lxml")
    size = re.findall(string=str(page), pattern=r"\);\">(\d+)</a>")
    if len(size) < 1:
        page_size = 1
    else:
        page_size = eval(size[-1])
    for page_id in range(1, page_size + 1):
        data["pageSize"] = page_size
        data["pageNo"] = page_id
        next_page = requests.post(root + href, data=data,
                                  verify=False, headers={'User-Agent': random.choice(user_agent)})
        next_page = BeautifulSoup(next_page.text, "lxml")
        if next_page is None:
            return
        tr_list = next_page.find("table", {"id": "contentTable"}).find("tbody").find_all("tr")
        for tr in tr_list:
            ref_id = re.search(string=str(tr), pattern=r"<td>(\w*)</td>").group(1)
            ref_single = tr.find("a").get("href")
            single_page = requests.get(root + ref_single, headers={'User-Agent': random.choice(user_agent)})
            time.sleep(0.5)
            if single_page.text is None:
                return
            img_page = BeautifulSoup(single_page.text, "lxml")
            if img_page is None:
                return
            try:
                img_href = img_page.find("table", {"id": "tpzlTb"}).find("a").get("href")
            except Exception as e:
                # print(e)
                return
            type_img = img_href.split('.')[-1]
            if os.path.exists(path + "/" + ref_id + f'.{type_img}') is False:
                # set max retries
                s = requests.Session()
                s.mount('http://', HTTPAdapter(max_retries=3))
                s.mount('https://', HTTPAdapter(max_retries=3))
                # resp = requests.get(root + img_href, headers={'User-Agent': random.choice(user_agent)})

                file_p = path + "/" + ref_id + f'.{type_img}'

                # db[ref_id] = str(file_p)
                item = {
                    '_id': ref_id,
                    'name': path.split('/')[-1],
                    'Class_of_3': path.split('/')[-3],
                    'Class_of_n': path.split('/')[-2],
                }
                insert(item)
                # time.sleep(0.1)
                # print(res)

                # with open(str(file_p).replace('(', '').replace(')', ''), "wb") as f:
                #     f.write(resp.content)
                #     f.flush()
                # print(f"save image:{root + img_href},{path}+/+{ref_id}.{type_img} successfully!")
                if count % 50 == 0:
                    print(f"loading ...  {count}")
            count += 1
            # if count % 50 == 0:
            #     print(count)
            if count >= limit:
                print("limit")
                time.sleep(1)
                return

    img_href = page.find("table", {"id": "contentTable"}).findAll("a")
    # print(img_href)


"""
about documents:
document.html ---> Rock Data start page
document1.html ---> Mineral Data start page
document2.html ---> Ore Data start page
"""
if __name__ == "__main__":
    soup = BeautifulSoup(loadStartPage("document_cug.html"), "lxml")
    start = soup
    entrance(start, 0)
    # print(db)
    # from json_db import *
    #
    # #db = load("ref_id.txt")
    # # db = {v: k for k, v in db.items()}
    # save(db, "ref_id.txt")
    # print(db['2342C0001200001021'])
