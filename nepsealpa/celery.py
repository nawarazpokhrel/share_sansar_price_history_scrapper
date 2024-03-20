from celery import Celery
from celery.schedules import crontab
from nepsealpa.spiders import historic_share_data, historic_date_wise
from celery import shared_task
from scrapy.crawler import CrawlerProcess

app = Celery('nepsealpa')
app.conf.broker_url = 'redis://redis-prod:6379/0'
app.conf.result_backend = 'redis://redis-prod:6379/0'
app.conf.enable_utc=False
app.conf.timezone = 'Asia/Kathmandu'
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'run-historic-share-data-at-3pm': {
        'task': 'nepsealpa.celery.run_historic_share_data_spider',
        'schedule': crontab(minute=0, hour=15),  # Run at 3 PM Nepal time
    },
    'run-historic-date-wise-at-3pm': {
        'task': 'nepsealpa.celery.run_historic_date_wise_spider',
        'schedule': crontab(minute=0, hour=15),  # Run at 3 PM Nepal time
    },
}

@shared_task
def run_historic_share_data_spider():
    process = CrawlerProcess()
    process.crawl(historic_share_data)
    process.start(stop_after_crawl=False)

@shared_task
def run_historic_date_wise_spider():
    process = CrawlerProcess()
    process.crawl(historic_date_wise)
    process.start(stop_after_crawl=False)