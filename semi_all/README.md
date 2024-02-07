## semi

本项目仅用于测试爬虫基础使用。<br>

```txt
https://semi.cas.cn/
```

我使用的mac，我访问`https://semi.cas.cn/xwdt/zhxw/`，开发者模式复制 outerHTML 的结果如下：

```html
<td class="fw_t"><a href="./202401/t20240126_6972307.html">			中国科学院党组第四巡视组向半导体研究所反馈巡视情况<br></a></td>
```


请讲一下Scrapy中，`response.urljoin(relative_url)`的使用方法。

scrapy中如何执行页面跳转？跳转后的界面如何接着我当前界面的操作进行下一步爬取。


我使用的scrapy，我想爬取`https://semi.cas.cn/`网页下所有内容，如果有跳转链接就进行跳转，然后再进行爬取，直到爬取所有。跳转后的网页大概分3种情况，我如何针对这3种情况分别处理呢？请给出示例代码。




我在开发者工具的元素选项中，复制到的outer HTML如下，我该如何在另一个网页中搜索是否有以下字段呢？比如我在对比另外两个网页的时候就是用 ctrl f 然后查找是否有 `div.content` 检索的。

```html
<span><a href="../../../" title="首页" class="w12l20 CurrChnlCls">首页</a>&nbsp;&gt;&nbsp;<a href="../../" title="所情概况" class="w12l20 CurrChnlCls">所情概况</a>&nbsp;&gt;&nbsp;<a href="../" title="学位委员会" class="w12l20 CurrChnlCls">学位委员会</a></span>
```

我看到有人在谷歌浏览器用开发者工具输入 `div.Position span a` 语句定位到了以下内容，`div.Position span a` 是什么语句？书写规则是什么？

```html
<div class="Position"><span><a href="../../../" title="首页" class="w12l20 CurrChnlCls">首页</a>&nbsp;&gt;&nbsp;<a href="../../" title="新闻动态" class="w12l20 CurrChnlCls">新闻动态</a>&nbsp;&gt;&nbsp;<a href="../" title="综合新闻" class="w12l20 CurrChnlCls">综合新闻</a></span></div>
```


`div.Position span a` 是一个CSS选择器，用于在HTML文档中定位和选择具有特定结构的元素。这个语句的书写规则遵循CSS选择器的标准语法，下面是它的组成部分解析：

1. **`div.Position`**：这个部分选择所有具有`class="Position"`的`<div>`元素。`.`在CSS中表示类选择器，用于选择具有特定类名的元素。

2. **`span`**：紧随其后的`span`表示选择`div.Position`内部的所有`<span>`元素。由于没有指定类或ID，它将选择所有`span`元素。

3. **`a`**：最后的`a`表示选择所有在`span`元素内部的`<a>`（锚点）元素。

总的来说，`div.Position span a`选择的是所有位于`class="Position"`的`<div>`元素内部，且这些`<div>`元素内部还包含`<span>`元素，而这些`<span>`元素又包含`<a>`元素的所有`<a>`元素。

这种选择器非常有用于定位具有特定结构的HTML元素，常用于CSS样式应用、JavaScript操作等场合。在你提供的HTML片段中，此选择器将定位到三个`<a>`元素，它们分别指向“首页”、“新闻动态”和“综合新闻”。

CSS选择器什么时候用 `.`？什么时候用空格啊？还有没有其他语法，例如 `/`