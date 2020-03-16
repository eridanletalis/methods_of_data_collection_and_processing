from sshtunnel import SSHTunnelForwarder

MONGO_HOST = "192.168.1.72"
MONGO_USER = "ubuntu"
MONGO_PASS = ""


def mongo_tunneling():
    return SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USER,
        ssh_password=MONGO_PASS,
        remote_bind_address=('127.0.0.1', 27017)
    )


def mysql_tunneling():
    return SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USER,
        ssh_password=MONGO_PASS,
        remote_bind_address=('127.0.0.1', 3306)
    )


def hh_compensation_pareser(compensation):
    min = max = currency = 0
    currency1 = compensation.find("руб")
    currency2 = compensation.find("РУБ")
    if currency1 < currency2:
        currency1 = currency2
    if currency1 > -1:
        compensation = compensation[:currency1]
        currency = "РУБ"
    currency1 = compensation.find("USD")
    currency2 = compensation.find("usd")
    if currency1 < currency2:
        currency1 = currency2
    if currency1 > -1:
        compensation = compensation[:currency1]
        currency = "USD"
    compensation = compensation.replace(" ", "")

    delim = compensation.find('-')
    if delim > -1:
        min = compensation[:delim]
        max = compensation[delim + 1:]
        min = min.replace('\xa0', "")
        max = max.replace('\xa0', "")
        return min, max, currency
    from_ = compensation.find("от")
    before_ = compensation.find("до")
    if from_ > -1:
        min = compensation[2:]
    if before_ > -1:
        max = compensation[2:]
    try:
        min = min.replace('\xa0', "")
    except:
        pass
    try:
        max = max.replace('\xa0', "")
    except:
        pass
    try:
        min = int(min)
        max = int(max)
    except:
        pass
    return min, max, currency


def job_compensation_pareser(compensation):
    if compensation == "По договорённости":
        return 0, 0, 0
    min = max = currency = 0
    currency = "РУБ"
    compensation = compensation[:-2]
    compensation = compensation.replace(" ", "")

    delim = compensation.find('—')
    if delim > -1:
        min = compensation[:delim]
        max = compensation[delim + 1:]
        min = min.replace('\xa0', "")
        max = max.replace('\xa0', "")
        return min, max, currency

    from_ = compensation.find("от")
    before_ = compensation.find("до")
    if from_ > -1:
        min = compensation[2:]
    if before_ > -1:
        max = compensation[2:]
    try:
        min = min.replace('\xa0', "")
    except:
        pass
    try:
        max = max.replace('\xa0', "")
    except:
        pass

    try:
        min = int(min)
    except:
        pass
    try:
        max = int(max)
    except:
        pass

    return min, max, currency
