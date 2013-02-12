minicrawler
===========

简介
====

minicrawler 是友盟基于 scrapy 开发的一套应用市场采集系统，能够及时得到我们想要的数据 。
现在系统支持的应用市场 360zhushou Hiapk waptw iTunes Anzhi AndroidMarket AppChina 。
爬虫种类包含三种 IndexSpider / ContentSpider / UpdateSpider / CommemtSpider 。

IndexSpider:
采集市场主页，获取市场的整体数据信息。其数据可以用于市场的对比，矫正采集数据的全面性和性能。

ContentSpider:
采集应用的具体页面，填充应用的基本信息，每个新发现应用抓取一次即可。

UpdateSpider:
遍历市场的的列表页面，增加应用的下载数、评分等。

CommentSpider:
评论爬虫，更新App的评论信息。

ApkSpider:
下载App安装包，并进行数据分析，同时进行数据回填。

以上采集程序通过umspider统一调度执行，爬虫通过数据库进行调度。

================================================================================

安装
sudo apt-get install python requests scrapy mongodb pymongo

运行
sudo umspider
可以直接使用scrapy的命令工具
