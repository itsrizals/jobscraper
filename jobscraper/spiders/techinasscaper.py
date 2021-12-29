import json
import scrapy 
from scrapy_playwright.page import PageCoroutine

class TechinasiaSpider(scrapy.Spider):
	name = 'techinasscaper'
	start_urls = ['www.techinasia.com']
	def start_requests(self):

		yield scrapy.http.Request('https://www.techinasia.com/jobs/search?country_name[]=Indonesia', meta=dict(
             playwright = True,
             playwright_include_page = True,
             playwright_page_coroutines = [
                 PageCoroutine('wait_for_selector', 'article.jsx-1022654950')
                 ]
         ))


	async def parse(self, response):
		for link in response.css('article.jsx-1022654950'):

			origin = 'https://www.techinasia.com/api/2.0'
			extracted_link = link.css('a[data-cy="job-title"]').attrib['href'].replace('jobs', 'job-postings')
			yield scrapy.http.Request(origin + extracted_link, callback=self.parse_final, dont_filter= 'TRUE')


	def parse_final(self, response):
		resp_json = json.loads(response.body)
		data = resp_json['data']
		yield from data