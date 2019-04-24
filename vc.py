import requests


def load_photo_to_vc_group_wall(access_token, group_id, image_path, message=''):
    params = {'v': 5.95,
              'access_token': access_token,
              'group_id': group_id
              }

    res_dict = get_wall_upload_server(group_id, params)
    response = res_dict['response']
    upload_url = response['upload_url']

    ###########################################################

    res_dict = upload_photo_to_server(image_path, upload_url)

    params = params.copy()
    params.update(res_dict)

    ###########################################################

    res_dict = save_wall_photo(params)
    response = res_dict['response']

    attachments_list = ['photo{}_{}'.format(photo_dict['owner_id'], photo_dict['id']) for photo_dict in response]
    attachments = ','.join(attachments_list)

    ###########################################################

    params.update({'attachments': attachments,
                   'from_group': 1,
                   'message': message
                   })

    wall_post_to_group(group_id, params)


def wall_post_to_group(group_id, params: dict) -> dict:
    ''' https://vk.com/dev/wall.post '''

    params = params.copy()
    params['owner_id'] = '-{}'.format(group_id)

    res = requests.post('https://api.vk.com/method/wall.post', params=params)
    res.raise_for_status()

    return res.json()


def save_wall_photo(params):
    ''' https://vk.com/dev/photos.saveWallPhoto '''

    res = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=params)
    res.raise_for_status()

    return res.json()


def get_wall_upload_server(group_id, params: dict):
    ''' https://vk.com/dev/photos.getWallUploadServer '''

    params = params.copy()
    params['group_id'] = group_id

    res = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=params)
    res.raise_for_status()

    return res.json()


def upload_photo_to_server(image_path, upload_url) -> dict:
    ''' https://vk.com/dev/upload_files '''

    with open(image_path, 'rb') as image_file_descriptor:
        files = {'photo': image_file_descriptor}

        res = requests.post(upload_url, files=files)
        res.raise_for_status()

    return res.json()
