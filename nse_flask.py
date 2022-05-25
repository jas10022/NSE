from flask import Flask, render_template, request, jsonify
import pandas as pd 
import csv
import json
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from time import time
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, Date, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy.ext.automap import automap_base
from flask_cors import CORS

engine = create_engine('sqlite:///nse.db', convert_unicode=True, echo=False)
Base = automap_base()
#Base.metadata.reflect(engine)
Base.prepare(engine, reflect=True)


class NSE_Node(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'NSE'
    __table_args__ = {'sqlite_autoincrement': True, 'extend_existing': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True, nullable=False) 
    symbol = Column(String(45), nullable=False)
    series = Column(String(45))
    date = Column(String(45), nullable=False)
    prev_close = Column(Float)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    last_price = Column(Float)
    close_price = Column(Float)
    avg_price = Column(Float)
    ttl_trd_qt = Column(Float)
    turnover_lakhs = Column(Float)
    no_of_trades = Column(Float)
    deliv_qty = Column(Float)
    deliv_per = Column(Float)


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_symbol', methods= ["GET"])
def get_symbol():
    db_session = scoped_session(sessionmaker(bind=engine))
    args = request.args
    symbol = args.get("symbol")
    q = db_session.query(NSE_Node.id, NSE_Node.symbol,NSE_Node.series,NSE_Node.date,NSE_Node.prev_close,NSE_Node.open_price,NSE_Node.high_price,NSE_Node.low_price,NSE_Node.last_price, NSE_Node.close_price, NSE_Node.avg_price, NSE_Node.ttl_trd_qt, NSE_Node.turnover_lakhs, NSE_Node.no_of_trades, NSE_Node.deliv_qty, NSE_Node.deliv_per)
    t = []
    for i in q.filter(NSE_Node.symbol == symbol):
        t.append({'id':i.id, 'symbol':i.symbol, 'series': i.series, 'date': i.date, 'prev_close': i.prev_close, 'open_price':i.open_price,'high_price':i.high_price,'low_price':i.low_price,'last_price':i.last_price,'close_price':i.close_price,'avg_price':i.avg_price, 'ttl_trd_qt':i.ttl_trd_qt,'turnover_lakhs':i.turnover_lakhs, 'no_of_trades': i.no_of_trades, 'deliv_qty':i.deliv_qty, 'deliv_per':i.deliv_per})

    return jsonify({'status': 200, 'value': t})

@app.route('/live', methods= ["GET"])
def live():
    db_session = scoped_session(sessionmaker(bind=engine))
    q = db_session.query(NSE_Node.id, NSE_Node.symbol,NSE_Node.series,NSE_Node.date,NSE_Node.prev_close,NSE_Node.open_price,NSE_Node.high_price,NSE_Node.low_price,NSE_Node.last_price, NSE_Node.close_price, NSE_Node.avg_price, NSE_Node.ttl_trd_qt, NSE_Node.turnover_lakhs, NSE_Node.no_of_trades, NSE_Node.deliv_qty, NSE_Node.deliv_per)
    t = []
    for i in q:
        t.append({'id':i.id, 'symbol':i.symbol, 'series': i.series, 'date': i.date, 'prev_close': i.prev_close, 'open_price':i.open_price,'high_price':i.high_price,'low_price':i.low_price,'last_price':i.last_price,'close_price':i.close_price,'avg_price':i.avg_price, 'ttl_trd_qt':i.ttl_trd_qt,'turnover_lakhs':i.turnover_lakhs, 'no_of_trades': i.no_of_trades, 'deliv_qty':i.deliv_qty, 'deliv_per':i.deliv_per})
    return jsonify({'status': 200, 'value': t})

if (__name__ == "__main__"):
    app.run(host='0.0.0.0',port = 80)

