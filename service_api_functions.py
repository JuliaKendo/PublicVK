import requests


def get_filename(url):
    fragments_url = url.split('/')
    if len(fragments_url) > 1:
        return fragments_url[-1]


def download_image(current_comic):
    url_image = current_comic['img']
    filename = get_filename(url_image)
    if filename:
        get_file(url_image, filename)
    return filename


def upload_image(current_comic):
    upload_parametrs = upload_file(current_comic['upload_url'], current_comic['filename'])
    if upload_parametrs:
        current_comic['photo'] = upload_parametrs['photo']
        current_comic['server'] = upload_parametrs['server']
        current_comic['hash'] = upload_parametrs['hash']

    return current_comic


def get_data_from_site(url, params=None, method='GET'):
    if method == 'GET':
        response = requests.get(url, params=params)
    else:
        response = requests.post(url, data=params)
    response.raise_for_status()
    json_data = response.json()
    if 'error' in json_data:
        raise requests.exceptions.HTTPError(json_data['error']['error_msg'])
    return json_data


def get_file(url, filename):
    response = requests.get(url, verify=False, timeout=10)
    response.raise_for_status()

    with open(filename, 'wb') as file_handler:
        file_handler.write(response.content)


def upload_file(url, filename):
    if url:
        with open(filename, 'rb') as file_handler:
            files = {
                'photo': file_handler,
            }
            response = requests.post(url, files=files)
            response.raise_for_status()
            json_data = response.json()
            if 'error' in json_data:
                raise requests.exceptions.HTTPError(json_data['error']['error_msg'])

            return json_data
