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
    list_data_objects = pqdm(all_coupon_links[:10], execute_single_sing, n_jobs=8)
    udemy_file_helper.write_data_to_json(list_data_objects)
    total_bar.close()


def execute_single_sing(coupon_url):
    u = UdemyCourseData(coupon_url)
    course_id, coupon_url, price, coupon_code, expired_date, course_title, headline, description, author, category, sub_category, level, content_length, duration, preview_img, preview_video, number_reviews, students, rating, language = u.get_full_course_data()
    if int(price) == 0 and expired_date != 0:
        with open('udemy_coupon.csv', 'a') as f:
            f.writelines(f"{course_id},{category},{sub_category},{course_title},{level},{author},{duration},{rating},{rating},{number_reviews},{students},{coupon_code},{preview_img},{coupon_url},{expired_date},{headline},{description},{preview_video}\n")
        coupon_object = {'course_id': f"{course_id}", 'category': f"{category}", 'sub_category': f"{sub_category}", 'title': f"{course_title}", 'level': f"{level}", 'author': f"{author}", 'duration': f"{duration}", 'rating': f"{rating}", 'reviews': f"{number_reviews}",
                         'students': f"{students}", 'coupon_code': f"{coupon_code}", 'preview_img': f"{preview_img}", 'coupon_link': f"{coupon_url}", 'expired_date': f"{expired_date}", 'headline': f"{headline}", 'description': f"{description}", 'preview_video': f"{preview_video}"}
        return coupon_object
    else:
        with open("error.log", 'a') as f:
            f.writelines(f"{coupon_url}\n")
            return


start = time.time()
try:
    os.remove("udemy_coupon.csv")
    os.remove("coupon_link.txt")
    os.remove("udemy_coupon.json")
    os.remove("error.log")
except:
    pass
udemy_coupon_url_crawler.main()
execute_all_link()
print(f"It took {time.time()-start} second to crawl")
