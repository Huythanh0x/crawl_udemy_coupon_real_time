import requests
from bs4 import BeautifulSoup as bs
import json


def get_course_id(coupon_url):
    r = requests.get(coupon_url, allow_redirects=True)
    if r.status_code in (404, 302, 301) or "/course/draft/" in r.url:
        return False
    soup = bs(r.content, "html5lib")
    try: 
        course_id = soup.find(
                "body", attrs={"id": "udemy"}
            )["data-clp-course-id"]
    except:
        course_id = soup.find(
                "div", attrs={"class": "sidebar-container-position-manager"}
            ).find('img')["src"].split('_')[0].split('/')[-1]
    return course_id


def get_coupon_code(coupon_url):
    return coupon_url.split('/?couponCode=')[1]


def get_coupon_status(course_id, coupon_code):
    url_check_status_coupons = f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}/me/?couponCode={coupon_code}&components=deal_badge,discount_expiration,gift_this_course,price_text,purchase,recommendation,redeem_coupon,cacheable_deal_badge,cacheable_discount_expiration,cacheable_price_text,cacheable_buy_button,buy_button,buy_for_team,cacheable_purchase_text,cacheable_add_to_cart,money_back_guarantee,instructor_links,incentives_context,top_companies_notice_context,curated_for_ufb_notice_context,sidebar_container,purchase_tabs_context,subscribe_team_modal_context,lifetime_access_context,available_coupons"
    # print(url_check_status_coupons)
    r = requests.get(url_check_status_coupons, allow_redirects=False)
    if r.status_code in (404, 302, 301):
        return False
    content_html = r.content.decode("utf-8")
    # TODO NOT FOUND coupon
    # if "Not found" in content_html:
    #     print(f"NOT FOUND {url_check_status_coupons}")
    price, preview_img, preview_video, expired_date,uses_remaining = extract_data_coupon(
        content_html)
    return price, preview_img, preview_video, expired_date,uses_remaining


def extract_data_coupon(content_html):
    my_json = json.loads(content_html)
    try:
        price = my_json['price_text']['data']['pricing_result']['price']['amount']
    except:
        price = None
    try:
        expired_date = my_json['price_text']['data']['pricing_result']['campaign']['end_time']
    except:
        expired_date = 0
    try:
        preview_img = my_json['sidebar_container']['componentProps']['introductionAsset']['images']['image_750x422']
    except:
        preview_img = "null"
    try:
        preview_video = "https://www.udemy.com" + my_json['sidebar_container']['componentProps']['introductionAsset']['course_preview_path']
    except:
        preview_video = "null"
    uses_remaining = my_json['price_text']['data']['pricing_result']['campaign']['uses_remaining']
    return price, preview_img, preview_video, expired_date,uses_remaining


def get_course_status(course_id):
    url_check_course_status = f"https://www.udemy.com/api-2.0/courses/{course_id}/?fields[course]=title,context_info,primary_category,primary_subcategory,avg_rating_recent,visible_instructors,locale,estimated_content_length,num_subscribers,num_reviews,description,headline,instructional_level"
    r = requests.get(url_check_course_status, allow_redirects=False)
    if r.status_code in (404, 302, 301):
        return False
    content_html = r.content.decode("utf-8")
    category, sub_category, course_title, level, author, content_length, rating, number_reviews, students, language, headline, description = extract_data_course(
        content_html)
    return category, sub_category, course_title, level, author, content_length, rating, number_reviews, students, language, headline, description


def extract_data_course(content_html):
    my_json = json.loads(content_html)
    course_title = my_json['title']
    headline = my_json['headline']
    description = my_json['description'].replace("\n", "")
    try:
        author = my_json['visible_instructors'][0]['title']
    except:
        author = "Unknown"
    try:
        category = my_json['primary_category']['title']
    except:
        category = "No category"
    try:
        sub_category = my_json['primary_subcategory']['title']
    except:
        sub_category = "No category"
    language = my_json['locale']['simple_english_title']
    level = my_json['instructional_level']
    students = my_json['num_subscribers']
    rating = round(float(my_json['avg_rating_recent']), 1)
    number_reviews = my_json['num_reviews']
    content_length = my_json['estimated_content_length']
    return category, sub_category, course_title, level, author, content_length, rating, number_reviews, students, language, headline, description
