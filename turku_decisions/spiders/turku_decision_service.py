from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import Request
from urlparse import urljoin

from turku_decisions.items import *

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
            item = Meeting()
            item['title'] = site.xpath('a/text()').extract()
            item['url'] = urljoin(response.url, site.xpath('a/@href').extract()[0])

            yield Request(item['url'],
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
            if url:
                yield Request(urljoin(response.url, url[0]),
                              callback=self.parseItem,
#                              errback=lambda _: item,
#                              meta=dict(item=item),
                             )
            else:
                m_item = MeetingItem()
                m_item['ingress'] = item.xpath('td/a/text()').extract()
                m_item['title'] = item.xpath('td[not(@align="center")]').extract()
                yield m_item

    def parseItem(self, response):
        sel = Selector(response)

        m_item = MeetingItem()

        m_item['title'] = sel.xpath('//p[@class="ots"]/text()').extract()
        m_item['ingress'] = sel.xpath('//p[@class="ing"]').extract()
        m_item['content'] = sel.xpath('//div[@class="docxframe"]').extract()
        m_item['attachments'] = sel.xpath('//div[@class="XSDoc"]/p[@class="liiteoheis"]')
#        m_item['suggestion'] = sel.xpath('//p[contains(span[@class="ehdotuspaatos"])]')
        delivery = sel.xpath('//p[@class="jakelu"]')
        m_item['delivery'] = delivery

        print m_item

        return m_item
