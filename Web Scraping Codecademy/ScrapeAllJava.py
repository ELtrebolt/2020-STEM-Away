# Takes 11 minutes to run - should get 1723 total results from the GetHelp-Java page 
# 57 pages x 30 topics per page + 13 topics on the last page = 1723 total

# Web Scraping imports
from requests import get        
import time                 
from bs4 import BeautifulSoup

# Data imports
import pandas as pd 

topics = []         # scrape all of these from the main pages that contain 30 topics each
views = []
replies = []

upvotes = []        # scrape all of these by accessing each topic link individually
categories = []
tags = []
contents = []
comments = []

for i in range(0,58):   # repeat for pages 0 to 57
    url = 'https://discuss.codecademy.com/c/get-help/java/1816?page='+str(i)   
    page = get(url) # request the page
    soup = BeautifulSoup(page.content, 'html.parser')   # soup object for the main page
    topic_containers = soup.find_all('tr', class_ = 'topic-list-item')  # topic containers that each have their own 'title', 'views', and 'replies' elements

    for container in topic_containers:  # scrape topics, views, and replies for all 30 topics shown
        topic = container.find('a', class_ = 'title raw-link raw-topic-link').text
        topics.append(topic)

        view = container.find('span', class_ = 'views').text
        views.append(view)

        reply = container.find('span', class_ = 'posts').text # Noticed that this number includes all posts on the page
        replies.append(int(reply)-1)     # Number of replies is equal to total - 1 (1 from original post)

    postlinks = []      # make a list of each link for the 30 topics

    for a in soup.find_all('a', href=True):     # find all links
        if 'https://discuss.codecademy.com/t/' in (a['href']):  # if the link is to the same forum
            postlinks.append(a['href'])
            
    for link in postlinks:      # repeat for each of the 30 links
        pagey = get(link)       # request the page
        soupy = BeautifulSoup(pagey.content, 'html.parser')     # soup object for the topic page

        upvote = soupy.find('span', class_='post-likes')
        if upvote is not None:      # if there is text to be found in the upvote element
            text = upvote.text
            upvotes.append(text)
            '''if len(text) == 6 or len(text) == 7:  # ex: '1 Like' or '2 Likes'
                upvotes.append(text[0:1])
            elif len(text) == 8:                  # ex: '10 Likes'
                upvotes.append(text[0:2])'''
        else:                       # mark 0 if the post doesn't show any 
            upvotes.append('0 Likes')

        category_containers = soupy.find_all('span', class_ = 'category-name') # scrape categories
        categorylist = ''
        for container in category_containers:
            categorylist = categorylist + container.text + ' '
        categories.append(categorylist)

        tag_containers = soupy.find_all('a', class_ = 'discourse-tag') # scrape tags
        if not tag_containers:      # if the list is empty
            tags.append('none')
        else:
            taglist = ''
            for container in tag_containers:
                taglist = taglist + container.text + ' '
            tags.append(taglist)
        
        content_containers = soupy.find_all('div', class_ = 'post') # scrape content 
        contentlist = []
        for container in content_containers:
            allcontent = container.find_all('p')
            content = ''
            for item in allcontent:
                content += item.text
            contentlist.append(content)
        if not contentlist:         # if the list is empty
            contents.append('none')
            comments.append('none')
        else:
            contents.append(contentlist[0])
            contentlist.pop(0)
            comment = ''
            for item in contentlist:
                comment = comment + item + ' '
            comments.append(comment) 

    time.sleep(4)        # prevent error for too many requests

df = pd.DataFrame({'Topic': topics,
'Views': views,
'Replies': replies,
'Upvotes': upvotes,
'Categories': categories,
'Tags': tags,
'Content': contents,
'Comments': comments
})

# df.to_csv('JavaScraping.csv', index=False)
# print(df)