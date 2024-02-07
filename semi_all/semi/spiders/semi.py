import scrapy
from semi.items import SemiItem

class Mypider(scrapy.Spider):
    name = 'semi'
    allowed_domains = ['semi.cas.cn']
    start_urls = ['https://semi.cas.cn/']

    def parse(self, response):
        # 处理主页面内容，提取所有链接并跟踪它们
        for href in response.css('a::attr(href)').getall():
            yield response.follow(href, self.parse_link)

    def parse_link(self, response):
        # 根据网页类型进行不同处理
        # 假设有三种情况：Type1, Type2, Type3
        # 这里需要你根据实际情况来识别和处理这些类型

        # 示例：判断页面类型
        if "条件1" in response.text:
            yield self.parse_type1(response)
        elif "条件2" in response.text:
            yield self.parse_type2(response)
        elif "条件3" in response.text:
            yield self.parse_type3(response)
        else:
            # 其他情况的处理
            pass

    def parse_type1(self, response):
        # 处理第一种类型的页面
        item = SemiItem()
        # 示例：提取数据
        item['url'] = response.url
        item['title'] = response.css('title::text').get()
        item['content'] = response.css('body').get()
        return item

    def parse_type2(self, response):
        # 处理第二种类型的页面
        # 类似于parse_type1，但针对不同的页面结构或信息
        pass

    def parse_type3(self, response):
        # 处理第三种类型的页面
        # 类似于parse_type1和parse_type2，但针对另一种不同的页面结构或信息
        pass