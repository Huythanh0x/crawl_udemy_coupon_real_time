import requests
import json
import os

# for i in ["requests","bs4","html5lib","tqdm"]:
#     print("installing",i)
#     os.system(f"pip3 install {i} -U")


from functools import partial
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as bs
import json
import threading
import time
import traceback
import os
import pytz
from datetime import datetime
from urllib.parse import parse_qs, unquote, urlsplit
from decimal import Decimal

from bs4 import BeautifulSoup as bs


PAGE_NTH = 6

def real_discount():

    global rd_links
    rd_links = []
    big_all = []

    for page in range(1, PAGE_NTH):
        r = requests.get(
            "https://app.real.discount/stores/Udemy?page=" + str(page))
        soup = bs(r.content, "html5lib")
        all = soup.find_all("div", class_="col-xl-4 col-md-6")
        big_all.extend(all)

    for index, items in enumerate(big_all):
        url = "https://app.real.discount" + items.a["href"]
        r = requests.get(url)
        soup = bs(r.content, "html5lib")
        try:
            link = soup.find("div",class_="col-xs-12 col-md-12 col-sm-12 text-center").a['href']
            rd_links.append(link.strip())
            print(link.strip())
            with open('real_discount.txt','a') as f:
                f.writelines(f'{link.strip()}\n')
        except:
            pass
real_discount()