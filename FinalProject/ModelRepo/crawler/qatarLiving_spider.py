'''
	Need to install scrapy with conda in order to run
		conda install -c scrapinghub scrapy
	To run:
		scrapy runspider qatarLiving_spider.py

	NOTE = This is a partial implementation which will not run over all of the data from the site.
	The full crawler was reverted back to a previous version due to conflicts which emerged when
	trying to push the datasets to github. The full version has been lost and this version must be modified. 

	__author__= Will Russell


'''
import scrapy
import json
from pprint import pprint
import re

def getTopic(self, response):
	topic = response.request.url.split('/')
	topic = re.sub('\?page=[0-9]', '',topic[len(topic)-1])
	return topic

def createSeedDict(topics = []):
	seed = {}
	for topic in topics:
		seedDict = {
			'topic': topic,
			'url': 'http://www.qatarliving.com/forum/' + topic,
			'page': 0,
			'max_page': 5
		}
		seed[topic] = seedDict
	return seed

def seedStartUrls(seedDict):
	start_urls = []
	for k,v in seedDict.items():
		start_urls.append(v['url'])
	return start_urls

class qatarLiving_spider(scrapy.Spider):
	name = "ql"
	topics = ['advice-help', 'qatar-living-lounge','welcome-qatar','socialising','visas-permits','motoring', 'qatari-culture']
	seedDict = createSeedDict(topics)
	start_urls = seedStartUrls(seedDict)
	currentTopic = 'STARTER'

	f = open('./questFile.json', 'w')

	def parseQuestions(self, response):
		question = response.css("div.b-post-detail--el-text p::text").extract()
		question = " ".join(question)
		userDict = {
			"subject": response.css("div.b-post-header--el-title::text").extract_first(),
			"username": response.css("div.b-post-detail--el-info a::text").extract_first(),
			"question": question,
			"topic": self.currentTopic
		}
		comments= response.css("div.b-comments-list--el-comment")
		if(len(comments) > 0):
			commentList = []
			commentIds = response.css("div.b-comments-list a::attr(id)").extract()
			for x in range(0, len(comments)):
				comment = comments[x].css("div.b-comments-list--el-text p::text").extract()
				comment = " ".join(comment)
				commentDict = {
					"commentId": commentIds[x],
					"username": comments[x].css("div.b-comments-list--el-info a::text").extract_first(),
					"comment": comment
				}
				commentList.append(commentDict)
			userDict["comments"] = commentList
		if(userDict["question"] != None):
			json.dump(userDict, self.f)
			self.f.write('\n')
	

	def parse(self, response):
		posts = response.css("a.b-topic-post--el-title::attr(href)").extract() 
		for post in posts:
			yield scrapy.Request(post, self.parseQuestions)
		

		currentTopic = getTopic(self, response)
		self.currentTopic = currentTopic
		currentPage = self.seedDict[currentTopic]['page']
		currentMaxPage = self.seedDict[currentTopic]['max_page']
		if(currentMaxPage == 5):
			pages = response.css("div.b-pagination a.b-pagination--el-page::attr(href)").extract()
			max_page = re.sub('[^0-9]','',pages[len(pages)-1])
			#BEWARE!! --> uncommenting the following code will run through ALL of the pages on the site
			# for advice-help : max-page = 899
			# for qatar-living-lounge : max-page = 2487
			# !!!!!!!!!!!!!
			#self.seedDict[currentTopic]['max_page'] = max_page
		print('##########')
		print('topic : ' + currentTopic)
		print('url : ' + response.request.url)
		print('page: ' + str(currentPage))
		print('real max_page: ' + str(max_page))
		print('##########')

		if(currentPage <= currentMaxPage):
			href = '/forum/' + currentTopic + '?page=' + str(currentPage)
			self.seedDict[currentTopic]['page'] += 1
			next_page = response.urljoin(href)
			yield scrapy.Request(next_page, self.parse)
		