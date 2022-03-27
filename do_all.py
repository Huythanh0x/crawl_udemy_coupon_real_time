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
import pytz
from datetime import datetime
from urllib.parse import parse_qs, unquote, urlsplit
from bs4 import BeautifulSoup as bs

tqdm = partial(tqdm, position=0, leave=True)
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
        r = requests.get("https://www.discudemy.com/all/" +
                         str(page), headers=head)
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
            du_links.append(soup.find("div", "ui segment").a["href"].strip())
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
        uf_links.append(link.strip())
    uf_bar.close()


def tutorialbar():

    global tb_links
    tb_links = []
    big_all = []

    for page in range(1, PAGE_NTH):
        r = requests.get(
            "https://www.tutorialbar.com/all-courses/page/" + str(page))
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
            tb_links.append(link.strip())
    tb_bar.close()


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
    rd_bar = tqdm(total=len(big_all), desc="Real Discount")

    for index, items in enumerate(big_all):
        rd_bar.update(1)
        title = items.h3.text
        url = "https://app.real.discount" + items.a["href"]
        r = requests.get(url)
        soup = bs(r.content, "html5lib")
        try:
            # link = soup.select_one("a[href^='https://www.udemy.com']")["href"]
            link = soup.find("div",class_="col-xs-12 col-md-12 col-sm-12 text-center").a['href']
            link = link.replace("http://click.linksynergy.com/fs-bin/click?id=bnwWbXPyqPU&subid=&offerid=323058.1&type=10&tmpid=14537&RD_PARM1=","")
            rd_links.append(link.strip())
        except:
            pass
    rd_bar.close()


def teaching_guide():
    global tg_links
    my_json = requests.get(
        "https://teachinguide.azure-api.net/course-coupon?sortCol=featured&sortDir=DESC&length=100&page=1&inkw=&discount=100&language=").json()
    list_object_coupon = my_json['results']
    tg_links = [coupon["CouponLink"] for coupon in list_object_coupon]


def coursevania():

    global cv_links
    cv_links = []
    r = requests.get("https://coursevania.com/courses/")
    soup = bs(r.content, "html5lib")
    nonce = soup.find_all("script")[22].text[30:]
    nonce = json.loads(nonce.strip().strip(";"))["load_content"]
    r = requests.get(
        "https://coursevania.com/wp-admin/admin-ajax.php?&template=courses/grid&args={%22posts_per_page%22:%2230%22}&action=stm_lms_load_content&nonce="
        + nonce
        + "&sort=date_high"
    ).json()
    soup = bs(r["content"], "html5lib")
    all = soup.find_all(
        "div", attrs={"class": "stm_lms_courses__single--title"})
    cv_bar = tqdm(total=len(all), desc="Course Vania")

    for index, item in enumerate(all):
        cv_bar.update(1)
        title = item.h5.text
        r = requests.get(item.a["href"])
        soup = bs(r.content, "html5lib")
        cv_links.append(
            soup.find("div", attrs={"class": "stm-lms-buy-buttons"}).a["href"].strip())
    cv_bar.close()


def idcoupons():

    global idc_links
    idc_links = []
    big_all = []
    for page in range(1, PAGE_NTH):
        r = requests.get(
            "https://idownloadcoupon.com/product-category/udemy-2/page/" +
            str(page)
        )
        soup = bs(r.content, "html5lib")
        all = soup.find_all(
            "a", attrs={"class": "button product_type_external"})
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
            idc_links.append(link.strip())
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
            en_links.append(link.strip())
        except:
            pass

    en_bar.close()


def teaching_guide():
    global tg_links
    my_json = requests.get(
        "https://teachinguide.azure-api.net/course-coupon?sortCol=featured&sortDir=DESC&length=100&page=1&inkw=&discount=100&language=").json()
    list_object_coupon = my_json['results']
    tg_links = [coupon["CouponLink"] for coupon in list_object_coupon]


def create_scrape_obj():
    funcs = {
        "Udemy Freebies": threading.Thread(target=udemy_freebies, daemon=True),
        "Tutorial Bar": threading.Thread(target=tutorialbar, daemon=True),
        "Real Discount": threading.Thread(target=real_discount, daemon=True),
        "Course Vania": threading.Thread(target=coursevania, daemon=True),
        "IDownloadCoupons": threading.Thread(target=idcoupons, daemon=True),
        "E-next": threading.Thread(target=enext, daemon=True),
        "TeachinGuide": threading.Thread(target=teaching_guide, daemon=True),
    }
    # funcs = {
    #     "Discudemy": threading.Thread(target=discudemy, daemon=True),
    #     "Udemy Freebies": threading.Thread(target=udemy_freebies, daemon=True),
    #     "Tutorial Bar": threading.Thread(target=tutorialbar, daemon=True),
    #     "Real Discount": threading.Thread(target=real_discount, daemon=True),
    #     "Course Vania": threading.Thread(target=coursevania, daemon=True),
    #     "IDownloadCoupons": threading.Thread(target=idcoupons, daemon=True),
    #     "E-next": threading.Thread(target=enext, daemon=True),
    #     "TeachinGuide": threading.Thread(target=teaching_guide, daemon=True),
    # }
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
            "tg_links",
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
    with open('coupon_link.txt', 'w') as f:
        f.writelines(links_ls_to_write)


def coupon_status(course_id, coupon_code):
    url_check_status_coupons = f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}/me/?couponCode={coupon_code}&components=deal_badge,discount_expiration,gift_this_course,price_text,purchase,recommendation,redeem_coupon,cacheable_deal_badge,cacheable_discount_expiration,cacheable_price_text,cacheable_buy_button,buy_button,buy_for_team,cacheable_purchase_text,cacheable_add_to_cart,money_back_guarantee,instructor_links,incentives_context,top_companies_notice_context,curated_for_ufb_notice_context,sidebar_container,purchase_tabs_context,subscribe_team_modal_context,lifetime_access_context,available_coupons"
    r = requests.get(url_check_status_coupons, allow_redirects=False)
    # print(url_check_status_coupons)
    if r.status_code in (404, 302, 301):
        return 0, None, None, None, None, None
    content_html = r.content.decode("utf-8")
    if "Not found" in content_html:
        with open('not_found.log', 'a') as f:
            f.writelines(f"{url_check_status_coupons}\n")
        print(f"NOT FOUND {url_check_status_coupons}")
    price, price_string, preview_img, preview_video, duration, end_day = get_data_coupon(
        content_html)
    return price, price_string, preview_img, preview_video, duration, end_day


def get_data_coupon(content_html):
    # print("get status coupon")
    my_json = json.loads(content_html)
    try:
        price = my_json['price_text']['data']['pricing_result']['price']['amount']
    except:
        price = 1
    try:
        end_day = my_json['price_text']['data']['pricing_result']['campaign']['end_time']
    except:
        end_day = None
    try:
        price_string = my_json['price_text']['data']['pricing_result']['price']['price_string']
    except:
        price_string = "NOT FREE TODAY"
    try:
        preview_img = my_json['sidebar_container']['componentProps']['introductionAsset']['preview_image_url']
    except:
        preview_img = "null"
    try:
        preview_video = my_json['sidebar_container']['componentProps']['introductionAsset']['media_sources'][0]['src']
    except:
        preview_video = ""
    try:
        duration = my_json['sidebar_container']['componentProps']['incentives']['video_content_length']
    except:
        duration = "null"
    return price, price_string, preview_img, preview_video, duration, end_day


def course_status(course_id):
    url_check_course_status = f"https://www.udemy.com/api-2.0/courses/{course_id}/?fields[course]=title,context_info,primary_category,primary_subcategory,avg_rating_recent,visible_instructors,locale,estimated_content_length,num_subscribers,num_reviews,description,headline,instructional_level,,locale"
    # url_check_course_status = f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}/me/?components=deal_badge,discount_expiration,gift_this_course,price_text,purchase,recommendation,redeem_coupon,cacheable_deal_badge,cacheable_discount_expiration,cacheable_price_text,cacheable_buy_button,buy_button,buy_for_team,cacheable_purchase_text,cacheable_add_to_cart,money_back_guarantee,instructor_links,incentives_context,top_companies_notice_context,curated_for_ufb_notice_context,sidebar_container,purchase_tabs_context,subscribe_team_modal_context,lifetime_access_context,available_coupons,price_text,deal_badge,discount_expiration,redeem_coupon,gift_this_course,base_purchase_section,purchase_tabs_context,subscribe_team_modal_context,lifetime_access_context"
    r = requests.get(url_check_course_status, allow_redirects=False)
    print(url_check_course_status)
    if r.status_code in (404, 302, 301):
        return None, None, None, None, None, None, None, None, None, None, None, None, None
    content_html = r.content.decode("utf-8")
    category, sub_category, course_title, level, author, content_length, rating, number_reviews, students, coupon_code, language, headline, description,locale = get_data_course(
        content_html)
    return category, sub_category, course_title, level, author, content_length, rating, number_reviews, students, coupon_code, language, headline, description,locale


def get_data_course(content_html):
    # print("get data course")
    my_json = json.loads(content_html)
    course_title = my_json['title']
    try:
        author = my_json['visible_instructors'][0]['title']
    except:
        author = "Unknown"
    students = my_json['num_subscribers']
    category = my_json['primary_category']['title']
    sub_category = my_json['primary_subcategory']['title']
    language = my_json['locale']['simple_english_title']
    content_length = my_json['estimated_content_length']
    rating = my_json['avg_rating_recent']
    rating = round(float(rating), 1)
    number_reviews = my_json['num_reviews']
    headline = my_json['headline']
    description = my_json['description']
    level = my_json['instructional_level']
    locale = my_json['locale']['simple_english_title']
    return category, sub_category, course_title, level, author, content_length, rating, number_reviews, students, coupon_code, language, headline, description,locale

  ############## MAIN ############# MAIN############## MAIN ############# MAIN ############## MAIN ############# MAIN ###########

start  = time.time()

try:
    os.remove("coupon_link.txt")
    os.remove("final_api.json")
    os.remove("error.log")
except:
    pass

PAGE_NTH = 6
all_functions = create_scrape_obj()
tm = threading.Thread(target=main, daemon=True)
tm.start()
tm.join()

with open('coupon_link.txt', 'r') as f:
    all_link = set(f.readlines())

list_object = []

for coupon_link in all_link:
    _, coupon_code = coupon_link.split('couponCode=')
    coupon_link = coupon_link.replace('\n', '')
    coupon_code = coupon_code.replace('\n', '')
    try:
        course_id = get_course_id(coupon_link)
    except:
        continue
    price, price_string, preview_img, preview_video, duration, end_day = coupon_status(
        course_id, coupon_code)
    category, sub_category, course_title, level, author, content_length, rating, number_reviews, students, coupon_code, language, headline, description,locale = course_status(
        course_id)
    if int(price) == 0 and end_day != None and content_length != None:
        coupon_object = {'course_id': f"{course_id}", 'category': f"{category}", 'sub_category': f"{sub_category}", 'title': f"{course_title}", 'level': f"{level}", 'author': f"{author}", 'duration': f"{duration}", 'rating': f"{rating}", 'reviews': f"{number_reviews}",
                         'students': f"{students}", 'coupon_code': f"{coupon_code}", 'preview_img': f"{preview_img}", 'coupon_link': f"{coupon_link}", 'end_day': f"{end_day}", 'headline': f"{headline}", 'description': f"{description}", 'preview_video': f"{preview_video}",'locale':f"{locale}"}
        list_object.append(coupon_object)
    else:
        with open("error.log", 'a') as f:
            f.writelines(f"{coupon_link}\n")


time_zone = pytz.timezone('Europe/Madrid')
last_time_update = datetime.now(time_zone)
last_time_update = last_time_update.strftime("%Y-%m-%d %H:%M:%S")

list_json_result = {
    "last_time_update": last_time_update, "results": list_object}

final_json = json.dumps(list_json_result)

with open('final_api.json', 'w') as f:
    f.writelines(final_json)

end = time.time()
print(f"It took {end-start} seconds to update data json")