from sqlalchemy import create_engine, Column, Integer, Float, Date, String, Table
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///nse.db', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)


from sqlalchemy.orm import relationship, backref

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


if __name__ == '__main__':
    from sqlalchemy.orm import scoped_session, sessionmaker, Query
    db_session = scoped_session(sessionmaker(bind=engine))
    for item in db_session.query(NSE_Node):
        print (item.id)
    print(db_session.query(NSE_Node))