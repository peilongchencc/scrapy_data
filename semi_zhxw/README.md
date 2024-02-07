## semi

### 依赖项安装:

conda安装方式:<br>

```bash
conda install -c conda-forge scrapy
```

pip安装方式:<br>

```bash
pip install Scrapy
```

笔者安装的Scrapy版本`scrapy==2.11.0 `。<br>

### 项目运行方式:

cd 到 `scrapy.cfg` 同级目录，然后终端运行以下指令:

```bash
scrapy crawl shell
```

### 备注:

爬取到的文件中，部分数据 "page_content" 为空并不是报错，是因为网页中内容是图片，没有文本可以匹配。示例如下：<br>

```txt
{
    "page_content": "",
    "metadata": {
        "source": "https://semi.cas.cn/xwdt/zhxw/202212/t20221231_6592363.html",
        "title": "首页 > 新闻动态 > 综合新闻: 新年致辞",
        "date": "2022-12-31"
    }
}
```