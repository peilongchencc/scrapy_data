# QuotesBot

这是一个使用Scrapy框架的项目，旨在从 http://quotes.toscrape.com （GitHub仓库）上抓取名人名言。<br>

此项目仅用于教育目的。<br>

> 8年前的项目，可看可不看。

## Extracted data

该项目提取了名言，并结合了相应的作者姓名(author names)和标签(tags)。<br>

提取的数据如下样本所示：<br>

```txt
{
    'author': 'Douglas Adams',
    'text': '“I may not have gone where I intended to go, but I think I ...”',
    'tags': ['life', 'navigation']
}
```


## Spiders

该项目包含两个爬虫，您可以使用 `list` 命令来列出它们：

```bash
$ scrapy list
toscrape-css
toscrape-xpath
```

这两个爬虫从同一网站提取相同的数据，但是 `toscrape-css` 使用CSS选择器，而 `toscrape-xpath` 使用XPath表达式。<br>

您可以通过阅读 [Scrapy教程](http://doc.scrapy.org/en/latest/intro/tutorial.html) 来了解更多关于这些爬虫的信息。<br>


## Running the spiders

你可以使用 `scrapy crawl` 命令来运行一个爬虫，例如：<br>

```bash
$ scrapy crawl toscrape-css
```

如果你想将抓取的数据保存到文件中，可以使用 `-o` 选项：<br>

```bash
$ scrapy crawl toscrape-css -o quotes.json
```

