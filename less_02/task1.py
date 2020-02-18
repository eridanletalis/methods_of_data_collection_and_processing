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

def job_compensation_pareser(compensation):
    if compensation == "По договорённости":
        return "NA", "NA", "NA"
    min = max = currency = "NA"
    currency = "РУБ"
    compensation = compensation[:-2]
    compensation = compensation.replace(" ", "")

    delim = compensation.find('—')
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

main_link = 'https://www.hh.ru'
headers = {'user-agent': 'PostmanRuntime/7.22.0'}
data = input("Введите поисковый запрос: ")
pages_hh = pages_job = int(input("Введите количество страниц в каждом агрегаторе: "))
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
        try:
            who = block.find('a', {'data-qa':"vacancy-serp__vacancy-employer"}).text
        except:
            who = "NA"
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

        main_link

        vacancy.append([name, link, who, where, compens_min, compens_max, currency, main_link])

    pages_hh -= 1
    next = html.find('a', {"data-qa":"pager-next"})
    if next is not None and pages_hh > 0:
        next_link = next.attrs['href']
        response = requests.get(main_link + next_link, headers=headers).text
    else:
        next_page = False

if pages_hh > 0:
    print("По вашему запросу существует меньше страниц на HH, чем было запрошено")


main_link = "https://russia.superjob.ru"
response = requests.get(main_link + "/vacancy/search/?keywords=" + data, headers=headers).text


next_page = True
while next_page:

    # Superjob

    html = bs(response, 'lxml')
    block = html.findAll('div', {"class": "_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr"})
    for item in block:
        name = item.find('div', {"class": "_3mfro CuJz5 PlM3e _2JVkc _3LJqf"}).text  # Название вакансии
        try:
            who = item.find(
                'span',
                {"class": "_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI"}).text
        except:
            who = "NA"

        compensation = item.find('span',
                                 {"class": "_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz"}).text

        try:
            compens_min, compens_max, currency = job_compensation_pareser(compensation)
        except:
            currency = compens_max = compens_min = "NA"

        link = item.find('div', {"class": "_3syPg _3P0J7 _9_FPy"}).contents[0].find('a').attrs['href']
        link = main_link + link

        try:
            where = item.find(
                "span", {"class": "_3mfro f-test-text-company-item-location _9fXTd _2JVkc _2VHxz"}).contents[2].text
        except:
            where = "NA"

        vacancy.append([name, link, who, where, compens_min, compens_max, currency, main_link])

    pages_job -= 1
    next = html.find("a", {"class": "icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe"})

    if next is not None and pages_job > 0:
        next_link = next['href']
        response = requests.get(main_link + next_link, headers=headers).text
    else:
        next_page = False


if pages_job > 0:
    print("По вашему запросу существует меньше страниц на SuperJib, чем было запрошено")

labels = ["name", "link", "who", "where", "compens_min", "compens_max", "currency", "src"]
df = pd.DataFrame(vacancy, columns=labels)
df.to_csv("jobs" + str(time()) + ".csv", sep=';', index=False, encoding = 'utf-16')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
print(df)
