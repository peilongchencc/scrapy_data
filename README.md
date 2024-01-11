# Scrapy
- [Scrapy](#scrapy)
  - [Scrapy概览:](#scrapy概览)
  - [安装方式:](#安装方式)
    - [逐步解析一个爬取器:](#逐步解析一个爬取器)
    - [具体发生了什么呢？](#具体发生了什么呢)
    - [还有呢？](#还有呢)
    - [接下来呢？](#接下来呢)
  - [Scrapy 教程:](#scrapy-教程)
    - [创建一个新的Scrapy项目:](#创建一个新的scrapy项目)
    - [我们的第一个爬虫:](#我们的第一个爬虫)
    - [怎样运行我们的爬虫:](#怎样运行我们的爬虫)
    - [刚才底层发生了什么？(What just happened under the hood?)](#刚才底层发生了什么what-just-happened-under-the-hood)
    - [start\_requests方法的快捷方式:](#start_requests方法的快捷方式)
    - [提取数据:](#提取数据)
    - [XPath: 简介(a brief intro):](#xpath-简介a-brief-intro)
    - [提取引用和作者(Extracting quotes and authors):](#提取引用和作者extracting-quotes-and-authors)
    - [在我们的爬虫程序中提取数据(Extracting data in our spider):](#在我们的爬虫程序中提取数据extracting-data-in-our-spider)
    - [将抓取的数据存储起来(Storing the scraped data):](#将抓取的数据存储起来storing-the-scraped-data)
    - [跟随链接(翻页)(Following links"):](#跟随链接翻页following-links)
    - [创建请求的快捷方式(A shortcut for creating Requests):](#创建请求的快捷方式a-shortcut-for-creating-requests)
    - [更多的例子和模式(More examples and patterns):](#更多的例子和模式more-examples-and-patterns)
    - [使用spider参数(Using spider arguments):](#使用spider参数using-spider-arguments)
    - [下一步(Next steps):](#下一步next-steps)
  - [示例(Examples):](#示例examples)
  - [选择器(Selectors):](#选择器selectors)
    - [使用选择器(Using selectors):](#使用选择器using-selectors)
      - [构造选择器(Constructing selectors):](#构造选择器constructing-selectors)
      - [使用选择器(Using selectors):](#使用选择器using-selectors-1)
      - [拓展-XPath语法解释:](#拓展-xpath语法解释)
      - [拓展--"::" 选择 "伪元素" :](#拓展---选择-伪元素-)
    - [CSS 选择器的扩展(Extensions to CSS Selectors):](#css-选择器的扩展extensions-to-css-selectors)
      - [拓展-CSS中 `#` 用法解析:](#拓展-css中--用法解析)
    - [嵌套选择器(Nesting selectors):](#嵌套选择器nesting-selectors)
  - [html中的 `href` 是什么？](#html中的-href-是什么)
  - [scrapy进行爬虫时，为什么使用yield关键字？](#scrapy进行爬虫时为什么使用yield关键字)
  - [在爬虫中，CSS和XPath是什么关系？](#在爬虫中css和xpath是什么关系)
  - [动态网页爬取:](#动态网页爬取)
    - [问题描述:](#问题描述)
    - [解决方案:](#解决方案)
  - [爬取鼠标悬停才能显示的内容:](#爬取鼠标悬停才能显示的内容)
    - [问题描述:](#问题描述-1)
    - [解决方案:](#解决方案-1)


## Scrapy概览:

Scrapy是一个用于爬行网站和提取结构化数据的应用程序框架，可用于广泛的有用应用程序，如数据挖掘、信息处理或历史档案。<br>

尽管 Scrapy 最初是为 Web 抓取而设计的，但是它也可以用于使用 API (比如 Amazon Associates Web Services)提取数据，或者作为一个通用的 Web 爬虫。<br>

## 安装方式:

conda安装方式:<br>

```bash
conda install -c conda-forge scrapy
```

pip安装方式:<br>

```bash
pip install Scrapy
```

笔者安装的Scrapy版本`scrapy==2.11.0 `，发布于2023年9月18日。<br>


### 逐步解析一个爬取器:

为了向你展示 Scrapy 带来了什么，我们将通过一个 Scrapy Spider 的例子，使用最简单的方法来运行一个 Spider。<br>

下面是一个爬虫的代码，它可以从网站 https://quotes.toscrape.com 下面的分页中找到一些著名的引言:<br>

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/tag/humor/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "author": quote.xpath("span/small/text()").get(),
                "text": quote.css("span.text::text").get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```

把它放在一个文本文件中，将它命名为`quotes_spider.py`，然后使用 `runspider` 命令运行这个爬虫:<br>

请详细解释以下终端指令:

```bash
scrapy runspider quotes_spider.py -o quotes.jsonl
```

这个终端命令使用了Scrapy，一个快速的、高层次的Web抓取和网络爬虫框架，用于Python。命令的各个部分解释如下：<br>

1. **scrapy**: 这是主命令，用来调用Scrapy工具。

2. **runspider**: 是Scrapy的一个命令，用于直接运行一个爬虫，而不需要通过创建Scrapy项目来运行。这对于快速测试或者运行单个爬虫脚本很有用。

3. **quotes_spider.py**: 这是一个Python脚本文件，其中包含了爬虫的定义。在这个文件中，你将定义爬虫的名称、开始的URL、如何跟随链接以及如何解析页面内容等。这个文件名表明这个爬虫可能是用来从某些网站抓取引用或者名言的。

4. **-o quotes.jsonl**: 这是Scrapy命令的一个参数，用来指定输出文件。

- **-o**: 这个选项用于指定输出文件的路径。在这个例子中，爬取的数据将会被输出。

- **quotes.jsonl**: 这是输出文件的名称和格式。`.jsonl`是JSON Lines的缩写，这是一种存储结构化数据的方式，其中每一行是一个有效的JSON对象。与标准的JSON文件相比，JSON Lines文件更容易被流式处理，因为每行都是独立的。

当你运行这个命令时，Scrapy将会启动并运行`quotes_spider.py`脚本中定义的爬虫，抓取数据，并将结果以JSON Lines格式保存在`quotes.jsonl`文件中。这个命令适合于快速抓取和存储数据，特别是当你不需要完整的Scrapy项目结构时。<br>


有时，你运行当前scrapy文件时，可能提示以下内容，此时运行 `pip install chardet` 即可:<br>

```txt
ImportError: cannot import name 'is_ascii' from 'charset_normalizer.utils' (/opt/anaconda3/envs/nazhi/lib/python3.10/site-packages/charset_normalizer/utils.py)
```


完成后，在 `quotes.jsonl` 文件中将有一个 JSON Lines 格式的引言列表，其中包含文本和作者，如下所示:<br>

```json
{"author": "Jane Austen", "text": "\u201cThe person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.\u201d"}
{"author": "Steve Martin", "text": "\u201cA day without sunshine is like, you know, night.\u201d"}
{"author": "Garrison Keillor", "text": "\u201cAnyone who thinks sitting in church can make you a Christian must also think that sitting in a garage can make you a car.\u201d"}
...
```

### 具体发生了什么呢？

当你运行命令 `scrapy runspider quotes_spider.py` 时，Scrapy 会寻找其中的 Spider 定义并通过其爬虫引擎运行它。<br>

爬取过程首先向 `start_urls` 属性中定义的 URL（在本例中，只有 **humor** (幽默)类别的引言的 URL）发出请求，**并调用默认的回调方法 parse** 🤨🤨🤨，将响应对象作为参数传递。在 parse 回调中，我们使用 CSS 选择器循环遍历引语元素，生成一个包含提取的引语文本和作者的 Python 字典，**寻找到下一页的链接**🐳🐳🐳并使用相同的 parse 方法作为回调来安排另一个请求。<br>

在此，你会注意到 Scrapy 的一个主要优势：**请求被安排和异步处理**。这意味着 Scrapy 不需要等待一个请求完成并处理，它可以在此期间发送另一个请求或做其他事情。这也意味着，即使某些请求失败或在处理时出现错误，其他请求也可以继续进行。<br>

虽然这使你能够进行非常快速的爬取（同时发送多个并发请求，以容错方式），Scrapy 也通过一些设置（https://docs.scrapy.org/en/latest/topics/settings.html#topics-settings-ref）让你控制爬取的礼貌性。你可以做诸如设置每个请求之间的下载延迟、限制每个域或每个 IP 的并发请求数量，甚至使用一个自动调节扩展来尝试自动地解决这些问题。<br>

### 还有呢？

您已了解如何使用Scrapy从网站提取和存储项目，但这只是冰山一角。Scrapy提供了许多强大功能，使得抓取变得简单高效，例如：

- 内置支持使用扩展的CSS选择器和XPath表达式从HTML/XML源选择和提取数据，配有辅助方法通过正则表达式提取数据。

- 一个交互式shell控制台（支持IPython），用于尝试CSS和XPath表达式来抓取数据，编写或调试您的爬虫时非常有用。

- 内置支持生成多种格式（JSON, CSV, XML）的feed导出，并能将它们存储在多种后端（FTP, S3, 本地文件系统）。

- 坚实的编码支持和自动检测功能，用于处理外来的、非标准的及损坏的编码声明。

- 强大的可扩展性支持，允许您插入自己的功能，使用信号和定义明确的API（中间件、扩展和管道）。

- 广泛的内置扩展和中间件，用于处理：
  - cookie和会话处理
  - HTTP功能，如压缩、认证、缓存
  - 用户代理伪装
  - robots.txt
  - 爬行深度限制
  - 以及更多

- 一个Telnet控制台，用于连接到运行在您的Scrapy进程中的Python控制台，以便内省和调试您的爬虫。

- 还有其他好东西，如可重用的爬虫来从站点地图和XML/CSV源抓取网站，一个自动下载与抓取项目相关的图像（或任何其他媒体）的媒体管道，一个缓存DNS解析器，以及更多！

### 接下来呢？

你接下来的步骤是安装Scrapy，跟随教程学习如何创建一个完整的Scrapy项目，并加入社区。感谢你的关注！


## Scrapy 教程:

在本教程中，我们假设你的系统上已经安装了Scrapy。如果不是这样，请参阅安装指南。<br>

我们将爬取 `quotes.toscrape.com` 这个网站，它列出了著名作者的引言。<br>

本教程将指导你完成以下任务：<br>

1. 创建一个新的Scrapy项目；

2. 编写一个爬虫来抓取网站并提取数据；

3. 使用命令行导出抓取的数据；

4. 修改爬虫以递归跟随链接；

5. 使用爬虫参数；

Scrapy是用Python编写的。如果你对这门语言不熟悉，可能想先了解一下语言的概貌，以便更好地利用Scrapy。<br>

### 创建一个新的Scrapy项目:

在你开始抓取数据之前，你需要设置一个新的Scrapy项目。进入一个你想存放代码的目录，并运行：<br>

```bash
scrapy startproject tutorial
```

这将创建一个包含以下内容的 `tutorial` 目录:<br>

```txt
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

并且终端提示以下内容:<br>

```txt
New Scrapy project 'tutorial', using template directory '/opt/anaconda3/envs/nazhi/lib/python3.10/site-packages/scrapy/templates/project', created in:
    /Users/peilongchencc/Desktop/code_draft/tutorial

You can start your first spider with:
    cd tutorial
    scrapy genspider example example.com
```


### 我们的第一个爬虫:

Spiders是你定义的类，Scrapy利用它们从一个网站（或一组网站）上抓取信息。**它们必须继承Spider类，并定义初始请求‼️**、可选地如何跟踪页面中的链接，以及如何解析下载的页面内容以提取数据。<br>

这是我们的第一个爬虫代码。请将其保存在项目的 `tutorial/spiders` 目录下，文件名为 `quotes_spider.py`：<br>

```python
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
```

正如您所见，我们的Spider子类继承了 `scrapy.Spider` 并定义了一些属性和方法：<br>

- name：标识Spider。它在一个项目中必须是唯一的，也就是说，您不能为不同的Spider设置相同的名称。🚨

- start_requests()：必须返回一个请求的可迭代对象（您可以返回一个请求列表或编写一个生成器函数），Spider将从中开始爬取。后续的请求将会依次从这些初始请求生成。

- parse()：这个方法将被调用来处理为每个请求下载的响应。response参数是一个 `TextResponse` 实例，它保存了页面内容，并提供了进一步处理它的有用方法。

通常，parse()方法会解析响应，提取作为字典的爬取数据，并且还会寻找新的URL来跟进，并从中创建新的请求（Request）。<br>

### 怎样运行我们的爬虫:

要使我们的spider正常工作，请转到项目的顶级目录(最上层的那个`tutorial`所在层级)并运行：<br>

```bash
scrapy crawl quotes
```

> 如果上面的代码中 `name = "ex"`，则运行 `scrapy crawl ex`。

这个命令会运行我们刚添加的名为 `quotes` 的爬虫，它会向 `quotes.toscrape.com` 域名发送一些请求。你将得到类似以下的输出：<br>

```txt
... (omitted for brevity)
2016-12-16 21:24:05 [scrapy.core.engine] INFO: Spider opened
2016-12-16 21:24:05 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2016-12-16 21:24:05 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (404) <GET https://quotes.toscrape.com/robots.txt> (referer: None)
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://quotes.toscrape.com/page/1/> (referer: None)
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://quotes.toscrape.com/page/2/> (referer: None)
2016-12-16 21:24:05 [quotes] DEBUG: Saved file quotes-1.html
2016-12-16 21:24:05 [quotes] DEBUG: Saved file quotes-2.html
2016-12-16 21:24:05 [scrapy.core.engine] INFO: Closing spider (finished)
...
```

现在，请检查当前目录中的文件。您应该会注意到有两个新文件被创建了：`quotes-1.html` 和 `quotes-2.html`，它们包含了各自网址的内容，正如我们的 `parse` 方法所指示的。<br>

> 如果你想知道为什么我们还没有解析HTML，别急，我们很快就会讲到这个。


### 刚才底层发生了什么？(What just happened under the hood?)

Scrapy安排由Spider的 `start_requests` 方法返回的 `scrapy.Request` 对象。每收到一个的响应后，它就会实例化 `Response` 对象并调用与请求相关联的回调方法（在这种情况下是 `parse` 方法），同时传递响应作为参数。<br>

### start_requests方法的快捷方式:

你可以不用实现一个生成 `scrapy.Request` 对象的 `start_requests()` 方法，而是直接定义一个包含URL列表的 `start_urls` 类属性。这个列表随后将被 `start_requests()` 的默认实现所使用，以创建你的爬虫的初始请求。<br>

```python
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
```

`parse()` 方法将被调用来处理对这些URL的每个请求，即使我们没有明确告诉Scrapy这样做。这是因为 `parse()` 是Scrapy的默认回调方法，对于没有明确分配回调的请求，将自动调用此方法。<br>

### 提取数据:

要学习如何使用Scrapy提取数据的最佳方式是尝试使用Scrapy shell来运行选择器。运行：<br>

```bash
scrapy shell 'https://quotes.toscrape.com/page/1/'
```

当从命令行运行Scrapy shell时，**请记得始终将网址用引号括起来**，否则含有参数（即包含&字符）的网址将无法工作。在Windows上，请使用双引号，例如：<br>

```bash
scrapy shell "https://quotes.toscrape.com/page/1/"
```

你将看到以下内容：<br>

```txt
[ ... Scrapy log here ... ]
2016-09-19 12:09:27 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://quotes.toscrape.com/page/1/> (referer: None)
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7fa91d888c90>
[s]   item       {}
[s]   request    <GET https://quotes.toscrape.com/page/1/>
[s]   response   <200 https://quotes.toscrape.com/page/1/>
[s]   settings   <scrapy.settings.Settings object at 0x7fa91d888c10>
[s]   spider     <DefaultSpider 'default' at 0x7fa91c8af990>
[s] Useful shortcuts:
[s]   shelp()           Shell help (print this help)
[s]   fetch(req_or_url) Fetch request (or URL) and update local objects
[s]   view(response)    View response in a browser
```

在Shell中，您可以尝试使用CSS及响应对象来选择元素(selecting elements)：<br>

```bash
>>> response.css("title")
[<Selector query='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
```

运行 `response.css('title')` 的结果是一个类似列表的对象，名为 `SelectorList` 。它代表了一系列的 `Selector` 对象，这些对象围绕着 `XML/HTML` 元素，并**允许你进一步查询以细化选择或提取数据**。要从上述标题中提取文本，你可以这样做：🚀<br>

```bash
>>> response.css("title::text").getall()
['Quotes to Scrape']
```

There are two things to note here: one is that we’ve added ::text to the CSS query, to mean we want to select only the text elements directly inside <title> element. If we don’t specify ::text, we’d get the full title element, including its tags:

这里有两点需要注意：一是我们在**CSS查询**中添加了 `::text` ，意味着我们只想选择 `<title>` 元素内部的**文本元素**🤨。如果我们不指定 `::text`，我们将得到完整的标题元素，包括它的标签：<br>

```bash
>>> response.css("title").getall()
['<title>Quotes to Scrape</title>']
```

另外一点是调用 `.getall()` 的结果是一个列表：选择器可能返回多于一个结果，所以我们提取它们所有。**当你知道你只想要第一个结果时**，就像在这种情况下，你可以这么做：<br>

```bash
>>> response.css("title::text").get()
'Quotes to Scrape'
```

作为替代，你也可以写成:<br>

```bash
>>> response.css("title::text")[0].get()
'Quotes to Scrape'
```

访问 `SelectorList` 实例上的索引，**如果没有结果**将会引发 `IndexError` 异常。<br>

```bash
>>> response.css("noelement")[0].get()
Traceback (most recent call last):
...
IndexError: list index out of range
```

You might want to use .get() directly on the SelectorList instance instead, which returns None if there are no results:

你可能想要直接在SelectorList实例上使用 `.get()`，如果没有结果的话，它会返回 `None`：<br>

> 直接跳到下一行，什么也不显示。

```bash
>>> response.css("noelement").get()
>>>
```

这里有一个值得学习的地方：对于大多数爬虫代码，你希望它能够对于页面上找不到内容而导致的错误具有韧性，这样即使某些部分无法爬取，你至少能获取一些数据。<br>

除了 `getall()` 和 `get()` 方法之外，你还可以使用 `re()` 方法通过**正则表达式**来提取数据✅✅✅：<br>

```bash
>>> response.css("title::text").re(r"Quotes.*")
['Quotes to Scrape']
>>> response.css("title::text").re(r"Q\w+")
['Quotes']
>>> response.css("title::text").re(r"(\w+) to (\w+)")
['Quotes', 'Scrape']
```

为了找到合适的CSS选择器，你可能会发现在你的网络浏览器中使用 `view(response)` 命令打开响应页面很有帮助。你可以使用浏览器的**开发者工具**检查HTML，并制定一个选择器（参见使用你的浏览器的开发者工具进行抓取，https://docs.scrapy.org/en/latest/topics/developer-tools.html#topics-developer-tools）。<br>

**"Selector Gadget"** 也是一个很好的工具，可以快速为视觉选定的元素找到CSS选择器，它在许多浏览器中都能工作。<br>


### XPath: 简介(a brief intro):

除了CSS，Scrapy选择器还支持使用XPath表达式：<br>

```bash
>>> response.xpath("//title")
[<Selector query='//title' data='<title>Quotes to Scrape</title>'>]
>>> response.xpath("//title/text()").get()
'Quotes to Scrape'
```

XPath表达式非常强大，它们是Scrapy选择器的基础。**实际上，CSS选择器在底层被转换为XPath**。如果你仔细阅读shell中选择器对象的文本表示，你就可以看到这一点。<br>

虽然XPath表达式可能没有CSS选择器那么流行，但它们提供了更多的能力，因为除了导航结构外，它还可以查看内容。使用XPath，你可以选择诸如 **“选择包含文本‘下一页’的链接”** 之类的元素。这使得XPath非常适合于抓取任务，即使你已经知道如何构建CSS选择器，我们也鼓励你学习XPath，它会使抓取工作变得更加容易。<br>

我们这里不会详细介绍XPath，但你可以在这里阅读更多关于[如何使用Scrapy选择器的XPath]([链接的地址](https://docs.scrapy.org/en/latest/topics/selectors.html#topics-selectors))。为了更深入地了解XPath，我们推荐这个通过[示例](https://zvon.org/comp/r/tut-XPath_1.html)学习XPath的教程，以及这个学习[“如何用XPath思考”](http://plasmasturm.org/log/xpath101/)的教程。<br>




### 提取引用和作者(Extracting quotes and authors):

现在你已经了解了选择和提取的一些知识，让我们通过编写代码来提取网页上的引用来完成我们的爬虫。<br>

在 `https://quotes.toscrape.com` 上的每个引用都是由这样的HTML元素表示的：<br>

```html
<div class="quote">
    <span class="text">“The world as we have created it is a process of our
    thinking. It cannot be changed without changing our thinking.”</span>
    <span>
        by <small class="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
    </span>
    <div class="tags">
        Tags:
        <a class="tag" href="/tag/change/page/1/">change</a>
        <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
        <a class="tag" href="/tag/thinking/page/1/">thinking</a>
        <a class="tag" href="/tag/world/page/1/">world</a>
    </div>
</div>
```

让我们打开 `scrapy shell`，稍微尝试一下，找出如何提取我们想要的数据：<br>

```bash
scrapy shell 'https://quotes.toscrape.com'
```

我们通过以下方式获取引用HTML元素的选择器列表：<br>

```bash
>>> response.css("div.quote")
[<Selector query="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>,
<Selector query="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>,
...]
```

你可以使用下列python代码整理一下获取到的内容的格式:<br>

```python
import re
import json

text_data = """
[<Selector query="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>, <Selector query="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>, <Selector query="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>, <Select...
"""

# 定义模式以从每个选择器中捕获查询和数据字段
pattern = r'<Selector query="([^"]+)" data=\'([^>]+)>'
matches = re.findall(pattern, text_data)

# 将匹配转换为更易读的格式，例如字典列表
organized_data = [{'query': match[0], 'data': match[1]} for match in matches]

# 将组织好的数据转换为格式化的字符串
pretty_data = json.dumps(organized_data, indent=2)
print(pretty_data)
```

终端输出如下:<br>

```txt
[
  {
    "query": "descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]",
    "data": "<div class=\"quote\" itemscope itemtype...'"
  },
  {
    "query": "descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]",
    "data": "<div class=\"quote\" itemscope itemtype...'"
  },
  {
    "query": "descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]",
    "data": "<div class=\"quote\" itemscope itemtype...'"
  }
]
```

上述查询返回的每个选择器(Selector)都允许我们对其子元素进行进一步的查询。让我们将第一个选择器赋值给一个变量，这样我们就可以直接在特定引语上运行我们的CSS选择器：<br>

```bash
>>> quote = response.css("div.quote")[0]
```

现在，让我们使用刚刚创建的引用对象来提取引文的文本(`text`)、作者(`author`)和标签(`tags`)：<br>

```bash
>>> text = quote.css("span.text::text").get()
>>> text
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'
>>> author = quote.css("small.author::text").get()
>>> author
'Albert Einstein'
```


给定标签(`tags`)是**字符串列表**，我们可以使用 `.getall()` 方法来获取它们所有的内容：<br>

```bash
>>> tags = quote.css("div.tags a.tag::text").getall()
>>> tags
['change', 'deep-thoughts', 'thinking', 'world']
```

我们已经弄清楚了如何提取每一个部分，现在我们可以遍历所有的**引言元素(quotes elements)**，并将它们整合成一个Python字典：<br>

```bash
>>> for quote in response.css("div.quote"):
...     text = quote.css("span.text::text").get()
...     author = quote.css("small.author::text").get()
...     tags = quote.css("div.tags a.tag::text").getall()
...     print(dict(text=text, author=author, tags=tags))
...
{'text': '“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”', 'author': 'Albert Einstein', 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
{'text': '“It is our choices, Harry, that show what we truly are, far more than our abilities.”', 'author': 'J.K. Rowling', 'tags': ['abilities', 'choices']}
...
```

### 在我们的爬虫程序中提取数据(Extracting data in our spider):

让我们回到我们的爬虫程序。到目前为止，它还没有提取任何特定的数据，只是将整个HTML页面保存到本地文件中。让我们将上面的提取逻辑整合到我们的爬虫程序中。<br>

一个典型的Scrapy爬虫通常会生成许多包含从页面提取的数据的字典。为此，我们在回调中使用Python关键字 `yield` ，正如你下面所见：<br>

> 基于异步和内存考虑，所以用 `yield` 关键字。

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
```

要运行这个爬虫，请输入以下命令退出 `scrapy shell`：<br>

```bash
quit()
```

然后运行:<br>

```bash
scrapy crawl quotes
```

现在，它应该输出提取的数据，并附有日志：<br>

```txt
2016-09-19 18:57:19 [scrapy.core.scraper] DEBUG: Scraped from <200 https://quotes.toscrape.com/page/1/>
{'tags': ['life', 'love'], 'author': 'André Gide', 'text': '“It is better to be hated for what you are than to be loved for what you are not.”'}
2016-09-19 18:57:19 [scrapy.core.scraper] DEBUG: Scraped from <200 https://quotes.toscrape.com/page/1/>
{'tags': ['edison', 'failure', 'inspirational', 'paraphrased'], 'author': 'Thomas A. Edison', 'text': "“I have not failed. I've just found 10,000 ways that won't work.”"}
```


### 将抓取的数据存储起来(Storing the scraped data):

将抓取的数据存储最简单的方法是使用 [Feed](https://docs.scrapy.org/en/latest/topics/feed-exports.html#topics-feed-exports) 导出，通过以下命令实现：<br>

```bash
scrapy crawl quotes -O quotes.json
```

这将生成一个名为 `quotes.json` 的文件，其中包含所有抓取的项目，以JSON格式序列化。<br>

命令行开关 `-O` **会覆盖任何现有文件** ⚠️；使用-o则可以将新内容 **追加** ✅到任何现有文件中。**然而，追加到JSON文件会使文件内容成为无效的JSON。当追加到文件时，考虑使用不同的序列化格式，例如JSON Lines** 🚨🚨🚨：<br>

```bahs
scrapy crawl quotes -o quotes.jsonl
```

JSON Lines格式的有用之处在于它类似于流(stream-like)，你可以轻松地向其中追加新记录。它不像JSON那样在你运行两次时会遇到同样的问题。此外，由于每条记录都是独立的一行，你可以处理大文件而无需将所有内容都放入内存中，像 [JQ](https://jqlang.github.io/jq/) 这样的工具可以帮助你在命令行上完成这些操作。<br>

在小型项目中（就像本教程中的那样），这应该就足够了。然而，如果你想对抓取的项目执行更复杂的操作，你可以编写一个 [项目管道](https://docs.scrapy.org/en/latest/topics/item-pipeline.html#topics-item-pipeline) 。当项目创建时，已经为你准备好了一个项目管道的占位文件，在 `tutorial/pipelines.py` 中。不过，如果你只是想存储抓取的项目，那么你不需要实现任何项目管道。<br>


### 跟随链接(翻页)(Following links"):

让我们假设，你不只是从 `https://quotes.toscrape.com` 网站的前两页抓取内容，而是想要从该网站的所有页面获取名言。<br>

既然你已经知道如何从页面提取数据，那么接下来让我们看看如何从这些页面中跟踪链接。<br>

首先要做的事情是提取我们想要跟踪的页面的链接。检查我们的页面，我们可以看到有一个到下一页的链接，其标记如下：<br>

```html
<ul class="pager">
    <li class="next">
        <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
    </li>
</ul>
```

我们可以尝试在命令行中提取它：<br>

```bash
>>> response.css('li.next a').get()
'<a href="/page/2/">Next <span aria-hidden="true">→</span></a>'
```

这段代码获取了锚点元素，但我们需要的是 `href` (超文本引用)属性。为此，Scrapy 支持一个 CSS 扩展，可以让你选择属性内容，像这样：<br>

```bash
>>> response.css("li.next a::attr(href)").get()
'/page/2/'
```

还有一个可用的 `attrib` 属性（更多详情见[选择元素属性](https://docs.scrapy.org/en/latest/topics/selectors.html#selecting-attributes)）。<br>

```bash
>>> response.css("li.next a").attrib["href"]
'/page/2/'
```

现在让我们看看我们的爬虫程序如何经过修改，能够递归地跟随链接到下一个页面，并从中提取数据：<br>

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
```

现在，在提取数据之后，**`parse()` 方法会查找指向下一页的链接**，并使用 `urljoin()` 方法**构建一个完整的绝对 URL**💦（因为链接可能是相对的），然后产生一个新的请求到下一页，并**将自己注册为回调函数**，以处理下一页的数据提取，并继续通过所有页面进行爬取。<br>

你在这里看到的是 Scrapy 跟随链接的机制：当你在回调方法中产生一个请求时，Scrapy 将安排发送该请求，并注册一个回调方法，在该请求完成时执行。<br>

利用这种方式，你可以构建复杂的爬虫，这些爬虫根据你定义的规则跟随链接，并根据它访问的页面提取不同类型的数据。<br>

在我们的例子中，它创建了一种循环，跟随所有指向下一页的链接，直到找不到为止——这对于爬取博客、论坛和其他带有分页的网站非常方便。<br>


### 创建请求的快捷方式(A shortcut for creating Requests):

你可以使用 `response.follow` 作为**创建 `Request` 对象**的快捷方式:<br>

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("span small::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
```

与 `scrapy.Request` 不同，`response.follow` **直接支持相对 URL** - 不需要调用 `urljoin`。请注意，`response.follow` 只是返回一个 `Request` 实例；你仍然需要 `yield` 这个 `Request`。<br>

你还可以传递一个选择器给 `response.follow`，而不是一个字符串；这个选择器应该提取必要的属性：<br>

```python
for href in response.css("ul.pager a::attr(href)"):
    yield response.follow(href, callback=self.parse)
```

`response.css("ul.pager a::attr(href)")` 返回的内容如下:<br>

```bash
>>> response.css("ul.pager a::attr(href)")
[<Selector query="descendant-or-self::ul[@class and contains(concat(' ', normalize-space(@class), ' '), ' pager ')]/descendant-or-self::*/a/@href" data='/page/2/'>]
```

🤭🤭🤭对于 `<a>` 元素，有一个快捷方式：`response.follow` 会自动使用它们的 `href` 属性。因此，代码可以进一步简化：<br>

```python
for a in response.css("ul.pager a"):
    yield response.follow(a, callback=self.parse)
```

要从一个可迭代对象创建多个请求，你可以使用 `response.follow_all` 替代：<br>

```python
anchors = response.css("ul.pager a")
yield from response.follow_all(anchors, callback=self.parse)
```

或者，进一步简化为：<br>

```python
yield from response.follow_all(css="ul.pager a", callback=self.parse)
```


### 更多的例子和模式(More examples and patterns):

这是另一个爬虫示例，用于展示回调和跟踪链接，这次是用来抓取作者信息的：<br>

```python
import scrapy


class AuthorSpider(scrapy.Spider):
    name = "author"

    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        author_page_links = response.css(".author + a")
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css("li.next a")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        yield {
            "name": extract_with_css("h3.author-title::text"),
            "birthdate": extract_with_css(".author-born-date::text"),
            "bio": extract_with_css(".author-description::text"),
        }
```

这个爬虫将从主页开始，它会跟踪所有指向作者(authors)页面的链接，并对每个页面调用 `parse_author` 回调函数，同时也会跟踪分页链接，并像我们之前看到的那样使用 `parse` 回调函数。<br>

这里我们将回调函数作为位置参数传递给 `response.follow_all`，以简化代码；这对于 `Request` 也同样适用。<br>

`parse_author` 回调函数定义了一个辅助函数，**用于提取和清理 CSS 查询的数据，并生成包含作者数据的 Python 字典。** <br>

🌿🌿🌿🌿🌿🌿<br>

这个爬虫展示的另一个有趣之处在于，即使有许多来自同一作者的引用，我们也不需要担心多次访问同一个作者的页面。默认情况下，`Scrapy` 会过滤掉对已访问过的 `URL` 的重复请求，避免了因编程错误而过度请求服务器的问题。这可以通过设置 `DUPEFILTER_CLASS` 来配置。<br>

🌿🌿🌿🌿🌿🌿<br>

希望到目前为止，你已经对如何使用 `Scrapy` 的跟踪链接和**回调机制**有了良好的理解。<br>

作为另一个利用跟踪链接机制的示例爬虫，请查看 `CrawlSpider` 类，这是一个通用的爬虫，实现了一个小规则引擎，你可以在其基础上编写你的爬虫。<br>

此外，一个常见的模式是从多个页面构建一个项目，使用一种技巧将额外的数据传递给回调函数。<br>


### 使用spider参数(Using spider arguments):

你可以在运行爬虫时使用 `-a` 选项为您的爬虫提供命令行参数：<br>

```bash
scrapy crawl quotes -O quotes-humor.json -a tag=humor
```

这些参数会传递给Spider的 __init__ 方法，并默认成为Spider的属性。<br>

在这个例子中，为 `tag` 参数提供的值将通过 `self.tag` 可用。你可以利用这一点来让你的Spider只抓取带有特定标签的引用，根据参数构建URL：<br>

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = "https://quotes.toscrape.com/"
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = url + "tag/" + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```

如果你向这个爬虫传递了 `tag=humor` 参数，你会发现它只会访问带有 **`humor`** 标签的URL，比如 `https://quotes.toscrape.com/tag/humor。` <br>

[你可以在这里了解更多关于处理爬虫参数的信息](https://docs.scrapy.org/en/latest/topics/spiders.html#spiderargs)。<br>

### 下一步(Next steps):

本教程仅涵盖了 `Scrapy` 的基础知识，但还有许多其他特性在此未提及。请查看 [ Scrapy at a glance](https://docs.scrapy.org/en/latest/intro/overview.html#intro-overview) 章节中的 [What else?](https://docs.scrapy.org/en/latest/intro/overview.html#topics-whatelse) 部分，以快速了解最重要的特性。<br>

你可以从 [Basic concepts](https://docs.scrapy.org/en/latest/index.html#section-basics) 部分继续学习，了解更多关于命令行工具、爬虫、选择器以及本教程未涉及的其他内容，比如对抓取数据的建模。如果您更喜欢通过实例项目进行学习，请查看 [Examples](https://docs.scrapy.org/en/latest/intro/examples.html#intro-examples) 部分。<br>


## 示例(Examples):

学习最好的方式是通过实例，`Scrapy` 也不例外。因此，有一个名为 [quotesbot](https://github.com/scrapy/quotesbot) 的示例 Scrapy 项目，你可以用它来进行实践并更深入地了解 Scrapy。该项目包含了针对 https://quotes.toscrape.com 的**两个爬虫，一个使用 CSS 选择器，另一个使用 XPath 表达式**。<br>

`quotesbot` 项目可在以下地址找到：`https://github.com/scrapy/quotesbot`。你可以在项目的 `README` 文件中找到更多关于它的信息。<br>

> 笔者在当前项目下，下载了该项目，项目文件夹名称为: `quotesbot`。

如果你熟悉 git，你可以检查代码。否则，你可以通过点击 [这里](https://github.com/scrapy/quotesbot/archive/master.zip) 下载项目的 zip 文件。<br>


## 选择器(Selectors):

在进行网页抓取时，你**最常需要执行的任务是从HTML源代码中提取数据**。有几个库可用于实现这一目标，例如：<br>

- `BeautifulSoup` 是一个在 Python 程序员中非常受欢迎的网页抓取库，它基于 HTML 代码的结构构建一个 Python 对象，并且对于糟糕的标记也处理得相当不错，但**它有一个缺点：速度慢。🚨**

- `lxml` 是一个基于 `ElementTree` 的具有 pythonic API 的 **XML 解析库（也可解析 HTML）**。（lxml 不是 Python 标准库的一部分。）

Scrapy 自带了提取数据的机制。它们被称为选择器，因为它们通过 `XPath` 或 `CSS` 表达式 “选择” HTML 文档中的特定部分。<br>

XPath 是一种用于选择 XML 文档中节点的语言，也可用于 HTML。CSS 是一种应用于 HTML 文档的样式语言。它定义了选择器，将这些样式与特定的 HTML 元素相关联。<br>

⚠️注意:<br>

Scrapy 选择器是围绕 parsel 库的一个薄包装层；这个包装层的目的是为了更好地与 Scrapy 响应对象集成。<br>

parsel 是一个独立的网页抓取库，可以在不使用 Scrapy 的情况下使用。它在底层使用 lxml 库，并在 lxml API 之上实现了一个简单的 API。这意味着 Scrapy 选择器在速度和解析准确性上与 lxml 非常相似。<br>

### 使用选择器(Using selectors):

#### 构造选择器(Constructing selectors):

`Response` 对象在 `.selector` 属性上暴露了一个 Selector 实例：<br>

```bash
>>> response.selector.xpath("//span/text()").get()
'good'
```

使用 XPath 和 CSS 查询响应(Querying responses)是非常常见的，因此响应(responses)还包括了两个更便捷的快捷方式：`response.xpath()` 和 `response.css()`：<br>

```bash
>>> response.xpath("//span/text()").get()
'good'
>>> response.css("span::text").get()
'good'
```

Scrapy 选择器是通过传递 `TextResponse` 对象或标记（作为字符串，在 text 参数中）来构建的 Selector 类的实例。<br>

通常不需要手动构建 Scrapy 选择器：在 Spider 回调中可以使用 `response` (响应)对象，因此在大多数情况下，使用 `response.css()` 和 `response.xpath()` 这些快捷方式更为方便。通过使用 `response.selector` 或这些快捷方式，你还可以确保响应体只被解析一次。<br>

但如果需要，也可以直接使用 `Selector`。从文本构建：<br>

```bash
>>> from scrapy.selector import Selector
>>> body = "<html><body><span>good</span></body></html>"
>>> Selector(text=body).xpath("//span/text()").get()
'good'
```

从response(响应)构建 - `HtmlResponse` 是 `TextResponse` 子类之一：<br>

```bash
>>> from scrapy.selector import Selector
>>> from scrapy.http import HtmlResponse
>>> response = HtmlResponse(url="http://example.com", body=body, encoding="utf-8")
>>> Selector(response=response).xpath("//span/text()").get()
'good'
```

`Selector` (选择器)会根据输入类型自动选择最佳的解析规则（XML 对比 HTML）。<br>

#### 使用选择器(Using selectors):

为了解释如何使用选择器，我们将使用 `Scrapy shell`（它提供了交互式测试）和位于 Scrapy 文档服务器上的一个示例页面：<br>

- https://docs.scrapy.org/en/latest/_static/selectors-sample1.html

为了完整性，这里是它的完整 HTML 代码：<br>

```html
<!DOCTYPE html>

<html>
  <head>
    <base href='http://example.com/' />
    <title>Example website</title>
  </head>
  <body>
    <div id='images'>
      <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' alt='image1'/></a>
      <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' alt='image2'/></a>
      <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' alt='image3'/></a>
      <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' alt='image4'/></a>
      <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' alt='image5'/></a>
    </div>
  </body>
</html>
```

首先，让我们打开 shell：<br>

```bash
scrapy shell https://docs.scrapy.org/en/latest/_static/selectors-sample1.html
```

然后，在 shell 加载后，你将在 `response shell` 变量中拥有可用的 `response` (响应)，并且其附加的选择器位于 `response.selector` 属性中。<br>

由于我们处理的是 HTML，选择器将自动使用 HTML 解析器。<br>

因此，通过查看该页面的 HTML 代码，让我们构造一个 XPath，用于选择 title 标签(tag)内的文本(text)：<br>

```bash
>>> response.xpath("//title/text()")
[<Selector query='//title/text()' data='Example website'>]
```

要真正提取文本数据，你必须调用选择器的 `.get()` 或 `.getall()` 方法，如下所示：<br>

```bash
>>> response.xpath("//title/text()").getall()
['Example website']
>>> response.xpath("//title/text()").get()
'Example website'
```

`.get()` 总是返回单个结果；**如果有多个匹配项，将返回第一个匹配项的内容；** 如果没有匹配项，则返回 None。`.getall()` 返回包含所有结果的列表。<br>

请注意，CSS 选择器可以使用 CSS3 伪元素选择文本或属性节点：<br>

```bash
>>> response.css("title::text").get()
'Example website'
```

如你所见，`.xpath()` 和 `.css()` 方法返回一个 `SelectorList` 实例，这是一个新选择器的列表。这个 API 可用于快速选择嵌套数据：<br>

```bash
>>> response.css("img").xpath("@src").getall()
['image1_thumb.jpg',
'image2_thumb.jpg',
'image3_thumb.jpg',
'image4_thumb.jpg',
'image5_thumb.jpg']
```

如果您只想提取第一个匹配的元素，可以调用选择器的 `.get()` 方法（或其在之前 Scrapy 版本中常用的别名 `.extract_first()`）：<br>

```bash
>>> response.xpath('//div[@id="images"]/a/text()').get()
'Name: My image 1 '
```

如果没有找到元素，它将返回 `None`：<br>

```bash
>>> response.xpath('//div[@id="not-exists"]/text()').get() is None
True
```

可以提供一个默认的返回值作为参数，以代替 `None` 使用：<br>

```bash
>>> response.xpath('//div[@id="not-exists"]/text()').get(default="not-found")
'not-found'
```

可以不使用例如 `'@src'` 的 **XPath**，而是通过选择器的 `.attrib` 属性来查询属性：<br>

```bash
>>> [img.attrib["src"] for img in response.css("img")]
['image1_thumb.jpg',
'image2_thumb.jpg',
'image3_thumb.jpg',
'image4_thumb.jpg',
'image5_thumb.jpg']
```

作为一种快捷方式，`.attrib` 也可以直接在 `SelectorList` 上使用；它返回第一个匹配元素的属性：<br>

```bash
>>> response.css("img").attrib["src"]
'image1_thumb.jpg'
```

这在只期望单个结果时最有用，例如通过 `id` 选择，或在网页上选择独特的元素时：<br>

```bash
>>> response.css("base").attrib["href"]
'http://example.com/'
```

`<base>` 标签位于`<head>`部分：<br>

```html
<base href='http://example.com/' />
```

这个`<base>`标签为页面上的所有相对URL指定了一个基础URL。在这个例子中，基础URL被设置为`'http://example.com/'`。这意味着页面中所有相对路径的URL（如在`<a>`标签中的`href`属性）都会以这个URL作为其基础。<br>

因此，在Scrapy中使用`response.css("base").attrib["href"]`能够成功地提取出`<base>`标签的`href`属性值，即`'http://example.com/'`。这在处理和构建完整的绝对URL时非常有用，特别是当页面中包含大量相对路径的链接时。<br>

> `<base>`标签在HTML中是一个不常用的标签，它用于指定页面内所有相对URL的基础URL。如果HTML中没有`<base>`标签，这段代码会返回一个错误或空值，因为它试图访问不存在的元素的属性。这种情况下，使用这段代码之前检查HTML是否包含`<base>`标签是一个好习惯。


现在我们将获取 **基础URL** 和一些 **图片链接** ：<br>

```bash
>>> response.xpath("//base/@href").get()
'http://example.com/'
```

代码详解：<br>

1. `response`: 这是Scrapy中的一个响应对象，代表了爬虫下载的页面。

2. `.xpath("//base/@href")`: 这是一个XPath选择器。XPath是一种在XML和HTML文档中查找信息的语言。这里的`//base/@href`意味着查找所有`<base>`标签的`href`属性。具体来说，`//`表示选择文档中所有符合条件的节点，`base`是HTML中的一个特定标签，而`@href`表示选择这个标签的`href`属性。

3. `.get()`: 这个方法用于获取XPath选择器找到的第一个匹配项的数据。

综上所述，这行代码的作用是从下载的网页中找出第一个`<base>`标签的`href`属性值。在这个示例中，返回的结果是`'http://example.com/'`，这意味着在爬取的页面中，`<base>`标签的`href`属性被设置为`http://example.com/`。这通常用于解析网页的基础URL或根URL。<br>


```bash
>>> response.css("base::attr(href)").get()
'http://example.com/'
```

`response` : 是 Scrapy 框架中的一个响应对象，包含了一个网页的全部内容。<br>

`.css("base::attr(href)")`: <br>

- `.css("...")` 是 Scrapy 用于选择网页上元素的方法，它使用 CSS 选择器来定位元素。

- `"base"` 指的是 `<base>` 标签，这是 HTML 中用于指定相对 URL 的基础路径的标签。

- `"::attr(href)"` 是一个伪类选择器，用于获取该元素的 `href` 属性值。在这种情况下，它提取的是 `<base>` 标签的 `href` 属性值。

`.get()`: 这个方法从选择的元素中提取出第一个匹配项的数据。如果你想获取所有匹配项，可以使用 `.getall()` 方法。<br>

总的来说，这段代码的目的是提取网页中 `<base>` 标签的 `href` 属性值。在这个示例中，它返回的是 `'http://example.com/'`，这通常是用来解析页面上的相对 URL 的基础 URL。<br>

```bash
>>> response.css("base").attrib["href"]
'http://example.com/'
```

```bash
>>> response.xpath('//a[contains(@href, "image")]/@href').getall()
['image1.html',
'image2.html',
'image3.html',
'image4.html',
'image5.html']
```

1. `response`: 这是一个 Scrapy Response 对象，代表了一个已经爬取到的网页。

2. `.xpath('//a[contains(@href, "image")]')`: 这是一个 XPath 查询。它的作用是在整个文档中查找所有 `<a>` 标签，其中的 `href` 属性包含了字符串“image”。`//` 表示在整个文档中查找，`a` 是 HTML 中用于创建链接的标签，`contains(@href, "image")` 是一个函数，用于查找 `href` 属性中包含“image”字样的 `<a>` 标签。

3. `/@href`: 这部分从上面找到的 `<a>` 标签中提取 `href` 属性的值。

4. `.getall()`: 这是 Scrapy 中的一个方法，用于从 XPath 查询结果中提取所有匹配项的值。在这个例子中，它将会提取所有符合条件的 `href` 属性值。

总的来说，这个特定的代码片段是用来提取网页中所有包含“image”字样在其 href 属性中的 `<a>` 标签的 href 值。<br>

```bash
>>> response.css("a[href*=image]::attr(href)").getall()
['image1.html',
'image2.html',
'image3.html',
'image4.html',
'image5.html']
```

`.css("a[href*=image]::attr(href)")` 是一个CSS选择器。这里的意思是：“选择所有 `href` 属性中包含 'image' 字符串的 `<a>` 标签，并获取这些标签的 `href` 属性值。”<br>

- `a` 表示选择所有的锚点（链接）标签 `<a>`。

- `[href*=image]` 是一个属性选择器，用于选择那些 `href` 属性中包含“image”文本的 `<a>` 标签。星号 `*=` 表示属性值包含特定字符串。

- `::attr(href)` 用于获取每个符合条件的 `<a>` 标签的 `href` 属性值。

`.getall()` 是一个方法，用于获取所有匹配的元素的列表，而不只是第一个匹配项。<br>

总的来说，这段代码的作用是从HTML中提取所有 `<a>` 标签的 `href` 属性值，这些标签的 `href` 属性包含字符串“image”。<br>

根据上面提供的HTML示例，它会返回以下列表：<br>

```python
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
```

这些是包含在`<div id='images'>`内部的五个图片链接的地址。<br>


```bash
response.xpath('//a[contains(@href, "image")]/img/@src').getall()
['image1_thumb.jpg',
'image2_thumb.jpg',
'image3_thumb.jpg',
'image4_thumb.jpg',
'image5_thumb.jpg']
```

#### 拓展-XPath语法解释:

```bash
response.xpath('//a[contains(@href, "image")]/img/@src').getall()
['image1_thumb.jpg',
'image2_thumb.jpg',
'image3_thumb.jpg',
'image4_thumb.jpg',
'image5_thumb.jpg']
```

这里根据上述语法详细解释这个XPath查询的各个组成部分。XPath是一种在XML和HTML文档中查找信息的语言。在上述例子中，XPath用于定位和提取特定的HTML元素。下面是各个部分的详细解释：<br>

1. `//`

- `//` 是XPath的语法，用于选择文档中的节点，而不考虑它们在文档中的位置。例如，`//div` 会选择文档中的所有`<div>`元素。

2. `[]`

- `[]` 用于**在XPath中添加条件**。它可以用来进一步细化你想要选择的节点。例如，`//a[condition]` 会选择满足`condition`条件的所有`<a>`元素。

3. `contains`

- `contains()` 是一个XPath函数，用于检查一个字符串是否包含另一个字符串。在你的例子中，`contains(@href, "image")` 用于检查`href`属性的值是否包含字符串“image”。

4. `@`

- `@` 在XPath中用于指代一个属性。例如，`@href` 表示选择`href`属性。

5. `/`

- `/` 在XPath中用作路径分隔符。它**用于选择直接的子节点**。例如，`div/a` 会选择所有`<div>`元素的直接子`<a>`元素。

将这些组件放在一起理解：<br>

- `//a[contains(@href, "image")]`：这个表达式选择文档中所有`<a>`元素，这些`<a>`元素的`href`属性中包含字符串“image”。`//` 表示在整个文档中搜索，`a` 指定要搜索的元素类型，`contains(@href, "image")` 是一个条件，表示仅选择那些`href`属性中包含“image”的`<a>`元素。

- `/img/@src`：这个表达式是在上面找到的每个`<a>`元素的基础上进一步定位。它选择这些`<a>`元素的子元素`<img>`，并提取这些`<img>`元素的`src`属性。`/img` 指定选择`<img>`子元素，`@src` 表示提取这些`<img>`元素的`src`属性值。

所以，整个表达式`//a[contains(@href, "image")]/img/@src` 会找到文档中所有其`href`属性包含“image”的`<a>`元素，然后从这些`<a>`元素的子元素`<img>`中提取`src`属性值。这通常是图片的URL。<br>


```bash
response.css("a[href*=image] img::attr(src)").getall()
['image1_thumb.jpg',
'image2_thumb.jpg',
'image3_thumb.jpg',
'image4_thumb.jpg',
'image5_thumb.jpg']
```

命令解释:<br>

1. `[]`（方括号）：用于属性选择器。当你需要选择具有特定属性的HTML元素时，你可以在元素名后使用方括号来指定属性。例如，在`a[href]`中，它选择所有具有`href`属性的`<a>`元素。

2. `*=`：这是一种属性选择器的操作符，用于选择属性值中包含特定文本的元素。例如，在`[href*=image]`中，`*=`操作符用于选择那些`href`属性中包含"image"文本的元素。这意味着它会匹配任何`href`值中含有"image"这个子串的元素。

3. `::`：用于伪元素选择器。在CSS中，伪元素用于添加一些特殊的效果或者选择某些部分的元素，而不是整个元素。例如，`::attr(src)`是一个伪元素选择器，用于获取元素的`src`属性。在你的代码示例中，`img::attr(src)`选择了所有`<img>`元素，并获取了它们的`src`属性值。

所以，在你的Scrapy代码示例 `response.css("a[href*=image] img::attr(src)").getall()` 中，它首先选择所有`href`属性中包含"image"的`<a>`元素，然后在这些`<a>`元素中选择`<img>`元素，并提取这些`<img>`元素的`src`属性值。


#### 拓展--"::" 选择 "伪元素" :

理解伪元素的概念对于掌握CSS选择器非常重要。伪元素是CSS的一个特性，它用于**指定页面上某个元素的某个部分或者添加特定的效果**。伪元素不是HTML文档中实际定义的元素，而是CSS创建的虚拟元素，用于应用样式或选择文档中的特定内容。<br>

在Scrapy中，使用CSS选择器时，伪元素`::`的使用略有不同。在Scrapy中，伪元素主要用于提取元素的特定属性。例如：<br>

- `::text`：这个伪元素用于选择元素的文本内容。例如，`p::text`会选择所有`<p>`标签中的文本(text)。

- `::attr(attribute-name)`：这个伪元素用于提取元素的特定属性值。例如，`img::attr(src)`会选择所有`<img>`标签的`src`属性值。

在你的Scrapy代码示例中，`img::attr(src)`表示选择每个`<img>`元素的`src`属性。这是一个非常有用的特性，因为它允许你直接提取HTML元素的属性，而不仅仅是元素本身。这在网络爬虫和数据提取中尤其有用，因为它提供了一种简洁的方法来获取诸如图像链接、页面链接等信息。<br>


### CSS 选择器的扩展(Extensions to CSS Selectors):

根据 W3C 标准，CSS 选择器不支持选择文本节点(text nodes)或属性值(attribute values)。但在网页抓取环境中，选择这些内容是非常必要的，因此**Scrapy(parsel)** 实现了一些非标准的伪元素：<br>

- 要选择文本节点(text nodes)，请使用 `::text`

- 要选择属性值(attribute values)，请使用 `::attr(name)`，其中 `name` 是你想要获取其值的属性的名称

🚨🚨🚨警告：<br>

这些伪元素是专门为 `Scrapy(parsel)` 设计的。它们很可能不适用于其他库，如 `lxml` 或 `PyQuery`。<br>

示例：<br>

- `title::text` 选择 <title> 元素的后代中的子文本节点(text nodes)：

```bash
>>> response.css("title::text").get()
'Example website'
```

`*::text`选择当前选择器上下文的所有后代文本节点。<br>

```bash
>>> response.css("#images *::text").getall()
['\n   ',
'Name: My image 1 ',
'\n   ',
'Name: My image 2 ',
'\n   ',
'Name: My image 3 ',
'\n   ',
'Name: My image 4 ',
'\n   ',
'Name: My image 5 ',
'\n  ']
```

命令解释:<br>

1. **`response`**：这是Scrapy中的一个对象，代表了爬虫获取的网页的响应。它包含了你请求的网页的全部内容。

2. **`css` 方法**：这是Scrapy Response对象的一个方法，用于对网页内容应用CSS选择器。CSS选择器是一种表达式，用于从HTML文档中选择元素。在这个上下文中，它被用来找到特定的HTML元素。

3. **`"#images *"`**：这是一个CSS选择器。`#images` 选择了所有id为`images`的元素（通常是一个div或其他容器元素）。星号（`*`）是一个通配符，表示选择`#images`元素内的所有子元素。所以，这个选择器的目的是选取id为`images`的元素下的所有内容。

```html
<div id='images'>
    <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' alt='image1'/></a>
    ... ...
</div>
```

4. **`::text`**：这是一个CSS伪元素选择器，用于选择元素的文本内容。在这个例子中，它会选择所有由`#images *`选择器找到的元素的文本内容。

5. **`getall()` 方法**：这个方法是用来提取所有匹配的选择器的数据。在这个例子中，它会返回所有由`#images *::text`选择器找到的文本内容的列表。

总结来说，这个命令在Scrapy中的作用是选取id为`images`的元素内的所有子元素的文本内容，并将这些文本内容作为一个列表返回。这在爬虫中常用于提取页面特定部分的所有文本数据。<br>


#### 拓展-CSS中 `#` 用法解析:

`#` 符号在CSS选择器中用来指定一个特定的id。在HTML中，id属性是用来唯一标识页面上的一个元素。每个id在一个HTML文档中应该是独一无二的，这意味着没有两个元素应该有相同的id值。<br>

当你在CSS选择器中使用 `#` 符号，后面紧跟一个id的值，选择器就会匹配所有具有那个特定id的元素。例如：<br>

- `#header` 会选择ID为 `header` 的元素。
- `#main-content` 会选择ID为 `main-content` 的元素。

这使得id选择器非常有用于定位页面上的特定元素，尤其是当你只对文档中的一个特定部分感兴趣时。在Web开发和网页数据抓取中，利用ID选择器可以精确地选择需要操作或提取数据的部分。<br>

了解HTML的基础对理解id的含义非常重要。HTML（超文本标记语言）是用于创建网页的标准标记语言。在HTML中，一个网页由许多不同的元素构成，比如段落、标题、图片等。这些元素通过标签（如 `<p>`、`<h1>`、`<img>` 等）来定义。<br>

在这些HTML元素中，`id` 属性是一个特别的属性，用于给元素指定一个唯一的标识符（ID）。这个ID在整个HTML文档中必须是唯一的。通过使用这个ID，你可以对特定的HTML元素进行定位和操作。这在网页设计和开发中非常有用，尤其是在使用CSS（用于设置网页样式的语言）和JavaScript（网页上用于添加交互性的编程语言）时。<br>

例如，一个简单的HTML元素带有ID可能是这样的：<br>

```html
<p id="first-paragraph">这是一个段落。</p>
```

在这个例子中，`<p>` 是一个段落标签，`id="first-paragraph"` 给这个段落指定了一个唯一的ID，即 `first-paragraph`。你可以在CSS中使用这个ID来特定地选择和样式化这个段落，或者在JavaScript中用它来获取或操作这个段落的内容。<br>

当你在CSS选择器中使用 `#` 符号，比如 `#first-paragraph`，这会选择所有ID为 `first-paragraph` 的元素。这就是ID在HTML中的基本用途和含义。<br>

如果 `foo` 元素存在但不包含任何文本（即文本为空）时，`foo::text` 将不返回任何结果:<br>

```bash
>>> response.css("img::text").getall()
[]

This means ``.css('foo::text').get()`` could return None even if an element
exists. Use ``default=''`` if you always want a string:
```

```bash
>>> response.css("img::text").get()
>>> response.css("img::text").get(default="")
''
```

`a::attr(href)` 选择其后链接的 `href` 属性值:<br>

```bash
>>> response.css("a::attr(href)").getall()
['image1.html',
'image2.html',
'image3.html',
'image4.html',
'image5.html']
```

### 嵌套选择器(Nesting selectors):

这个问题可以通过计算投资回报来分析哪种策略更精明。

首先，我们分析你的策略：
1. 你首先以6块一颗的价格购买了350颗果子，总成本为 \( 350 \times 6 = 2100 \) 块。
2. 然后你在果子价格涨到10块一颗时卖出350颗，总收入为 \( 350 \times 10 = 3500 \) 块。
3. 接着，你在价格为8块一颗时买回了100颗果子，总支出为 \( 100 \times 8 = 800 \) 块。
4. 最终，你的净收入为 \( 3500 - 2100 - 800 = 600 \) 块。

接下来，我们分析另一个策略：
1. 首先是相同的购买，以6块一颗的价格购买了350颗果子，总成本 \( 2100 \) 块。
2. 然后在价格达到10块时，仅卖出250颗，总收入为 \( 250 \times 10 = 2500 \) 块。
3. 保留100颗果子，因此没有进一步的买入或卖出。
4. 最终，这种策略的净收入为 \( 2500 - 2100 = 400 \) 块。

从这个分析来看，你的策略（最终净收入600块）比另一个策略（最终净收入400块）更精明，因为它带来了更高的净收入。



问你个问题：

现在有一堆果子，价格为6块一颗，你需要100颗果子自己用。

你打听到果灾将要爆发，这果子肯定涨价。

你想捞一笔，于是，你花了大量资金6块买了350颗果子，第二天果子真的开始涨价。

果子10块一颗的时候，你卖出了350颗果子，然后8块的时候你买入了自己需要的100颗果子。

另外有人说，要是他就买了350颗果子后，直接留下100颗，剩下的250颗果子在10块一颗的时候全部卖出。

提问，究竟谁更精明？是第一个人还是第二个人？

能否以差价的方式来估算谁赚得多呢？两个人的净收益分别是多少呢？两个人的净利润分别是多少呢？


我看到有人使用下列的算式表示第一个人赚的更多，下面的算式究竟是在算什么呢？

我是以差价盈利的方式看出第一个人赚的多的，你是怎么看的？

> 6块 --> 10块赚4块，10块 --> 8块亏2块。

第一个人： 4x(250+100)-2x100

第二个人： 4x250


这个问题其实可以通过比较两种策略的差价来简单分析谁赚得更多。

第一种策略：
1. 花费 \(6 \times 350 = 2100\) 块买入350颗果子。
2. 以 \(10 \times 350 = 3500\) 块卖出350颗果子，获利 \(3500 - 2100 = 1400\) 块。
3. 然后以 \(8 \times 100 = 800\) 块买入100颗果子。

总获利为 \(1400 - 800 = 600\) 块。

第二种策略：
1. 花费 \(6 \times 350 = 2100\) 块买入350颗果子。
2. 保留100颗自用，剩下 \(350 - 100 = 250\) 颗果子以 \(10 \times 250 = 2500\) 块卖出，获利 \(2500 - 2100 = 400\) 块。

比较两种策略：
- 第一种策略的总获利是 \(600\) 块。
- 第二种策略的总获利是 \(400\) 块。

因此，第一种策略的获利更多。这个结论是基于差价进行的简单计算，没有涉及复杂的详细计算。



我的理解是：果子6块一颗的时候，直接留下100颗果子少赚了6块到8块的差价，所以第一个人赚得多，但总感觉我忽略了点什么。





## html中的 `href` 是什么？

在HTML（超文本标记语言）中，`href` 是一个属性，通常用在 `<a>` （锚点）标签中。`href` 代表 "Hypertext Reference"，即 "超文本引用"。这个属性指定了一个链接的目的地地址，当用户点击这个链接时，浏览器会跳转到这个地址。<br>

例如：<br>

```html
<a href="https://www.example.com">访问例子网站</a>
```

在这个例子中，`<a>` 标签创建了一个到 "https://www.example.com" 的链接。当用户点击这个链接时，他们的浏览器会跳转到 "Example.com" 网站。<br>

`href` 属性不仅限于网页链接，它也可以用于指向电子邮件地址、文件、电话号码等。例如，创建一个指向电子邮件的链接：<br>

```html
<a href="mailto:someone@example.com">发送电子邮件</a>
```

在这个例子中，点击链接将会打开用户的默认邮件客户端，并创建一个发送到 "someone@example.com" 的新邮件。<br>


## scrapy进行爬虫时，为什么使用yield关键字？

在使用Scrapy进行爬虫时，`yield` 关键字的使用是出于以下几个原因：<br>

1. **异步处理：** Scrapy 是基于Twisted，一个异步网络框架。`yield` 关键字用于生成一个生成器（generator），允许Scrapy在爬虫过程中暂停和恢复请求，而不会阻塞整个爬虫的执行。这是异步编程的一部分，有助于提高爬虫的效率和速度。

2. **内存效率：** 使用 `yield`，爬虫在处理单个页面或请求时不需要将所有数据一次性加载到内存中。这意味着即使在处理大量数据时，爬虫也能保持较低的内存占用。

3. **流式处理数据：** `yield` 允许Scrapy一边下载网页，一边处理页面内容。这种流式处理方式可以更快地处理数据，尤其是在处理包含大量链接的大型网站时。

4. **方便的数据处理和管道集成：** 通过 `yield` 返回的项目或请求可以被Scrapy的其他组件（如Item Pipeline）轻松接收和处理。这样可以灵活地将爬取的数据传递给不同的后处理组件。

总之，使用 `yield` 关键字可以让Scrapy爬虫更加高效、灵活，并且能够更好地管理资源，特别是在处理大规模数据抓取时。<br>


## 在爬虫中，CSS和XPath是什么关系？

在爬虫领域，CSS选择器和XPath是两种常见的方法，用于从HTML文档中提取信息。虽然它们都用于相同的目的，但它们在语法和使用方式上有所不同。<br>

1. **CSS选择器**：

- CSS选择器是用于选择HTML文档中元素的模式，以便对元素应用样式。在爬虫中，CSS选择器被用来定位和提取HTML中的特定数据。

- CSS选择器简洁明了，易于学习，特别是如果你已经熟悉前端开发。

- 例如，要选择所有的`<h1>`标签，你会使用`h1`作为选择器。

2. **XPath**：

- XPath（XML路径语言）是一种在XML文档中查找信息的语言，它也可以用于HTML文档，因为HTML是XML的一个子集。

- XPath非常强大和灵活，允许你进行非常具体且复杂的查询。

- 例如，要选择所有的`<h1>`标签，你会使用`//h1`。

**在Scrapy中，你可以选择使用CSS选择器或XPath来提取数据。Scrapy为两者提供了良好的支持，你可以根据个人偏好和特定任务的需求来选择使用哪一种。** ❤️❤️❤️<br>

一些开发者更喜欢CSS选择器因为它们更简洁，而另一些可能会选择XPath因为它的功能更强大。在实际使用中，你甚至可以在同一个项目中同时使用CSS选择器和XPath。<br>


## 动态网页爬取:

### 问题描述:

我想要爬取的界面随着下拉进度条才会加载剩下的部分，这种情况下可以使用scrapy进行爬取吗？<br>

### 解决方案:

在处理需要滚动页面才能加载内容的网站时，Scrapy 本身并不支持 JavaScript 渲染或与页面交互，如滚动条操作。这是因为 Scrapy 是一个快速高级的爬虫框架，用于抓取网站并从页面中提取数据，但它不支持 JavaScript。<br>

但是，你可以使用如下方法来解决这个问题：<br>

1. **Selenium**: 使用 Selenium，一个用于自动化网页浏览器操作的工具，你可以模拟真实用户的行为，包括滚动页面。然后，你可以将页面的源代码传递给 Scrapy 以提取所需数据。

2. **Splash**: Splash 是一个与 Scrapy 配合良好的 JavaScript 渲染服务，它允许执行 JavaScript 脚本，从而可以模拟页面滚动等操作。

3. **分析AJAX请求**: 有些网站在滚动到页面底部时会发送一个AJAX请求来加载更多数据。你可以通过检查网络请求来找出这个请求，并直接用 Scrapy 发送这些请求来获取数据。

每种方法都有其优缺点，选择哪一种取决于具体的网站结构和你的具体需求。通常，分析 AJAX 请求是最快且效率最高的方法，但它需要你能够理解和模拟浏览器发出的网络请求。Selenium 和 Splash 则提供了一种更直观、更灵活的方式来处理 JavaScript，但可能会慢一些，并且需要更多的资源。<br>

## 爬取鼠标悬停才能显示的内容:

### 问题描述:

我要爬取的网页内容是鼠标悬停在那个位置才会显示其中的内容，不是点击，点击就跳转界面了，这种情况下也能使用scrapy进行爬取吗？<br>

### 解决方案:

当内容只在鼠标悬停时显示，并且点击会导致页面跳转，使用Scrapy单独进行爬取可能会有一些限制。Scrapy是一个非常强大的爬虫框架，主要用于提取HTML和XML中的数据。然而，它本身不处理JavaScript生成的内容，这意味着如果网页内容是在鼠标悬停事件之后由JavaScript动态生成的，Scrapy可能无法直接捕获这些内容。<br>

但是，有几种方法可以处理这种情况：<br>

1. **分析AJAX请求**：有时，悬停事件会触发一个AJAX请求，该请求从服务器获取要显示的数据。你可以使用浏览器的开发者工具来监视网络请求，并找出对应的AJAX请求。一旦找到，你可以直接用Scrapy模拟这些请求来获取数据。

2. **集成Selenium**：Selenium是一个自动化工具，可以模拟真实用户的行为，包括鼠标悬停。你可以将Selenium与Scrapy结合使用，Selenium用来处理用户交互和JavaScript渲染，而Scrapy用来处理数据提取。

3. **使用Splash**：Splash是一个与Scrapy兼容的JavaScript渲染服务。它可以处理JavaScript，并提供了一个HTTP API来控制浏览器的行为，比如模拟鼠标悬停。你可以将Splash作为一个中间件集成到你的Scrapy项目中。

每种方法都有其优缺点，你可能需要根据具体的网站结构和需求来选择最合适的方法。在处理复杂的JavaScript交互时，通常需要一定的试错过程。<br>