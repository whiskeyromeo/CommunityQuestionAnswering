
# import scrapy 
# ###Working with the qatarliving.com site...

# #gets the string in string form --> use extract() to get 
# # a list if it turns out there are more than one p
# # columns within the div
# post = response.css("div.b-post-detail--el-text p::text").extract_first()
# questionUser = response.css("div.b-post-detail--el-info a::text").extract_first()
# #Select the div containing all of the comments


# userDict = {
# 	"username": response.css("div.b-post-detail--el-info a::text").extract_first(),
# 	"question": response.css("div.b-post-detail--el-text p::text").extract_first()
# }
# comments= response.css("div.b-comments-list--el-comment")
# if(len(comments) > 0):
# 	commentList = []
# 	commentIds = response.css("div.b-comments-list a::attr(id)").extract()
# 	for x in range(0, len(comments)):
# 		commentDict = {
# 			"commentId": commentIds[x],
# 			"username": comments[x].css("div.b-comments-list--el-info a::text").extract_first(),
# 			"comment": comments[x].css("div.b-comments-list--el-text p::text").extract_first()
# 		}
# 		commentList.append(commentDict)
# 	userDict["comments"] = commentList

# #######################
# # work on the lists on each page 
# #########

# #for http://www.qatarliving.com/forum/advice-help?page=# <--where # is the page number
# posts = response.css("div.b-topic-post--el-post")
# # pull the links for each post on the page so the crawler can hit each one
# for post in posts:
# 	title = post.css("a.b-topic-post--el-title::attr(href)").extract_first()
# 	if(title != None):
# 		print(title)

# # pull out the links on the pagination feature 
# pages = response.css("div.b-pagination a.b-pagination--el-page::attr(href)").extract()
# # pull the max number out of the last page


