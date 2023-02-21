from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as bs
import threading
import time
import helper_class.udemy_file_helper as udemy_file_helper
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def discudemy():
    global disc_udemy_links
    disc_udemy_links = []
    big_all = []
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    for page in range(1, MAX_PAGE_LOAD):
        r = requests.get("https://www.discudemy.com/all/" +
                         str(page), headers=head)
        soup = bs(r.content, "html5lib")
        all = soup.find_all("section", "card")
        big_all.extend(all)
    du_bar = tqdm(total=len(big_all), desc="Discudemy")
    for items in big_all:
        du_bar.update(1)
        try:
            url = items.a["href"]
            r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")
            next = soup.find("div", "ui center aligned basic segment")
            url = next.a["href"]
            r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")
            disc_udemy_links.append(
                soup.find("div", "ui segment").a["href"].strip())
        except:
            pass
    du_bar.close()
    return disc_udemy_links


def udemy_freebies():
    global udemy_freebies_links
    udemy_freebies_links = []
    big_all = []
    for page in range(1, MAX_PAGE_LOAD):
        r = requests.get(
            "https://www.udemyfreebies.com/free-udemy-courses/" + str(page)
        )
        soup = bs(r.content, "html5lib")
        all = soup.find_all("div", "coupon-name")
        big_all.extend(all)
    uf_bar = tqdm(total=len(big_all), desc="Udemy Freebies")
    for items in big_all:
        uf_bar.update(1)
        url_to_page = items.find("a")["href"]
        r = requests.get(url_to_page)
        url = bs(r.content, "html5lib").find("a", class_="button-icon")["href"]
        link = requests.get(url).url
        udemy_freebies_links.append(link.strip())
    uf_bar.close()
    return udemy_freebies_links


def tutorialbar():
    global tutorial_bar_links
    tutorial_bar_links = []
    big_all = []
    for page in range(1, MAX_PAGE_LOAD):
        r = requests.get(
            "https://www.tutorialbar.com/all-courses/page/" + str(page))
        soup = bs(r.content, "html5lib")
        all = soup.find_all(
            "div", class_="content_constructor pb0 pr20 pl20 mobilepadding"
        )
        big_all.extend(all)
    tb_bar = tqdm(total=len(big_all), desc="Tutorial Bar")
    for items in big_all:
        tb_bar.update(1)
        url = items.a["href"]
        r = requests.get(url)
        soup = bs(r.content, "html5lib")
        link = soup.find("a", class_="btn_offer_block re_track_btn")["href"]
        if "www.udemy.com" in link:
            tutorial_bar_links.append(link.strip())
    tb_bar.close()
    return tutorial_bar_links


def real_discount():
    global real_discount_links
    real_discount_links = []
    big_all = []
    for page in range(1, MAX_PAGE_LOAD):
        r = requests.get(
            "https://app.real.discount/stores/Udemy?page=" + str(page))
        soup = bs(r.content, "html5lib")
        all = soup.find_all("div", class_="col-xl-4 col-md-6")
        big_all.extend(all)
    rd_bar = tqdm(total=len(big_all), desc="Real Discount")
    for items in big_all:
        rd_bar.update(1)
        url = "https://app.real.discount" + items.a["href"]
        r = requests.get(url)
        soup = bs(r.content, "html5lib")
        try:
            link = soup.find(
                "div", class_="col-xs-12 col-md-12 col-sm-12 text-center").a['href']
            link = link.replace(
                "http://click.linksynergy.com/fs-bin/click?id=bnwWbXPyqPU&subid=&offerid=323058.1&type=10&tmpid=14537&RD_PARM1=", "")
            real_discount_links.append(link.strip())
        except:
            pass
    rd_bar.close()
    return real_discount_links


def idcoupons():

    global idc_links
    idc_links = []
    big_all = []
    for page in range(1, MAX_PAGE_LOAD):
        r = requests.get(
            "https://idownloadcoupon.com/page/" +
            str(page)
        )
        soup = bs(r.content, "html5lib")
        all = soup.find_all(
            "a", attrs={"class": "product_type_external"})
        big_all.extend(all)
    idc_bar = tqdm(total=len(big_all), desc="IDownloadCoupons")
    for index, item in enumerate(big_all):
        idc_bar.update(1)
        link = str(item["href"]).split("ulp=")
        try:
            link = link[1]
        except IndexError:
            link = link[0]
        link = unquote(link)
        if link.startswith("https://www.udemy.com"):
            idc_links.append(link.strip())
    idc_bar.close()
    return idc_links


def enext():
    global en_links
    en_links = []
    r = requests.get("https://jobs.e-next.in/public/assets/data/udemy.json")
    en_links.extend([item['site'] for item in r.json()])
    return en_links

def create_scrape_obj():
    funcs = {
        "Discudemy": threading.Thread(target=discudemy, daemon=True),
        "Udemy Freebies": threading.Thread(target=udemy_freebies, daemon=True),
        "Tutorial Bar": threading.Thread(target=tutorialbar, daemon=True),
        "Real Discount": threading.Thread(target=real_discount, daemon=True),
        "IDownloadCoupons": threading.Thread(target=idcoupons, daemon=True),
        "E-next": threading.Thread(target=enext, daemon=True)
    }
    return funcs


def start_crawling():
    all_functions = create_scrape_obj()
    links_ls = []
    for index in all_functions:
        all_functions[index].start()
    for t in all_functions:
        all_functions[t].join()
    for link_list in [
        "disc_udemy_links",
        "udemy_freebies_links",
        "tutorial_bar_links",
        "real_discount_links",
        "idc_links",
        "en_links"
    ]:
        try:
            links_ls += eval(link_list)
        except:
            print(f"ERROR AT eval(link_list)")
    links_ls = [x for x in links_ls if "couponCode=" in x]
    for idx, url in enumerate(links_ls):
        if "/?couponCode=" not in url:
            url = url.replace("?couponCode=", "/?couponCode=")
            links_ls[idx] = url
        if "#" in url:
            url = url.split('#')[0]
            links_ls[idx] = url
    links_ls = set(links_ls)
    udemy_file_helper.write_all_coupon_links(links_ls)
    print(f"Length is {len(links_ls)}")


def main():
    tm = threading.Thread(target=start_crawling, daemon=True)
    tm.start()
    tm.join()


MAX_PAGE_LOAD = 6