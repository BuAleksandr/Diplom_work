import requests
from pprint import pprint

user_id = input('Введите свой ID в VK: ')
user_token_ya_disk = input('Введите свой токен для Яндекс.Диска: ')
user_token_VK = input('Введите свой токен для ВК: ')


class VK_User:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def search_photo(self, owner_id, sorting=0):
        photos_search_url = self.url + 'photos.get'
        photos_search_params = {
            'count': 50,
            'owner_id': owner_id,
            'extended': 1,
            'album_id': 'profile'
        }
        req = requests.get(photos_search_url, params={**self.params, **photos_search_params}).json()
        return req['response']['items']


vk_client = VK_User(user_token_VK, '5.131')
i = 0
photos_json = vk_client.search_photo(user_id)
photos_count = len(photos_json)
new_json = []

while i < photos_count:
    photos_dict = {}
    likes = photos_json[i]['likes']['count']
    size_len = len(photos_json[i]['sizes']) - 1
    size = photos_json[i]['sizes'][size_len]
    photos_dict['file name'] = likes
    photos_dict['size'] = size
    new_json.append(photos_dict)
    i += 1

pprint(new_json)


class YaUploader:
    API_BASE_URL = "https://cloud-api.yandex.net:443"

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Authorization': self.token
        }

    def new_folder(self, name_folder):
        req = requests.put(self.API_BASE_URL + '/v1/disk/resources?path=' + name_folder, headers=self.headers)
        req_url = req.json()["href"]
        return req_url

    def upload(self, yandex_folder_name, file_name, path_file: str):
        name_folder_file = f'{yandex_folder_name}/{file_name}.jpeg'
        params = {
            'path': name_folder_file,
            'url': path_file
        }
        requests.post(self.API_BASE_URL + '/v1/disk/resources/upload', params=params, headers=self.headers)


uploader = YaUploader(user_token_ya_disk)
name_yandex_folder = input(f'Как назвать папку? ')
url_folder = uploader.new_folder(name_yandex_folder)
x = 0

while x < photos_count:
    name_file = new_json[x]['file name']
    path_to_file = new_json[x]['size']['url']
    uploader.upload(name_yandex_folder, name_file, path_to_file)
    x += 1
    print(f'Файл {name_file} загружен')
print('Работа выполнена')
