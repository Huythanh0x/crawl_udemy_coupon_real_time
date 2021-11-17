from decimal import Decimal
from urllib.parse import parse_qs, unquote, urlsplit
from datetime import datetime
import traceback
import time
import threading
import json
from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm
from functools import partial
import os

for i in ["requests", "bs4", "html5lib", "tqdm"]:
    print("installing", i)
    os.system(f"pip3 install {i} -U")

PAGE_NTH = 6
tqdm = partial(tqdm, position=0, leave=True)


def discudemy():
    global du_links
    du_links = []
    big_all = []
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    proxyDict = {
        'http': "add http proxy",
        'https': "add https proxy"
    }

    for page in range(1, PAGE_NTH):
        r = requests.get("https://www.discudemy.com/all/" +
                         str(page), headers=head, proxies=proxyDict)
        soup = bs(r.content, "html5lib")
        all = soup.find_all("section", "card")
        big_all.extend(all)
    du_bar = tqdm(total=len(big_all), desc="Discudemy")
    for index, items in enumerate(big_all):
        du_bar.update(1)
        try:
            title = items.a.text
            url = items.a["href"]

            r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")
            next = soup.find("div", "ui center aligned basic segment")
            url = next.a["href"]
            r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")
            du_links.append(soup.find("div", "ui segment").a["href"])
        except AttributeError:
            continue
    du_bar.close()


discudemy()
