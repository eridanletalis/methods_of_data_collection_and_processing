from suppl_functuions import mysql_tunneling
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, select
import pandas as pd


def insert_mysql(frame):
    meta = MetaData()
    vacancy = Table(
        'vacancy', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('where', String),
        Column('who', String),
        Column('link', String),
        Column('compens_min', Integer),
        Column('compens_max', Integer),
        Column('currency', String),
        Column('site', String),
    )

    server = mysql_tunneling()
    server.start()
    engine = create_engine('mysql://user:password@127.0.0.1:3306/test_db?charset=utf8mb4', pool_recycle=3306, echo=True)
    conn = engine.connect()
    vcncy = frame.to_dict('records')
    conn.execute(vacancy.insert(), vcncy)
    server.stop()


def req_gte_compensation_min(compensation_min: int):
    meta = MetaData()
    vacancy = Table(
        'vacancy', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('where', String),
        Column('who', String),
        Column('link', String),
        Column('compens_min', Integer),
        Column('compens_max', Integer),
        Column('currency', String),
        Column('site', String),
    )

    server = mysql_tunneling()
    server.start()
    engine = create_engine('mysql://user:password@127.0.0.1:3306/test_db?charset=utf8mb4', pool_recycle=3306, echo=True)
    conn = engine.connect()
    s = select([vacancy]).where(vacancy.c.compens_min >= compensation_min)
    result = conn.execute(s)
    req_list = []
    for r in result:
        req_list.append(r)
    server.stop()
    return req_list
