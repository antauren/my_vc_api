import os
import requests
import json
from urllib import parse


def download_file(url, path):
    response = requests.get(url)
    response.raise_for_status()

    with open(path, 'wb') as file_:
        file_.write(response.content)

    return True


def load_json_file(path):
    with open(path) as f:
        return json.loads(f.read())


def get_file_name_from_url(url):
    parsed_url = parse.urlparse(url)

    return os.path.split(parsed_url.path)[-1]


if __name__ == '__main__':
    pass
