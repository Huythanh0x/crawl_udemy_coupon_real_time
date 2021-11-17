import json
with open('api_response.txt','r') as f:
    origin_json = f.readlines()[0]

# print(origin_json)
my_json = json.loads(origin_json)
# print(my_json)

price = my_json['price_text']['data']['pricing_result']['price']['amount']
price_string = my_json['price_text']['data']['pricing_result']['price']['price_string']
id_course = my_json['price_text']['data']['course_id']
coupon_code = my_json['price_text']['data']['pricing_result']['campaign']['code']
preview_img = my_json['sidebar_container']['componentProps']['introductionAsset']['preview_image_url']
preview_video = my_json['sidebar_container']['componentProps']['introductionAsset']['media_sources'][0]['src']
duration = my_json['sidebar_container']['componentProps']['incentives']['video_content_length']
# print(price,price_string,id_course,coupon_code,preview_img,preview_video,duration)
print(price)
print(price_string)
print(id_course)
print(coupon_code)
print(preview_video)
print(preview_img)
print(duration)