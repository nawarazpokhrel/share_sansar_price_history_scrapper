import csv
from datetime import datetime

import scrapy

from nepsealpa.items import ShareSansarIndexItem


class SharesansarSpider(scrapy.Spider):
    name = 'dateindex'
    allowed_domains = ['sharesansar.com']
    custom_settings = {

        "LOG_ENABLED": True,  # Enable logging
        "ITEM_PIPELINES": {"nepsealpa.pipelines.DateWiseIndexPipeline": 302}
    }

    cookies = {
        'XSRF-TOKEN': 'eyJpdiI6Ik9mcU01OGhKZFBzOXY5eTJuazB3ckE9PSIsInZhbHVlIjoieVRnNjdSa2c0NXEzTC84VnprVXh1WUxueEFkTUhRanVibmJ6aG0rUmtsaHJQOCsxeHJJbm9ER2xFRWlEU3hyV0lZWE5URE0xbmY3VnRrMDg3amdSWlRDSE1rRVhpaS9MdTIramlsdmVyRkJuZkYwbktxTmt4elJ3bkh3SWRtdXUiLCJtYWMiOiI2ZmVhNDJkYzA0MzA2MTUyNzIyMjI1NzUyMWI1NDBiYjAyMjBiZjZiYTFiOWI4MjdiMzk4MWU5M2YzM2Y2ZDY0In0%3D',
        'sharesansar_session': 'eyJpdiI6Iml2c3g1U1dJZmJzdCtCeXZyQzFaUWc9PSIsInZhbHVlIjoiN1NnVG5qZ0RUYmF5M0FmTG5Pd3F4ZW9NcjZmdk5LZjZRaWJ6Y2JEZVFQRVBjdC81VlRoVnpOb3dxY2kwZytscitWUmtDSDlBNGR5bUtaQlNHRnc5TFc4STJ6aUxxcDRoaXZlbGI0SEdRZmMxd2U3bGIvNW1ucUkwK1ByaExNOFEiLCJtYWMiOiI1ODJjNTc4OGRlOTBhZTRiZGI0NDNmMWQ5ZjE5Mzc4YTYyNzE3ZjA1ZmMwNTljNzk2YjgxZTVlMWU3OGJiZGU1In0%3D',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.sharesansar.com/datewise-indices',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    def start_requests(self):
        base_url = 'https://www.sharesansar.com/datewise-indices'
        with open('nepse_calender.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                date_obj = datetime.strptime(row[1], '%Y-%m-%d').date()
                params = {'date': date_obj}
                url_with_params = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
                yield scrapy.Request(
                    url=url_with_params,
                    callback=self.parse,
                    cookies=self.cookies,
                    headers=self.headers,
                    cb_kwargs={'date': date_obj}
                )

    def parse(self, response,date):
        # print(response.text,"hi"*100)
        # Save the formatted HTML to a file
        rows = response.xpath('//table[@class="table table-bordered table-striped table-hover"]/tbody/tr')

        for row in rows:
            item = ShareSansarIndexItem()

            item['index_name'] = str(row.xpath('td[1]/text()').get())
            item['current_value'] = str(row.xpath('td[2]/text()').get())
            item['point_change'] = str(row.xpath('td[3]/text()').get())
            item['percent_change'] = str(row.xpath('td[4]/text()').get())
            item['turnover'] = str(row.xpath('td[5]/text()').get())
            item['date'] = date.strftime('%Y-%m-%d')

            # Now you can do something with the extracted data, such as storing it or printing it
            yield item
