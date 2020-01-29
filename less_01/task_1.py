from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth
import json
import stdiomask # Для маскирование ввода пароля пользователем

def savefile(name, data):
    with open(name + ".json", 'w') as json_file:
        json.dump(data, json_file)

link = r'https://api.github.com/user/repos'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 /'
                       '(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


login = input("Введите логин пользователя GitHub: ")
# password = input("Введите пароль пользователя GitHub: ")
password = stdiomask.getpass(prompt="Введите пароль пользователя GitHub: ", mask='*') # маскирует только в терминале,
                                                                                # в PyCharm показывает в открытом виде


response = requests.get(link, auth=HTTPBasicAuth(login, password))
data = json.loads(response.text)
for repo in data:
    try:
        print("Название репозитория: "+ repo["name"])
        print("Язык программирования: " + str(repo["language"]))
        print("Описание репозитория: " + str(repo["description"]))
        print("Лицензия репозитория: " + str(repo["license"]["name"]))
    except:
        pass
    finally:
        print("URL репозитория:" + repo["url"])
        print('\n')

savefile(login, data)
# pprint(data)
