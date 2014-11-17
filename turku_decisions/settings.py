# Scrapy settings for turku_decisions project

SPIDER_MODULES = ['turku_decisions.spiders']
NEWSPIDER_MODULE = 'turku_decisions.spiders'
DEFAULT_ITEM_CLASS = 'turku_decisions.items.Website'

ITEM_PIPELINES = {'turku_decisions.pipelines.FilterWordsPipeline': 1}
