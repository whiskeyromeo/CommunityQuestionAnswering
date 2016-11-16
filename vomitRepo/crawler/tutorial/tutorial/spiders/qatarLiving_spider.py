import scrapy
import json
from pprint import pprint
import re

class qatarLiving_spider(scrapy.Spider):
	name = "ql"
	start_urls = [
		'http://www.qatarliving.com/forum/advice-help'
	]
	page = 0
	postDict = {}
	# uncomment the two lines below in order to hit all of the pages in the section
	# NOTE: This may take a long time and potentially be looked at by an isp as being an attack
	# causing a temporary cessation of services
	#pages = response.css("div.b-pagination a.b-pagination--el-page::attr(href)").extract()
	#max_page = re.sub('[^0-9]','',pages[len(pages)-1])
	max_page = 10
	f = open('./questFile.json', 'w')
	new_f = open('./questFile2.json', 'w')

	def parseQuestions(self, response):
		question = response.css("div.b-post-detail--el-text p::text").extract()
		question = " ".join(question)
		userDict = {
			"username": response.css("div.b-post-detail--el-info a::text").extract_first(),
			"question": question
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
		postList = []
		for post in posts:
			#postList.append(scrapy.Request(post, self.parseQuestions))
			yield scrapy.Request(post, self.parseQuestions)
		#self.postDict[str(self.page)] = postList
		#TODO : Figure out how to write the questions so that the topic is either carried with
		# each individual question or there is a key with the topic for each set of questions from
		# from that field
		
		if(self.page <= self.max_page):
			href = '/forum/advice-help?page=' + str(self.page)
			self.page += 1
			next_page = response.urljoin(href)
			yield scrapy.Request(next_page, self.parse)
		