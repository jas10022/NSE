import pandas as pd
from time import time
from sqlalchemy import Column, Integer, Float, Date, String, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
from sqlalchemy.ext.automap import automap_base

t = time()

#Create the database
engine = create_engine('sqlite:///nse.db')

#Create the session
session = sessionmaker()
session.configure(bind=engine)
s = session()

def create_db():
    Base = declarative_base()
    metadata = Base.metadata
    my_table = Table('NSE', metadata,
        Column('id',Integer, primary_key=True, nullable=False),
        Column('symbol',String(45), nullable=False),
        Column('series',String(45)),
        Column('date',String(45), nullable=False),
        Column('prev_close',String(45)),
        Column('open_price',String(45)),
        Column('high_price',String(45)),
        Column('low_price',String(45)),
        Column('last_price',String(45)),
        Column('close_price',String(45)),
        Column('avg_price',String(45)),
        Column('ttl_trd_qt',String(45)),
        Column('turnover_lakhs',String(45)),
        Column('no_of_trades',String(45)),
        Column('deliv_qty',String(45)),
        Column('deliv_per',String(45)),
        UniqueConstraint('symbol','date')
    )
    insert_query = my_table.insert()
    Base.metadata.create_all(engine)
    return insert_query
    

def load_db():
    Base = automap_base()
    metadata = Base.metadata
    my_table = Table('NSE', metadata,
        Column('id',Integer, primary_key=True, nullable=False),
        Column('symbol',String(45), nullable=False),
        Column('series',String(45)),
        Column('date',String(45), nullable=False),
        Column('prev_close',String(45)),
        Column('open_price',String(45)),
        Column('high_price',String(45)),
        Column('low_price',String(45)),
        Column('last_price',String(45)),
        Column('close_price',String(45)),
        Column('avg_price',String(45)),
        Column('ttl_trd_qt',String(45)),
        Column('turnover_lakhs',String(45)),
        Column('no_of_trades',String(45)),
        Column('deliv_qty',String(45)),
        Column('deliv_per',String(45)),
        UniqueConstraint('symbol','date')
    )
    insert_query = my_table.insert()
    Base.prepare(engine, reflect=True)
    return insert_query


def update_data(insert_query):
    t = f'https://archives.nseindia.com/products/content/sec_bhavdata_full_23052022.csv'

    pd.read_csv(t).to_csv('sec_bhavdata_full_23052022.csv')
    data = pd.read_csv('sec_bhavdata_full_23052022.csv')
    try:
        temp = []
        for index,i in data.iterrows():
            temp.append((
                    i['SYMBOL'],
                    i[' SERIES'],
                    i[' DATE1'].strip(),
                    i[' PREV_CLOSE'],
                    i[' OPEN_PRICE'],
                    i[' HIGH_PRICE'],
                    i[' LOW_PRICE'],
                    i[' LAST_PRICE'],
                    i[' CLOSE_PRICE'],
                    i[' AVG_PRICE'],
                    i[' TTL_TRD_QNTY'],
                    i[' TURNOVER_LACS'],
                    i[' NO_OF_TRADES'],
                    i[' DELIV_QTY'],
                    i[' DELIV_PER'],
                ))
        print(temp)
        ins = """INSERT OR REPLACE INTO "NSE" (symbol, series, date, prev_close, open_price, high_price, low_price, last_price, close_price, avg_price, ttl_trd_qt, turnover_lakhs, no_of_trades, deliv_qty, deliv_per) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        engine.execute(ins,temp)
        s.commit() #Attempt to commit all the records
    except Exception as e:
        print('exception', e)
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connections

if (__name__ == "__main__"):
    insert_query = None
    try:
        insert_query = create_db()
        #insert_query = load_db()
    except:
        insert_query = create_db()
    update_data(insert_query)