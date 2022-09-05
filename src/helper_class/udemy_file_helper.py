import json


def write_all_coupon_links(links_ls):
    links_ls_to_write = "\n".join(links_ls)
    with open('coupon_link.txt', 'w') as f:
        f.writelines(links_ls_to_write)


def get_all_coupon_links():
    with open('coupon_link.txt', 'r') as f:
        return [coupon_link.replace("\n", "") for coupon_link in f.readlines()]


def write_data_to_json(list_data_objects):
    list_json_result = {"results": list_data_objects}
    udemy_coupon_json = json.dumps(list_json_result)
    with open('udemy_coupon.json', 'w') as f:
        f.writelines(udemy_coupon_json)
