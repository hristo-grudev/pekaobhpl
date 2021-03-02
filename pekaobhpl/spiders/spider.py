import scrapy

from scrapy.loader import ItemLoader
from ..items import PekaobhplItem
from itemloaders.processors import TakeFirst


class PekaobhplSpider(scrapy.Spider):
	name = 'pekaobhpl'
	start_urls = ['https://www.pekaobh.pl/aktualnosci.html']

	def parse(self, response):
		post_links = response.xpath('//div[@class="columns small-12 medium-12s large-8 xlarge-9"]')
		for post in post_links:
			url = post.xpath('.//div[@class="links-container"]/a/@href').get()
			date = post.xpath('.//div[@class="small-10 item-with-date-date"]/p/text()').get()
			title = post.xpath('.//h2[@class="item-with-date-header"]/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, date, title):
		description = response.xpath('//div[@class="columns small-12 medium-8 large-7 end text-left item-with-date-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=PekaobhplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
