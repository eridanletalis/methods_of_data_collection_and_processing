from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from time import time

def hh_compensation_pareser(compensation):
    min = max = currency = "NA"
    currency1 = compensation.find("руб")
    currency2 = compensation.find("РУБ")
    if currency1 < currency2:
        currency1 = currency2
    if currency1 >  -1:
        compensation = compensation[:currency1]
        currency = "РУБ"
    currency1 = compensation.find("USD")
    currency2 = compensation.find("usd")
    if currency1 < currency2:
        currency1 = currency2
    if currency1 >  -1:
        compensation = compensation[:currency1]
        currency = "USD"
    compensation = compensation.replace(" ", "")

    delim = compensation.find('-')
    if delim > -1:
        min = compensation[:delim]
        max = compensation[delim+1:]
        min = min.replace('\xa0', "")
        max = max.replace('\xa0', "")
        return min, max, currency
    from_ = compensation.find("от")
    before_ = compensation.find("до")
    if from_ > -1:
        min = compensation[2:]
    if before_ > -1:
        max = compensation[2:]
    min = min.replace('\xa0', "")
    max = max.replace('\xa0', "")
    return min, max, currency



main_link = 'https://spb.hh.ru'
headers = {'user-agent': 'PostmanRuntime/7.22.0'}
data = input("Введите поисковый запрос: ")
pages_hh = pages_job = int(input("Введите количество страниц: "))
# pages_hh =pages_job =  10
# data = "Data Science"

data = data.replace(" ", "+")
response = requests.get(main_link +"/search/vacancy?area=2&st=searchVacancy&text=" + data, headers=headers).text
vacancy = []
next_page = True

while next_page:
    html = bs(response,'lxml')

    # HH

    vacancy_block = html.findAll('div', {'class': "vacancy-serp-item"})

    for block in vacancy_block:
        name = block.find('a', {'data-qa':"vacancy-serp__vacancy-title"})
        link = name.attrs['href']
        name = name.text
        who = block.find('a', {'data-qa':"vacancy-serp__vacancy-employer"}).text
        try:
            where = block.find('span', {'data-qa': "vacancy-serp__vacancy-address"}).text
        except:
            where = "NA"
        try:
            compens_min, compens_max, currency = hh_compensation_pareser(
                block.find('div', {'data-qa': "vacancy-serp__vacancy-compensation"}).text
            )
        except:
            currency = compens_max = compens_min = "NA"

        src = main_link

        vacancy.append([name, link, who, where, compens_min, compens_max, currency, src])

    pages_hh -= 1
    next = html.find('a', {"data-qa":"pager-next"})
    if next is not None and pages_hh > 0:
        next_link = next.attrs['href']
        response = requests.get(main_link + next_link, headers=headers).text
    else:
        next_page = False

if pages_hh > 0:
    print("По вашему запросу существует меньше страниц на HH, чем было запрошено")
labels = ["name", "link", "who", "where", "compens_min", "compens_max", "currency", "src"]
df = pd.DataFrame(vacancy, columns=labels)
df.to_csv("jobs" + str(time()) + ".csv", sep=';', index=False, encoding = 'utf-16')
print(df)
