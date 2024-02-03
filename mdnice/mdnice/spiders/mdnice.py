import scrapy
import json
from datetime import datetime, timedelta, timezone

class MdniceSpider(scrapy.Spider):
    name = 'mdnice'
    start_urls = ['https://www.mdnice.com/']

    def parse(self, response):
        json_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        data = json.loads(json_data)

        articles = data['props']['pageProps']['list']
        for article in articles:
            out_id = article['outId']
            title = article['title']
            url = f"https://www.mdnice.com/writing/{out_id}"
            create_time_str = article['createTime']

            # 解析ISO 8601格式时间字符串，包括时区信息
            create_time = datetime.strptime(create_time_str, "%Y-%m-%dT%H:%M:%S.%f%z")

            # 获取当前时间（考虑到时区）
            current_time = datetime.now(timezone.utc)

            # 计算时间差
            time_difference = current_time - create_time

            # 判断文章是否在过去2小时内创建
            if time_difference <= timedelta(hours=4):
                # 使用meta传递额外数据
                yield scrapy.Request(url, callback=self.parse_article, meta={'title': title, 'create_time': create_time_str})

    def parse_article(self, response):
        # 从meta中提取传递的数据
        title = response.meta['title']
        create_time = response.meta['create_time']

        # 提取阅读次数
        script = response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
        # 解析 JSON 数据
        data = json.loads(script)
        # 提取 readingNum 字段
        reading_num = data["props"]["pageProps"]["writingDetail"]["readingNum"]
        
        yield {
            'title': title,
            'create_time': create_time,
            'url': response.url,
            'read_count': reading_num
        }