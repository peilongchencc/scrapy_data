# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter

import time

def current_timestamp():
    """返回当前日期时间的字符串表示形式,格式为: 2023-08-15 11:29:22 """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class MdnicePipeline:
    def process_item(self, item, spider):
        return item

class MySQLPipeline:
    """
    A pipeline to store the item in a MySQL database.
    """

    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_password):
        self.mysql_host = mysql_host
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_db=crawler.settings.get('MYSQL_DBNAME'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):
        self.connection = pymysql.connect(host=self.mysql_host,
                                        user=self.mysql_user,
                                        password=self.mysql_password,
                                        database=self.mysql_db,
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

        # 检查表是否存在，如果不存在则创建
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS article_info (
                article_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '文章的唯一ID',
                article_title VARCHAR(255) NOT NULL COMMENT '文章标题',
                article_read_count INT NOT NULL COMMENT '文章阅读数',
                article_time VARCHAR(255) NOT NULL COMMENT '文章发表时间',
                article_url VARCHAR(255) NOT NULL COMMENT '文章具体链接',
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                modify_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间'
            ) CHARSET=utf8mb4;
        """)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # 构建插入数据的SQL语句，现在包括create_time和modify_time字段
        sql = """
        INSERT INTO article_info (article_title, article_read_count, article_time, article_url, create_time, modify_time) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # 准备插入数据的值，确保顺序与上面的SQL语句中的列对应
        # 假设item中已经包含了create_time和modify_time
        values = (
            item.get('title'), 
            item.get('read_count'), 
            item.get('create_time'),  # 假设这是文章的发布时间
            item.get('url'),
            current_timestamp(),  # 使用你的函数生成插入记录的当前时间
            current_timestamp(),  # 同上，这里假设创建和修改时间相同
        )
        
        try:
            # 执行SQL语句
            self.cursor.execute(sql, values)
            # 提交到数据库执行
            self.connection.commit()
        except pymysql.MySQLError as e:
            # 如果发生错误则回滚
            print(e)
            self.connection.rollback()
        
        return item
