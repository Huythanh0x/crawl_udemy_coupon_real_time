import json
import helper_class.date_time_helper as date_time_helper


def write_all_coupon_links(links_ls):
    links_ls_to_write = "\n".join(links_ls)
    with open('coupon_link.txt', 'w') as f:
        f.writelines(links_ls_to_write)


def get_all_coupon_links():
    with open('coupon_link.txt', 'r') as f:
        return [coupon_link.replace("\n", "") for coupon_link in f.readlines()]


def write_data_to_json(list_data_objects):
    list_data_objects = [
        data_object for data_object in list_data_objects if data_object != None]
    with open("udemy_coupon.json", "w") as f:
        f.writelines(json.dumps({"update_time": date_time_helper.get_update_time(
        ), "results": list_data_objects}, default=vars))
