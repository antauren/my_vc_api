import os
import shutil
import random
from dotenv import dotenv_values

from vc import load_photo_to_vc_group_wall
from utils import download_file, load_json_file, get_file_name_from_url

TMP_DIR = 'tmp'
TMP_JSON_PATH = os.path.join(TMP_DIR, 'rand_xkcd.json')


def get_xkcd_info():
    file_path = os.path.join(TMP_DIR, 'info.json')
    download_file('http://xkcd.com/info.0.json', file_path)

    info_dict = load_json_file(file_path)

    return info_dict['num']


def download_random_xkcd(last_num):
    rand_num = random.randint(1, last_num)

    download_file('https://xkcd.com/{}/info.0.json'.format(rand_num), TMP_JSON_PATH)


def get_img_path_and_alt():
    img_dict = load_json_file(TMP_JSON_PATH)

    alt = img_dict['alt']
    img_url = img_dict['img']

    file_name = get_file_name_from_url(img_url)

    tmp_img_path = os.path.join(TMP_DIR, file_name)

    download_file(img_url, tmp_img_path)

    return tmp_img_path, alt


if __name__ == '__main__':
    os.makedirs(TMP_DIR, exist_ok=True)

    last_num = get_xkcd_info()

    download_random_xkcd(last_num)

    tmp_img_path, alt = get_img_path_and_alt()

    ###########################

    access_token = dotenv_values()['access_token']
    group_id = dotenv_values()['group_id']

    is_load = load_photo_to_vc_group_wall(access_token, group_id, tmp_img_path, alt)

    if is_load:
        shutil.rmtree(TMP_DIR)
