from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import Request
from urlparse import urljoin

from turku_decisions.items import Website

class TurkuDecisionsSpider(Spider):
    name = "turku_decisions"
    allowed_domains = ["www05.turku.fi"]
    start_urls = [
#        "http://www05.turku.fi/ah/kh/2014/welcome.htm",
        "http://www05.turku.fi/ah/khkon/2014/welcome.htm",
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul/li')
        items = []

        base_url = response.url.rsplit('/', 1)[0]

        for site in sites:
            item = Website()
            item['name'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = ''

            yield Request(urljoin(response.url, item['url'][0]),
                          callback=self.parseMeeting,
#                          errback=lambda _: item,
#                          meta=dict(item=item),
                         )
            break

    def parseMeeting(self, response):
        sel = Selector(response)

        items = sel.xpath('//tr[@valign="top"]')
        print items

        for item in items:
            url = item.xpath('td/a/@href').extract()
            section = item.xpath('td/a/text()').extract()
            description = item.xpath('td[not(@align="center")]').extract()
            print url
            print section
            print description
            yield Request(urljoin(response.url, url[0]),
                          callback=self.parseItem,
#                          errback=lambda _: item,
#                          meta=dict(item=item),
                         )

    def parseItem(self, response):
        sel = Selector(response)

        title = sel.xpath('//p[@class="ots"]/text()').extract()
        ingress = sel.xpath('//p[@class="ing"]').extract()
        content = sel.xpath('//div[@class="docxframe"]').extract()
        attachments = sel.xpath('//div[@class="XSDoc"]/p[@class="liiteoheis"]')
#        suggestion = sel.xpath('//p[contains(span[@class="ehdotuspaatos"])]')

        print title
        print ingress
        print content
        print attachments
#        print suggestion
