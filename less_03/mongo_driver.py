import pymongo
import json
import pandas as pd
import suppl_functuions as supp

MONGO_DB = "test_data"


def insert_mongo(frame):
    # Использовать при необходимости сделать туннель.

    server = supp.mongo_tunneling()
    server.start()
    client = pymongo.MongoClient('127.0.0.1', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[MONGO_DB]
    records = json.loads(frame.T.to_json()).values()
    db.users.insert_many(records)

    client.close()
    server.stop()


def req_gte_compensation_min(compensation_min: int):
    server = supp.mongo_tunneling()

    server.start()
    client = pymongo.MongoClient('127.0.0.1', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[MONGO_DB]

    results = db.users.find({"compens_min": {"$gte": compensation_min}})
    req_list = []
    for r in results:
        req_list.append(r)

    client.close()
    server.stop()
    return req_list


def update_mongo(frame):
    return None
