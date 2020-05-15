import os
import random
import logging
import requests
import service_api_functions
from dotenv import load_dotenv


VERSION_VKONTAKTE = '5.52'
logger = logging.getLogger('posting')


def get_upload_url(params):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    uploading_address = service_api_functions.get_data_from_site(url, params)
    if uploading_address:
        return uploading_address['response']['upload_url']


def get_page_of_comics():
    last_comic = service_api_functions.get_data_from_site('http://xkcd.com/info.0.json')
    if last_comic:
        return random.randint(1, last_comic['num'])


def read_comic(params):
    page_of_comics = get_page_of_comics()
    url = 'http://xkcd.com/{0}/info.0.json'.format(page_of_comics)
    upload_url = get_upload_url(params)
    current_comic = service_api_functions.get_data_from_site(url)
    if current_comic:
        return {
            'filename': service_api_functions.download_image(current_comic),
            'title': current_comic['title'],
            'alt': current_comic['alt'],
            'upload_url': upload_url
        }


def create_attachment(photo_to_post):
    attachment = 'photo{0}_{1}'.format(photo_to_post[0]['owner_id'], photo_to_post[0]['id'])
    return attachment


def save_photo_to_post(upload_parametrs, params):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params['photo'] = upload_parametrs['photo']
    params['server'] = upload_parametrs['server']
    params['hash'] = upload_parametrs['hash']
    photo_to_post = service_api_functions.get_data_from_site(url, params, 'POST')
    if photo_to_post and photo_to_post['response']:
        upload_parametrs['attachment'] = create_attachment(photo_to_post['response'])
    return upload_parametrs


def public_post(published_comic, params):
    url = 'https://api.vk.com/method/wall.post'
    publication_params = {
        'access_token': params['access_token'],
        'v': params['v'],
        'owner_id': '-' + params['group_id'],
        'from_group': 1,
        'attachments': published_comic['attachment'],
        'message': published_comic['title']
    }
    service_api_functions.get_data_from_site(url, publication_params)


def initialize_logger():
    output_dir = os.path.dirname(os.path.realpath(__file__))
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(output_dir, 'log.txt'), "a")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():

    load_dotenv()
    initialize_logger()

    params = {
        'group_id': '195190507',
        'access_token': os.environ.get('VK_ACCESS_TOKEN'),
        'v': VERSION_VKONTAKTE
    }

    try:
        comic = read_comic(params)
        if comic:
            uploading_comic = service_api_functions.upload_image(comic)
            published_comic = save_photo_to_post(uploading_comic, params)
            public_post(published_comic, params)
            os.remove(comic['filename'])
    except requests.exceptions.HTTPError as error:
        logger.error('Ошибка получения или отправки данных на сайт: {0}'.format(error))
    except (KeyError, TypeError) as error:
        logger.error('Ошибка загрузки или публикации поста на сайте vc.com: {0}'.format(error))
    except OSError as error:
        logger.error('Ошибка работы с файлами: {0}'.format(error))
    else:
        logger.info('Публикация поста успешно завершена')


if __name__ == '__main__':
    main()
