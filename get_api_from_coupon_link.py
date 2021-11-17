import requests

from bs4 import BeautifulSoup as bs
import json
import random
import re
import os
import threading
import time
import traceback
from urllib.parse import parse_qs, unquote, urlsplit
from decimal import Decimal
import requests
from bs4 import BeautifulSoup as bs

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


def coupon_status(course_id,coupon_code):
    url_check_status_coupons = f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}/me/?couponCode={coupon_code}&components=deal_badge,discount_expiration,gift_this_course,price_text,purchase,recommendation,redeem_coupon,cacheable_deal_badge,cacheable_discount_expiration,cacheable_price_text,cacheable_buy_button,buy_button,buy_for_team,cacheable_purchase_text,cacheable_add_to_cart,money_back_guarantee,instructor_links,incentives_context,top_companies_notice_context,curated_for_ufb_notice_context,sidebar_container,purchase_tabs_context,subscribe_team_modal_context,lifetime_access_context,available_coupons"
    r = requests.get(url_check_status_coupons, allow_redirects=False)
    # print(url_check_status_coupons)
    if r.status_code in (404, 302, 301):
        return False 
    content_html = r.content.decode("utf-8")
    if "Not found" in content_html:
        print(f"NOT FOUND {url_check_status_coupons}")
    price,price_string,preview_img,preview_video,duration,end_day = get_data_coupon(content_html)
    return price,price_string,preview_img,preview_video,duration,end_day

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
        end_day = 0
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
    return price,price_string,preview_img,preview_video,duration,end_day

def course_status(course_id):
    url_check_course_status = f"https://www.udemy.com/api-2.0/courses/{course_id}/?fields[course]=title,context_info,primary_category,primary_subcategory,avg_rating_recent,visible_instructors,locale,estimated_content_length,num_subscribers,num_reviews,description,headline,instructional_level"
    # url_check_course_status = f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}/me/?components=deal_badge,discount_expiration,gift_this_course,price_text,purchase,recommendation,redeem_coupon,cacheable_deal_badge,cacheable_discount_expiration,cacheable_price_text,cacheable_buy_button,buy_button,buy_for_team,cacheable_purchase_text,cacheable_add_to_cart,money_back_guarantee,instructor_links,incentives_context,top_companies_notice_context,curated_for_ufb_notice_context,sidebar_container,purchase_tabs_context,subscribe_team_modal_context,lifetime_access_context,available_coupons,price_text,deal_badge,discount_expiration,redeem_coupon,gift_this_course,base_purchase_section,purchase_tabs_context,subscribe_team_modal_context,lifetime_access_context" 
    r = requests.get(url_check_course_status, allow_redirects=False)
    print(url_check_course_status)
    if r.status_code in (404, 302, 301):
        return False
    content_html = r.content.decode("utf-8") 
    category,sub_category,course_title,level,author,content_length,rating,number_reviews,students,coupon_code,language,headline,description = get_data_course(content_html)
    return category,sub_category,course_title,level,author,content_length,rating,number_reviews,students,coupon_code,language,headline,description

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
    rating = round(float(rating),1)
    number_reviews = my_json['num_reviews']
    headline = my_json['headline']
    description = my_json['description']
    level = my_json['instructional_level']
    return category,sub_category,course_title,level,author,content_length,rating,number_reviews,students,coupon_code,language,headline,description

try:
    os.remove("final_api.csv")
    os.remove("final_api.json")
    os.remove("error.log")
except:
    pass

with open('coupon_link.txt','r') as f:
    all_link = f.readlines()
    
list_object = []

for coupon_link in all_link:
    _,coupon_code = coupon_link.split('/?couponCode=')
    coupon_link = coupon_link.replace('\n','')
    coupon_code = coupon_code.replace('\n','')
    course_id = get_course_id(coupon_link)

    price,price_string,preview_img,preview_video,duration,end_day = coupon_status(course_id,coupon_code)
    category,sub_category,course_title,level,author,content_length,rating,number_reviews,students,_,language,headline,description = course_status(course_id)
    if int(price) == 0 and end_day != 0:
        # print(course_title)
        with open('final_api.csv','a') as f:
            f.writelines(f"{course_id},{category},{sub_category},{course_title},{level},{author},{duration},{rating},{rating},{number_reviews},{students},{coupon_code},{preview_img},{coupon_link},{end_day},{headline},{description},{preview_video}\n")
        coupon_object = {'course_id':f"{course_id}",'category': f"{category}",'sub_category':f"{sub_category}",'title':f"{course_title}",'level':f"{level}",'author':f"{author}",'duration':f"{duration}",'rating':f"{rating}",'reviews':f"{number_reviews}",'students':f"{students}",'coupon_code':f"{coupon_code}",'preview_img':f"{preview_img}",'coupon_link':f"{coupon_link}",'end_day':f"{end_day}",'headline':f"{headline}",'description':f"{description}",'preview_video':f"{preview_video}"}
        list_object.append(coupon_object)

    else:
        with open("error.log",'a') as f:
            f.writelines(f"{coupon_link}\n")

list_json_result = {"results":list_object}

final_json = json.dumps(list_json_result)

with open('final_api.json','w') as f:
    f.writelines(final_json)