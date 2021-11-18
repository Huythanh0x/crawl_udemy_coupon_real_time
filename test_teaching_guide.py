import requests
import json
def teaching_guide():
    global tg_links
    pass
    my_json = requests.get("https://teachinguide.azure-api.net/course-coupon?sortCol=featured&sortDir=DESC&length=100&page=1&inkw=&discount=100&language=").json()
    list_object_coupon = my_json['results']
    tg_links = [coupon["CouponLink"] for coupon in list_object_coupon]

teaching_guide()