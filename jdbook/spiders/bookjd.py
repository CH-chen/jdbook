# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json
import urllib
class BookjdSpider(scrapy.Spider):
    name = 'bookjd'
    allowed_domains = ['jd.com','p.3.cn']  #价格域名也要加进去
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        #第一种
        # dt_list = response.xpath("//div[@class='mc']/dl/dt")
        # dd_list = response.xpath("//div[@class='mc']/dl/dd")
        # # for dt in dt_list:
        # #     item = {}
        # #     item["fenlei"] = dt.xpath("./a/text()").extract_first()
        # #     print(item)
        # # for dd in dd_list:
        # #     em_list = dd.xpath("//em")
        # #     for em in em_list:
        # #         item = {}
        # #         item["fenlei"] = em.xpath("./a/text()").extract_first()
        # #         print(item)
        # for dt,dd in zip(dt_list,dd_list):
        #     item = {}
        #     item["dafenlei"] = dt.xpath("./a/text()").extract_first()
        #     em_list = dd.xpath("./em")
        #     for em in em_list:
        #
        #         item["fenlei"] = em.xpath("./a/text()").extract_first()
        #         print(item)
        #第二种
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            item["dafenlei"] = dt.xpath("./a/text()").extract_first()
            em_list = dt.xpath("./following-sibling::dd[1]/em")
            for em in em_list:

                item["fenlei"] = em.xpath("./a/text()").extract_first()
                #//list.jd.com/1713-3258-3297.html
                #https://list.jd.com/list.html?cat=1713,3258,3297&tid=3297
                item["href"] = em.xpath("./a/@href").extract_first()
                # num1 = item["href"].rsplit('/')[3].rsplit('.')[0].rsplit('-')[0]
                # num2 = item["href"].rsplit('/')[3].rsplit('.')[0].rsplit('-')[1]
                # num3 = item["href"].rsplit('/')[3].rsplit('.')[0].rsplit('-')[2]
                # item["href"] = "https://list.jd.com/list.html?cat={},{},{}&tid={}".format(num1,num2,num3,num3)
                if item["href"] is not None:
                    item["href"] = "https:" + item["href"]
                print(item)
                yield scrapy.Request(
                    item["href"],
                    callback=self.book_list,
                    meta = {"item":deepcopy(item)}

                )
    def book_list(self,response):
        item = response.meta["item"]
        li_list = response.xpath("//div[@id='plist']/ul/li")
        for li in li_list:
            item["book_title"] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()
            item["book_img"] = li.xpath(".//div[@class='p-img']/a/img/@src").extract_first()
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='p-img']/a/img/@data-lazy-img").extract_first()
            item["book_img"] = "https:"+ item["book_img"] if item["book_img"] is not None else None
            item["book_href"] = li.xpath(".//div[@class='p-name']/a/@href").extract_first()
            item["book_publish"] = li.xpath(".//span[@class='p-bi-store']/a/text()").extract_first()
            item["book_sku"] = li.xpath("./div/@data-sku").extract_first()
            print(item)
            #多个书籍价格的URL
            #https://p.3.cn/prices/mgets?callback=jQuery5548003&ext=11101000&pin=&type=1&area=1_72_4137_0&skuIds=J_11757834
            # %2CJ_12090377%2CJ_10616501%2CJ_12192773%2CJ_12155241%2CJ_11716978%2CJ_12174897%2CJ_10367073%2CJ_11711801
            # %2CJ_10960247%2CJ_10019917%2CJ_11711801%2CJ_10199768%2CJ_11711801%2CJ_12174895%2CJ_12173835%2CJ_12350509
            # %2CJ_12052646%2CJ_12479361%2CJ_12160627%2CJ_12406846%2CJ_10162899%2CJ_12449755%2CJ_11888857%2CJ_11982184
            # %2CJ_12271618%2CJ_12184621%2CJ_12041776%2CJ_12174923%2CJ_11982172
            # &pdbp=0&pdtk=&pdpin=&pduid=15498906230231700222016&source=list_pc_front&_=1549895670335  #多余的可以去去掉
            yield scrapy.Request(
                "https://p.3.cn/prices/mgets?skuIds=J_{}".format(item["book_sku"]),  #拼接单个书籍的价格
                callback=self.pare_book_price,
                meta={"item":deepcopy(item)}

            )
        next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url,next_url)
            yield scrapy.Request(
                next_url,
                callback=self.book_list,
                meta = {"item":item}
            )

    def pare_book_price(self,response):
        item = response.meta["item"]
        item["book_price"] = json.loads(response.body.decode())[0]["op"]


