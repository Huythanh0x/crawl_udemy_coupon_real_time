import json
with open('api_course_response.txt','r') as f:
    origin_json = f.readlines()[0]

# print(origin_json)
my_json = json.loads(origin_json)
# print(my_json)

course_title = my_json['title']
course_id = my_json['id']
author = my_json['visible_instructors'][0]['title']
students = my_json['num_subscribers']
category = my_json['primary_category']['title']
sub_category = my_json['primary_subcategory']['title']
language = my_json['locale']['simple_english_title']
content_length = my_json['estimated_content_length']
rating = my_json['avg_rating_recent']
number_reviews = my_json['num_reviews']
head_line = my_json['headline']
description = my_json['description']

print(course_id)
print(course_title)
print(author)
print(students)
print(category)
print(language)
print(content_length)
print(rating)
print(sub_category)
print(head_line)
print(description)