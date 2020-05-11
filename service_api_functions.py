import requests


def get_filename(url_pict):
    List = url_pict.split('/')
    if len(List) > 1:
        return List[len(List) - 1]


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


def query_to_site(url, params=None, method='GET'):
    if method == 'GET':
        response = requests.get(url, params=params)
    else:
        response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def get_file(url, filename):
    responce = requests.get(url, verify=False, timeout=10)
    responce.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(responce.content)


def upload_file(url, filename):
    if url:
        with open(filename, 'rb') as f:
            files = {
                'photo': f,
            }
            response = requests.post(url, files=files)
            response.raise_for_status()
            return response.json()
