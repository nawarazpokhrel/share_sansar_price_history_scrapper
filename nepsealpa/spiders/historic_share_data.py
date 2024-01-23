import csv
from datetime import datetime

import scrapy

from nepsealpa.items import ShareSansarItem


class ShareSansarSpider(scrapy.Spider):
    name = 'sharesansar'
    custom_settings = {

        "LOG_ENABLED": True,  # Enable logging
        "ITEM_PIPELINES": {"nepsealpa.pipelines.NepsealphaPipeline": 301}
    }
    start_urls = ['https://www.sharesansar.com/ajaxtodayshareprice']

    def start_requests(self):
        # Your cookies and headers from the original request
        with open('nepse_calender.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                date_str = row[1]
                # Convert date string to a format expected by the website
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

                # Your cookies and headers from the original request
                cookies = {
                    'XSRF-TOKEN': 'eyJpdiI6Ijd3Q2E5cUVhUVBhbXUrT3pDUHhSWUE9PSIsInZhbHVlIjoiN2tyb1E0ei9LdnpOYVFZcjRxNjFNeG1CMWlhTmZoaU03SzVBdGYreTNReUJWRUhFN1BubThoRGRpc1BRaGVWQXE3RkVoZGk0b0tHdmtHY0ZGOFNZMTQ4SklzeHlSZGxPNmRyaHJkeEFPenJ2dFV5anBQVGxGdFRuNU85bmUyNTciLCJtYWMiOiIyMDBlYzlkODhlMGFmNzY4Y2E3N2Q5M2M2Njg5Nzc4NzkzOWVjNTE2NjQ3NGE3MzZhNjYxNjVmMjY2NzQ0NGI5In0%3D',
                    'sharesansar_session': 'eyJpdiI6ImVUMGNsblZNQlMzR0E2K2pYN2MrVkE9PSIsInZhbHVlIjoibXlnOURlK05xdW9SRU5MSVFaN0EwVjhNOUxSNnlpQ1Q2WVhCUlFJbmF5RFBacTdwdEJWejgvYlVSTGpDU0Q3RW5aLzZpMmVQZWw0TWtld2JGTUFJRy93UWt4VTIzRGRLWThFN3lVdEp6UytlamM4cTUxZVUxMWtId3h3YU1na3EiLCJtYWMiOiIwZjNjOTYzYjY0OTkyMTk3NWU0NDEzMDk0MmRkNDZjOTNhMmJlODNhY2I1ZDM1ZjVjMGE2OWRhMDQ0OWU0MzhiIn0%3D',
                }

                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://www.sharesansar.com',
                    'Referer': 'https://www.sharesansar.com/today-share-price',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                }

                data = {
                    '_token': 'DJPFerCH2twF1aJrIRRIBgrrlVeE8hxpdtDJ7Wdg',
                    'sector': 'all_sec',
                    'date': date_obj.strftime('%Y-%m-%d'),
                }

                # Make a POST request with the provided data, cookies, and headers
                yield scrapy.FormRequest(
                    url=self.start_urls[0],
                    formdata=data,
                    cookies=cookies,
                    headers=headers,
                    callback=self.parse,
                    cb_kwargs={'date': date_obj}  # Pass date as a keyword argument to parse method
                )

    def parse(self, response,date):
        # Extract data from the table
        rows = response.css('table#headFixed tbody tr')
        for row in rows:
            item = ShareSansarItem()

            # Iterate over each column and extract data based on the column index
            for index, column in enumerate(row.css('td')):
                # Extract data based on the index
                if index == 0:
                    item['s_no'] = column.css('::text').get()
                elif index == 1:
                    item['symbol'] = column.css('a::text').get()
                elif index == 2:
                    item['confidence'] = column.css('::text').get()
                elif index == 3:
                    item['open_price'] = column.css('::text').get()
                elif index == 4:
                    item['high_price'] = str(column.css('::text').get())
                elif index == 5:
                    item['low_price'] = str(column.css('::text').get())
                elif index == 6:
                    item['close_price'] = str(column.css('::text').get())
                elif index == 7:
                    item['vwap'] = str(column.css('::text').get())
                elif index == 8:
                    item['volume'] = str(column.css('::text').get())
                elif index == 9:
                    item['prev_close'] = str(column.css('::text').get())
                elif index == 10:
                    item['turnover'] = str(column.css('::text').get())
                elif index == 11:
                    item['transactions'] = str(column.css('::text').get())
                elif index == 12:
                    item['diff'] = str(column.css('::text').get())
                elif index == 14:
                    item['diff_percentage'] = str(column.css('::text').get())

                item['date'] = date.strftime('%Y-%m-%d')


            yield item