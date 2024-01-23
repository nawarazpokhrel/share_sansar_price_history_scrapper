from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect

Base = declarative_base()

class ShareSansarData(Base):
    __tablename__ = 'share_history'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    s_no = Column(Integer)
    symbol = Column(String(50))
    confidence = Column(String(50))
    open_price = Column(String(50))
    high_price = Column(String(50))
    low_price = Column(String(50))
    close_price = Column(String(50))
    vwap = Column(String(50))
    volume = Column(String(50))
    prev_close = Column(String(50))
    turnover = Column(String(50))
    transactions = Column(String(50))
    diff = Column(String(50))
    diff_percentage = Column(String(50))
    date = Column(String(50))



def db_connect():
    return create_engine("postgresql://postgres:postgres@localhost:5432/share_sansar_data")

def create_table(engine):
    Base.metadata.create_all(engine)

def table_exists(engine, table_name):
    inspector = inspect(engine)
    return inspector.has_table(table_name)

class ShareSansarDateWiseIndex(Base):
    __tablename__ = 'share_index_history_data'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    index_name = Column(String(50))
    current_value = Column(String(50))
    point_change = Column(String(50))
    percent_change = Column(String(50))
    turnover = Column(String(50))
    date = Column(String(50))


