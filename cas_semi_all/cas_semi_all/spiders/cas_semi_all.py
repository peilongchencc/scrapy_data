import scrapy

class CasSpider(scrapy.Spider):
    name = 'cas_semi_all'
    allowed_domains = ['semi.cas.cn']
    start_urls = ['https://semi.cas.cn/']

    def parse(self, response):
        # 提取页面中的链接并跟随
        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.parse)

        # 提取并保存你想要的数据
        # 例如：抓取页面的标题
        yield {
            'title': response.css('title::text').get(),
            'url': response.url,
            # 其他你想要保存的数据
        }