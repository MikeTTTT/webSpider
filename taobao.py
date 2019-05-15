import scrapy
from scrapy.spiders import CrawlSpider

from selenium import webdriver
import re, requests


# 构建评论页表
def makeURL(itemId, sellerId, i):
    url = 'http://rate.tmall.com/list_detail_rate.htm?itemId=' \
          + itemId + '&sellerId=' + sellerId + '¤tPage=' + i
    return url


class taobaospider(CrawlSpider):
    name = "taobao"
    start_urls = [
        "https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=python%E4%B9%A6%E7%B1%8D&suggest=history_1&_input_charset=utf-8&wq=p&suggest_query=p&source=suggest&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=0"
    ]
    # 根据指定页数添加商品列表，设定值为20页
    for i in range(1, 2):
        url = "https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=python%E4%B9%A6%E7%B1%8D&suggest=history_1&_input_charset=utf-8&wq=p&suggest_query=p&source=suggest&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=" + str(
            i * 44)
        start_urls.append(url)

    def parse(self, response):

        # 需要通过selenium启动虚拟浏览器，如果使用其他浏览器需作出修改
        driver = webdriver.Chrome()

        driver.get(response.url)
        driver.implicitly_wait(30)
        driver.refresh()
        driver.implicitly_wait(30)

        html = driver.page_source
        driver.close()

        # 添加访问商品详细界面的url
        list = re.findall('href=\"//detail.tmall.com.*?\"', html)
        linkList = sorted(set(list), key=list.index)
        # 添加销量数据
        sales = re.findall('>[0-9]*人收货', html)
        i = 0
        for href in linkList:
            link = 'https:' + href.split('"')[1]
            sale = sales[i].replace('>', '').replace("人收货", "")
            i = i + 1
            yield scrapy.Request(url=link, meta={'sales': sale}, callback=self.parse_item)

    def parse_item(self, response):

        # 根据实际item名称修改此处
        item = GameItem()
        # 获取商品销量
        item['sales'] = response.meta['sales']
        # 从商品界面提取信息以构建评论界面的url
        try:
            str1 = re.findall('itemId:\".*?\"', response.text)[0]
            itemId = str1.split(' ')[1]
            str2 = re.findall('sellerId:\".*?\"', response.text)[0]
            sellerId = str2.split(' ')[1]
        except:
            return

        # 初始化评论列表
        comments = []
        comment_times = []
        # 爬取所需评论页数，设定值为爬取100页，如果没有评论则结束
        for i in range(1, 2):
            try:
                url_comment = makeURL(itemId, sellerId, str(i))
                page = requests.get(url_comment)
                page.status_code
                comment = re.findall('\"rateContent\":(\".*?\")', page.text)
                comment_time = re.findall('\"rateDate\":(\".*?\")', page.text)
                comments.extend(comment)
                comment_times.extend(comment_time)
            except:
                break
        # 输入评论
        item['comment'] = comments
        item['comment_time'] = comment_times

        # 获取商品其他信息，（以@为分割符）
        details = response.xpath('//ul[@id="J_AttrUL"]/li/text()').extract()
        details = "@".join(details)
        details = details + "@"
        # 输入item
        try:
            item['name'] = re.findall('书名:(.*?)@', details)[0].replace('书名:', '').replace("\xa0", "")
        except:
            pass
        try:
            item['ISBN'] = re.findall('ISBN编号:(.*?)@', details)[0].replace('ISBN编号:', '').replace("\xa0", "")
        except:
            pass
        try:
            item['writer'] = re.findall('作者:(.*?)@', details)[0].replace('作者:', '').replace("\xa0", "")
        except:
            pass
        try:
            item['price'] = re.findall('定价:(.*?)@', details)[0].replace('定价:', '').replace("\xa0", "")
        except:
            pass
        try:
            item['company'] = re.findall('出版社名称:(.*?)@', details)[0].replace('出版社名称:', '').replace("\xa0", "")
        except:
            pass

        yield item

