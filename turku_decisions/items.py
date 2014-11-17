from scrapy.item import Item, Field

class Meeting(Item):

    title = Field()
    url = Field()

class MeetingItem(Item):

    title = Field()
    ingress = Field()
    content = Field()
    suggestion = Field()
    attachments = Field()
    delivery = Field()
