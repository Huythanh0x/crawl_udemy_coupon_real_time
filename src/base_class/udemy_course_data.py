import helper_class.udemy_api_helper as udemy_api_helper


class UdemyCourseData():
    def __init__(self, coupon_url) -> None:
        self.coupon_url = coupon_url
        self.course_id = udemy_api_helper.get_course_id(self.coupon_url)
        self.coupon_code = udemy_api_helper.get_coupon_code(self.coupon_url)

    def __str__(self) -> str:
        return f"{self.course_id} {self.coupon_code} {self.coupon_url}"

    def get_full_course_data(self):
        price, preview_img, preview_video, expired_date,uses_remaining = udemy_api_helper.get_coupon_status(
            self.course_id, self.coupon_code)
        # if int(price) == 0: return self.course_id,self.coupon_url,price,self.coupon_code,expired_date,None,None,None,None,None,None,None,None,None, preview_img,None,None,None,None,None
        category, sub_category, course_title, level, author, content_length, rating, number_reviews, students, language, headline, description = udemy_api_helper.get_course_status(
            self.course_id)
        return self.course_id, self.coupon_url, price, self.coupon_code, expired_date,uses_remaining, course_title, headline, description, author, category, sub_category, level, content_length, preview_img, preview_video, number_reviews, students, rating, language
