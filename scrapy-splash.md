# Scrapy & JavaScript integration through Splash
- [Scrapy \& JavaScript integration through Splash](#scrapy--javascript-integration-through-splash)
  - [Installation:](#installation)
  - [Configuration:](#configuration)
  - [Usage:](#usage)
    - [Requests:](#requests)
      - [`meta['splash']['args']` contains arguments sent to Splash. scrapy-splash adds some default keys/values to args:](#metasplashargs-contains-arguments-sent-to-splash-scrapy-splash-adds-some-default-keysvalues-to-args)

通过Splash实现Scrapy与JavaScript的集成。<br>

This library provides [Scrapy](https://github.com/scrapy/scrapy) and JavaScript integration using [Splash](https://github.com/scrapinghub/splash). The license is BSD 3-clause.<br>

这个库使用Splash实现了Scrapy和JavaScript的集成。许可证是BSD 3-clause。<br>


## Installation:

Install scrapy-splash using pip:<br>

```bash
pip install scrapy-splash
```

Scrapy-Splash uses Splash HTTP API, so you also need a Splash instance. Usually to install & run Splash, something like this is enough:<br>

Scrapy-Splash使用Splash HTTP API，因此您还需要一个Splash实例。通常安装并运行Splash，像这样就足够了:<br>

```bash
docker run -p 8050:8050 scrapinghub/splash
```

终端将显示如下信息:<br>

> 下载内容会自动 Pull ...

```log
(langchain) root@iZ2zea5v77oawjy2qz7c20Z:/data/chat_system# docker run -p 8050:8050 scrapinghub/splash
Unable to find image 'scrapinghub/splash:latest' locally
latest: Pulling from scrapinghub/splash
7595c8c21622: Pulling fs layer 
d13af8ca898f: Pulling fs layer 
70799171ddba: Pulling fs layer 
b6c12202c5ef: Pulling fs layer 
60a588d4f36e: Pulling fs layer 
74efcc44bb0a: Pull complete 
630a03095961: Pull complete 
6ece3b427ef5: Pull complete 
a1fce8353093: Pull complete 
3933ca5f4768: Pull complete 
b0097a197686: Pull complete 
eb38ff0231d8: Pull complete 
3d065f0b97ea: Pull complete 
bce087e2552e: Pull complete 
86c96f1d4ecd: Pull complete 
3c421ffe4e4a: Pull complete 
3c667b2546ea: Pull complete 
765d9dad919d: Pull complete 
f20aa104f0ea: Pull complete 
bc2ee8c11554: Pull complete 
185117d6d955: Pull complete 
a40af7862b2f: Pull complete 
38a6d08ed185: Pull complete 
a36db9d4a71b: Pull complete 
adaa646ebfe9: Pull complete 
6ae21b55ecfd: Pull complete 
8ef8d76a1942: Pull complete 
Digest: sha256:b4173a88a9d11c424a4df4c8a41ce67ff6a6a3205bd093808966c12e0b06dacf
Status: Downloaded newer image for scrapinghub/splash:latest
2024-03-22 02:52:34+0000 [-] Log opened.
2024-03-22 02:52:34.943605 [-] Xvfb is started: ['Xvfb', ':1500143512', '-screen', '0', '1024x768x24', '-nolisten', 'tcp']
QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-splash'
2024-03-22 02:52:35.020444 [-] Splash version: 3.5
2024-03-22 02:52:35.058897 [-] Qt 5.14.1, PyQt 5.14.2, WebKit 602.1, Chromium 77.0.3865.129, sip 4.19.22, Twisted 19.7.0, Lua 5.2
2024-03-22 02:52:35.059113 [-] Python 3.6.9 (default, Jul 17 2020, 12:50:27) [GCC 8.4.0]
2024-03-22 02:52:35.059233 [-] Open files limit: 1048576
2024-03-22 02:52:35.059296 [-] Can't bump open files limit
2024-03-22 02:52:35.075799 [-] proxy profiles support is enabled, proxy profiles path: /etc/splash/proxy-profiles
2024-03-22 02:52:35.075955 [-] memory cache: enabled, private mode: enabled, js cross-domain access: disabled
2024-03-22 02:52:35.202764 [-] verbosity=1, slots=20, argument_cache_max_entries=500, max-timeout=90.0
2024-03-22 02:52:35.203049 [-] Web UI: enabled, Lua: enabled (sandbox: enabled), Webkit: enabled, Chromium: enabled
2024-03-22 02:52:35.203470 [-] Site starting on 8050
2024-03-22 02:52:35.203554 [-] Starting factory <twisted.web.server.Site object at 0x7fbe640f45c0>
2024-03-22 02:52:35.203825 [-] Server listening on http://0.0.0.0:8050
```


Check [Splash](https://splash.readthedocs.io/en/latest/install.html) install docs for more info.<br>

查看Splash安装文档了解更多信息。<br>


## Configuration:

1. Add the Splash server address to `settings.py` of your Scrapy project like this:

像这样在您的Scrapy项目的`settings.py`中添加Splash服务器地址:<br>

```conf
SPLASH_URL = 'http://192.168.59.103:8050'
```

你的写法也可以是:<br>

```conf
SPLASH_URL = 'http://localhost:8050'
```

2. Enable the Splash middleware by adding it to `DOWNLOADER_MIDDLEWARES` in your `settings.py` file and changing **HttpCompressionMiddleware** priority:

通过在您的 `settings.py` 文件中将其添加到 `DOWNLOADER_MIDDLEWARES` 并更改 **HttpCompressionMiddleware** 优先级来启用Splash中间件:<br>

```conf
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
```

Order 723 is just before HttpProxyMiddleware (750) in default scrapy settings.<br>

在默认的scrapy设置中，723的顺序就在HttpProxyMiddleware（750）之前。<br>

HttpCompressionMiddleware priority should be changed in order to allow advanced response processing; see [scrapy/scrapy#1895](https://github.com/scrapy/scrapy/issues/1895) for details.<br>

需要更改HttpCompressionMiddleware的优先级，以允许高级响应处理；详见scrapy/scrapy#1895。<br>

3. Enable `SplashDeduplicateArgsMiddleware` by adding it to `SPIDER_MIDDLEWARES` in your `settings.py`:

通过在 `settings.py` 中将其添加到 `SPIDER_MIDDLEWARES` 来启用 `SplashDeduplicateArgsMiddleware`:<br>

```conf
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
```

This middleware is needed to support `cache_args` feature; it allows to save disk space by not storing duplicate Splash arguments multiple times in a disk request queue. <br>

这个中间件是支持 `cache_args` 特性所必需的；它允许通过不在磁盘请求队列中多次存储重复的Splash参数来节省磁盘空间。<br>

If Splash 2.1+ is used the middleware also allows to save network traffic by not sending these duplicate arguments to Splash server multiple times.<br>

如果使用Splash 2.1+，中间件还允许通过不多次将这些重复参数发送到Splash服务器来节省网络流量。<br>

4. Set a custom `DUPEFILTER_CLASS`:

设置一个自定义的 `DUPEFILTER_CLASS` :<br>

```conf
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
```

5. If you use Scrapy HTTP cache then a custom cache storage backend is required. scrapy-splash provides a subclass of `scrapy.contrib.httpcache.FilesystemCacheStorage`:

如果您使用Scrapy HTTP缓存，则需要一个自定义的缓存存储后端。scrapy-splash提供了scrapy.contrib.httpcache.FilesystemCacheStorage的一个子类:<br>

```conf
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```

If you use other cache storage then it is necesary to subclass it and replace all `scrapy.util.request.request_fingerprint` calls with `scrapy_splash.splash_request_fingerprint`.<br>

如果您使用其他缓存存储，则需要对其进行子类化，并用 `scrapy_splash.splash_request_fingerprint` 替换所有的 `scrapy.util.request.request_fingerprint` 调用。<br>

‼️ **Note** :<br>

Steps (4) and (5) are necessary because Scrapy doesn't provide a way to override request fingerprints calculation algorithm globally; this could change in future.<br>

步骤（4）和（5）是必需的，因为Scrapy没有提供一种方法来全局覆盖请求指纹计算算法；这在将来可能会改变。<br>

There are also some additional options available. Put them into your `settings.py` if you want to change the defaults:<br>

还有一些额外的选项可用。如果您想改变默认设置，请将它们放入您的 `settings.py` 中：<br>

```conf
SPLASH_COOKIES_DEBUG = False  # 默认为False。设为True启用SplashCookiesMiddleware中的调试cookies。这个选项类似于内置的scarpy cookies中间件的COOKIES_DEBUG：它记录所有请求的发送和接收的cookies。
SPLASH_LOG_400 = True  # 默认为True - 它指示记录所有来自Splash的400错误。它们很重要，因为它们显示了执行Splash脚本时发生的错误。设置为False以禁用此日志记录。
SPLASH_SLOT_POLICY = scrapy_splash.SlotPolicy.PER_DOMAIN  # 默认为scrapy_splash.SlotPolicy.PER_DOMAIN（作为对象，而不仅仅是字符串）。它指定了如何为Splash请求维护并发和礼貌性，以及为SplashRequest的slot_policy参数指定默认值，下面将进行描述。
```


## Usage:

### Requests:

The easiest way to render requests with Splash is to use `scrapy_splash.SplashRequest`:<br>

使用Splash渲染请求的最简单方法是使用 `scrapy_splash.SplashRequest` ：<br>

```python
yield SplashRequest(url, self.parse_result,
    args={
        # optional; parameters passed to Splash HTTP API
        'wait': 0.5,

        # 'url' is prefilled from request url
        # 'http_method' is set to 'POST' for POST requests
        # 'body' is set to request body for POST requests
    },
    endpoint='render.json', # optional; default is render.html
    splash_url='<url>',     # optional; overrides SPLASH_URL
    slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
)
```

Alternatively, you can use regular scrapy.Request and `'splash'` Request meta key:<br>

或者，您可以使用常规的scrapy.Request和 `'splash'` 请求元键：<br>

```python
yield scrapy.Request(url, self.parse_result, meta={
    'splash': {
        'args': {
            # set rendering arguments here(在这里设置渲染参数)
            'html': 1,
            'png': 1,

            # 'url' is prefilled from request url('url' 会从请求的url中预填)
            # 'http_method' is set to 'POST' for POST requests(对于POST请求，'http_method' 设置为 'POST')
            # 'body' is set to request.body for POST requests(对于POST请求，'body'设置为request.body)
        },

        # optional parameters(可选参数)
        'endpoint': 'render.json',  # optional; default is render.json(可选；默认为 render.json)
        'splash_url': '<url>',      # optional; overrides SPLASH_URL(可选；覆盖SPLASH_URL)
        'slot_policy': scrapy_splash.SlotPolicy.PER_DOMAIN,
        'splash_headers': {},       # optional; a dict with headers sent to Splash(可选；发送给Splash的头部字典)
        'dont_process_response': True, # optional, default is False(可选， 默认为 False)
        'dont_send_headers': True,  # optional, default is False(可选， 默认为 False)
        'magic_response': False,    # optional, default is True(可选， 默认为 True)
    }
})
```

Use `request.meta['splash']` API in middlewares or when scrapy.Request subclasses are used (there is also `SplashFormRequest` described below). <br>

在中间件中或使用scrapy.Request子类时使用 `request.meta['splash']` API（下文还将描述SplashFormRequest）。<br>

For example, `meta['splash']` allows to create a middleware which enables Splash for all outgoing requests by default.<br>

例如，`meta['splash']` 允许创建一个中间件，**默认情况下为所有外发请求启用Splash。🚀🚀🚀**<br>

`SplashRequest` is a convenient utility to fill `request.meta['splash']` ;<br>

`SplashRequest`是一个方便的工具，用于填充 `request.meta['splash']` ；<br>

it should be easier to use in most cases. For each `request.meta['splash']` key there is a corresponding `SplashRequest` keyword argument:<br>

在大多数情况下，它应该更容易使用。对于每个 `request.meta['splash']` 键，都有一个对应的 `SplashRequest` 关键字参数：<br>

for example, to set `meta['splash']['args']` use `SplashRequest(..., args=myargs)` .<br>

例如，设置 `meta['splash']['args']使用SplashRequest(..., args=myargs)` 。<br>

#### `meta['splash']['args']` contains arguments sent to Splash. scrapy-splash adds some default keys/values to args:

meta['splash']['args']包含发送到Splash的参数。scrapy-splash向args添加了一些默认的键/值：<br>

- 'url' is set to request.url('url'设置为request.url);

- 'http_method' is set to 'POST' for POST requests(对于POST请求，'http_method'设置为'POST');

- 'body' is set to request.body for POST requests(对于POST请求，'body'设置为request.body).

You can override default values by setting them explicitly.<br>

您可以通过明确设置来覆盖默认值。<br>

Note that by default Scrapy escapes URL fragments using AJAX escaping scheme. If you want to pass a URL with a fragment to Splash then set `url` in `args` dict manually. <br>

请注意，默认情况下Scrapy使用AJAX转义方案转义URL片段。如果您想将带有片段的URL传递给Splash，则需要手动在args字典中设置url。<br>

🚨🚨🚨This is handled automatically if you use `SplashRequest`, but you need to keep that in mind if you use raw `meta['splash']` API.<br>

🚨🚨🚨如果您使用 `SplashRequest` ，则会自动处理此操作，但如果您使用原始 `meta['splash']` API，则需要记住这一点。<br>




