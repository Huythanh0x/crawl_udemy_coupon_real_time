import os

# for i in ["requests","bs4","html5lib","tqdm"]:
#     print("installing",i)
#     os.system(f"pip3 install {i} -U")

from functools import partial
from tqdm import tqdm
tqdm = partial(tqdm, position=0, leave=True)

import json
import threading
import time
import traceback
from urllib.parse import parse_qs, unquote, urlsplit
from decimal import Decimal
import requests
from bs4 import BeautifulSoup as bs

PAGE_NTH = 6

###############################################################################

def discudemy():
    global du_links
    du_links = []
    big_all = []
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
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


def udemy_freebies():
    global uf_links
    uf_links = []
    big_all = []

    for page in range(1, PAGE_NTH):
        r = requests.get(
            "https://www.udemyfreebies.com/free-udemy-courses/" + str(page)
        )
        soup = bs(r.content, "html5lib")
        all = soup.find_all("div", "coupon-name")
        big_all.extend(all)
    uf_bar = tqdm(total=len(big_all), desc="Udemy Freebies")

    for index, items in enumerate(big_all):
        uf_bar.update(1)
        title = items.a.text
        url = bs(requests.get(items.a["href"]).content, "html5lib").find(
            "a", class_="button-icon"
        )["href"]
        link = requests.get(url).url
        uf_links.append(link)
    uf_bar.close()


def tutorialbar():

    global tb_links
    tb_links = []
    big_all = []

    for page in range(1, PAGE_NTH):
        r = requests.get("https://www.tutorialbar.com/all-courses/page/" + str(page))
        soup = bs(r.content, "html5lib")
        all = soup.find_all(
            "div", class_="content_constructor pb0 pr20 pl20 mobilepadding"
        )
        big_all.extend(all)
    tb_bar = tqdm(total=len(big_all), desc="Tutorial Bar")

    for index, items in enumerate(big_all):
        tb_bar.update(1)
        title = items.a.text
        url = items.a["href"]

        r = requests.get(url)
        soup = bs(r.content, "html5lib")
        link = soup.find("a", class_="btn_offer_block re_track_btn")["href"]
        if "www.udemy.com" in link:
            tb_links.append(link)
    tb_bar.close()


def real_discount():

    global rd_links
    rd_links = []
    big_all = []

    for page in range(1, PAGE_NTH):
        r = requests.get("https://app.real.discount/stores/Udemy?page=" + str(page))
        soup = bs(r.content, "html5lib")
        all = soup.find_all("div", class_="col-xl-4 col-md-6")
        big_all.extend(all)
    rd_bar = tqdm(total=len(big_all), desc="Real Discount")

    for index, items in enumerate(big_all):
        rd_bar.update(1)
        title = items.h3.text
        url = "https://app.real.discount" + items.a["href"]
        r = requests.get(url)
        soup = bs(r.content, "html5lib")
        try:
            link = soup.select_one("a[href^='https://www.udemy.com']")["href"]
            rd_links.append(link)
        except:
            pass
    rd_bar.close()


def idcoupons():

    global idc_links
    idc_links = []
    big_all = []
    for page in range(1, PAGE_NTH):
        r = requests.get(
            "https://idownloadcoupon.com/product-category/udemy-2/page/" + str(page)
        )
        soup = bs(r.content, "html5lib")
        all = soup.find_all("a", attrs={"class": "button product_type_external"})
        big_all.extend(all)
    idc_bar = tqdm(total=len(big_all), desc="IDownloadCoupons")

    for index, item in enumerate(big_all):
        idc_bar.update(1)
        title = item["aria-label"]
        link = unquote(item["href"]).split("url=")
        try:
            link = link[1]
        except IndexError:
            link = link[0]
        if link.startswith("https://www.udemy.com"):
            idc_links.append(link)
    idc_bar.close()

def enext() -> list:
    en_links = []
    r = requests.get("https://e-next.in/e/udemycoupons.php")
    soup = bs(r.content, "html.parser")
    big_all = soup.find_all("p", {"class": "p2"})
    big_all.pop(0)
    en_bar = tqdm(total=len(big_all), desc="E-next")
    for i in big_all:
        en_bar.update(1)
        try:
            link = i.a["href"]
            en_links.append(link)
        except:
            pass

    en_bar.close()



def create_scrape_obj():
    funcs = {
        "Discudemy": threading.Thread(target=discudemy, daemon=True),
        "Udemy Freebies": threading.Thread(target=udemy_freebies, daemon=True),
        "Tutorial Bar": threading.Thread(target=tutorialbar, daemon=True),
        "Real Discount": threading.Thread(target=real_discount, daemon=True),
        "IDownloadCoupons": threading.Thread(target=idcoupons, daemon=True),
        "E-next": threading.Thread(target=enext, daemon=True),
    }
    return funcs


####################################################################

def get_course_id(url):
    r = requests.get(url, allow_redirects=False)
    if r.status_code in (404, 302, 301):
        return False
    if "/course/draft/" in url:
        return False
    soup = bs(r.content, "html5lib")

    try:
        courseid = soup.find(
            "div",
            attrs={"data-content-group": "Landing Page"},
        )["data-course-id"]
    except:
        courseid = soup.find(
            "body", attrs={"data-module-id": "course-landing-page/udlite"}
        )["data-clp-course-id"]
        # with open("problem.txt","w",encoding="utf-8") as f:
        # f.write(str(soup))
    return courseid


def get_course_coupon(url):
    query = urlsplit(url).query
    params = parse_qs(query)
    try:
        params = {k: v[0] for k, v in params.items()}
        return params["couponCode"]
    except:
        return ""

#####################################################

def course_landing_api(courseid):
    r = s.get(
        "https://www.udemy.com/api-2.0/course-landing-components/"
        + courseid
        + "/me/?components=purchase"
    ).json()
    try:
        purchased = r["purchase"]["data"]["purchase_date"]
    except:
        purchased = False
    try:
        amount = r["purchase"]["data"]["list_price"]["amount"]
    except:
        print(r["purchase"]["data"])

    return  purchased, Decimal(amount)


def main():
    try:
        links_ls = []
        for index in all_functions:
            all_functions[index].start()
            time.sleep(0.09)
        for t in all_functions:
            all_functions[t].join()
        time.sleep(1)

        for link_list in [
            "du_links",
            "uf_links",
            "tb_links",
            "rd_links",
            "cv_links",
            "idc_links",
            "en_links",
        ]:
            try:
                links_ls += eval(link_list)
            except:
                pass

        links_ls = [x for x in links_ls if "couponCode=" in x]
        links_ls = set(links_ls)
        write_all_coupon_links(links_ls)
        print(f"length is {len(links_ls)}")

    except:
        e = traceback.format_exc()
        print(e)

def write_all_coupon_links(links_ls):
    links_ls_to_write = "\n".join(links_ls)
    with open('coupon_link.txt','w') as f:
        f.writelines(links_ls_to_write)

############## MAIN ############# MAIN############## MAIN ############# MAIN ############## MAIN ############# MAIN ###########

all_functions = create_scrape_obj()
tm = threading.Thread(target=main, daemon=True)
tm.start()
tm.join()