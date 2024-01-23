# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from sqlalchemy import inspect
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from nepsealpa.models import ShareSansarData, db_connect, ShareSansarDateWiseIndex

Base = declarative_base()
def table_exists(engine, table_name):
    inspector = inspect(engine)
    return inspector.has_table(table_name)

class NepsealphaPipeline:
    def __init__(self):
        engine = db_connect()
        if not table_exists(engine, ShareSansarData.__tablename__):
            try:
                Base.metadata.create_all(engine, tables=[ShareSansarData.__table__])
            except Exception as e:
                print(f"Error creating table: {e}")
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        session = self.Session()
        share_data = ShareSansarData(
            s_no=item['s_no'],
            symbol=item['symbol'],
            confidence=item['confidence'],
            open_price=item['open_price'],
            high_price=item['high_price'],
            low_price=item['low_price'],
            close_price=item['close_price'],
            vwap=item['vwap'],
            volume=item['volume'],
            prev_close=item['prev_close'],
            turnover=item['turnover'],
            transactions=item['transactions'],
            diff=item['diff'],
            diff_percentage=item['diff_percentage'],
            date=item['date'],
        )

        try:
            session.add(share_data)
            session.commit()
        except Exception as e:
            session.rollback()
            spider.log(f"Error processing item: {e}")
        finally:
            session.close()

        return item



class DateWiseIndexPipeline:
    def __init__(self):
        engine = db_connect()
        if not table_exists(engine, ShareSansarDateWiseIndex.__tablename__):
            try:
                Base.metadata.create_all(engine, tables=[ShareSansarDateWiseIndex.__table__])
            except Exception as e:
                print(f"Error creating table: {e}")
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        session = self.Session()
        share_data = ShareSansarDateWiseIndex(
            index_name=item['index_name'],
            current_value=item['current_value'],
            point_change=item['point_change'],
            percent_change=item['percent_change'],
            turnover=item['turnover'],
            date=item['date'],

        )

        try:
            session.add(share_data)
            session.commit()
        except Exception as e:
            session.rollback()
            spider.log(f"Error processing item: {e}")
        finally:
            session.close()

        return item