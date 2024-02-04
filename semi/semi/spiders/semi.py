import json
import os
import scrapy
from datetime import datetime, timedelta

class MySpider(scrapy.Spider):
    name = 'semi'
    start_urls = ['https://semi.cas.cn/xwdt/zhxw/']

    def parse(self, response):
        # 确定过去30天的日期范围
        date_limit = datetime.now() - timedelta(days=30)

        # 遍历每个条目
        for item in response.xpath('//td[@class="fw_t"]/..'):
            # 提取并处理时间信息
            date_str = item.xpath('./td[@class="fw_s"]/text()').extract_first().strip()
            # 将字符串日期转换为datetime对象
            article_date = datetime.strptime('20' + date_str, '%Y-%m-%d')

            # 如果文章日期在过去30天内
            if article_date >= date_limit:
                # 提取相对路径并转换为完整URL
                relative_url = item.xpath('./td[@class="fw_t"]/a/@href').extract_first().strip()
                full_url = response.urljoin(relative_url)
                
                # 对每个文章URL发起请求，并将响应传递给parse_article方法处理
                request = scrapy.Request(full_url, callback=self.parse_article)
                request.meta['date'] = article_date.strftime('%Y-%m-%d')  # 传递文章日期
                request.meta['url'] = full_url  # 传递文章URL
                
                yield request

    def parse_article(self, response):
        article_date = response.meta['date']
        article_url = response.meta['url']
        
        article_content = " ".join(response.xpath('//div[contains(@class,"trs_editor_view")]//text()').extract()).strip()
        article_title = response.xpath('//div[@class="title"]/h3/text()').extract_first().strip()

        # 定义文件名，这里使用文章标题作为文件名，确保文件名对于文件系统是安全的
        # 可能需要对article_title进行一些处理，以确保它是有效的文件名
        filename = f"{article_title}.json".replace('/', '_')  # 替换不合法字符

        # 构造要保存的数据
        data = {
            "page_content": article_content,
            "metadata": {
                "source": article_url, 
                "title": article_title, 
                # "date": article_date    # 时间字段可用可不用
            }
        }

        # 指定保存文件的路径，'./' 路径表示和 `scrapy.cfg` 同级。
        file_path = os.path.join('./', filename)

        # 将数据写入JSON文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
