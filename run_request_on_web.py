import os

for i in ["requests","bs4","html5lib","tqdm"]:
    print("installing",i)
    os.system(f"pip3 install {i} -U")
from functools import partial
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as bs
import json
import threading
import time
import traceback
import os
from datetime import datetime
from urllib.parse import parse_qs, unquote, urlsplit
from decimal import Decimal
from bs4 import BeautifulSoup as bs

PAGE_NTH = 6
tqdm = partial(tqdm, position=0, leave=True)

def discudemy():
    global du_links
    du_links = []
    big_all = []
    head = {
    "Accept-Language" : "en-US,en;q=0.5",
    "User-Agent": "Defined",
    }

    for page in range(1, PAGE_NTH):
        r = requests.get("https://www.discudemy.com/all/" + str(page), headers=head)
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