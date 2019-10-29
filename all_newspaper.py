from newspaper import Article


url = 'http://politics.people.com.cn/n1/2019/0515/c1024-31084899.html'
news = Article(url, language='zh')

news .download()  #先下载
news .parse()    #再解析

print(news.text) #新闻正文
print(news.title) #新闻标题
# print(news.html)   #未修改的原始HTML
print(news.authors)  #新闻作者
# print(news.top_image) #本文的“最佳图像”的URL
# print(news.movies)  #本文电影url
print(news.keywords) #新闻关键词
print(news.summary)   #从文章主体txt中生成的摘要
# print(news.images) #本文中的所有图像url