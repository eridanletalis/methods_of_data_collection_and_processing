import requests
import json
from time import sleep


def savefile(name, data):
    with open(name + ".json", 'w') as json_file:
        json.dump(data, json_file)


token = input("Введите ваш токен для VK: ")

request = "https://api.vk.com/method/friends.get?v=5.52&access_token=" + token
request2_1 = "https://api.vk.com/method/users.get?user_ids="
request2_2 = "&fields=bdate&v=5.103&access_token="
response = requests.get(request)
data = json.loads(response.text)
data = data["response"]

savefile("friends_response", data)
friends = []
for friend in data["items"]:
    resp2 = requests.get(request2_1 + str(friend) + request2_2 + token)
    data2 = json.loads(resp2.text)
    data2 = data2["response"]
    sleep(0.2)  # сделано для того, чтобы не было ошибки из-за частых запросов.
    friends.append(data2[0])
    print("Друг {} {} ID: {}".format(data2[0]["first_name"], data2[0]["last_name"], data2[0]["id"]))

savefile("friends_2", friends)
