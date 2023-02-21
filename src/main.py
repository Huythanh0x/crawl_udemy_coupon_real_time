import os
import time
import os
import os
import base_class.udemy_coupon_url_crawler as udemy_coupon_url_crawler
import helper_class.udemy_file_helper as udemy_file_helper
from base_class.udemy_course_data import UdemyCourseData
from tqdm import tqdm
from pqdm.processes import pqdm

def execute_all_link():
    all_coupon_links = udemy_file_helper.get_all_coupon_links()
    total_bar = tqdm(total=len(all_coupon_links), desc="LOAD DATA TO JSON")
    list_data_objects = pqdm(all_coupon_links, execute_single_sing, n_jobs=24)
    udemy_file_helper.write_data_to_json(list_data_objects)
    total_bar.close()


def execute_single_sing(coupon_url):
    u = UdemyCourseData(coupon_url)
    course_id, coupon_url, price, coupon_code, expired_date,uses_remaining, course_title, headline, description, author, category, sub_category, level, content_length, preview_img, preview_video, number_reviews, students, rating, language = u.get_full_course_data()
    if int(price) == 0 and expired_date != 0:
        with open('udemy_coupon.csv', 'a') as f:
            f.writelines(f"{course_id},{category},{sub_category},{course_title},{level},{author},{content_length},{rating},{rating},{number_reviews},{students},{coupon_code},{preview_img},{coupon_url},{expired_date},{uses_remaining},{headline},{description},{preview_video},{language}\n")
        coupon_object = {'course_id': f"{course_id}", 'category': f"{category}", 'sub_category': f"{sub_category}", 'title': f"{course_title}", 'content_length': f"{content_length}", 'level': f"{level}", 'author': f"{author}", 'rating': f"{rating}", 'reviews': f"{number_reviews}",
                         'students': f"{students}", 'coupon_code': f"{coupon_code}", 'preview_img': f"{preview_img}", 'coupon_link': f"{coupon_url}", 'expired_date': f"{expired_date}","uses_remaining":f"{uses_remaining}", 'headline': f"{headline}", 'description': f"{description}", 'preview_video': f"{preview_video}",'language': f"{language}"}
        return coupon_object
    else:
        with open("error.log", 'a') as f:
            f.writelines(f"{coupon_url}\n")
            return

def remove_old_files():
    try:
        os.remove("udemy_coupon.csv")
    except: pass
    try:
        os.remove("coupon_link.txt")
    except: pass
    try:
        os.remove("error.log")  
    except: pass
    try:
        os.remove("udemy_coupon.json")
    except: pass


start = time.time()
remove_old_files()
udemy_coupon_url_crawler.main()
execute_all_link()
print(f"It took {time.time()-start} second to crawl")