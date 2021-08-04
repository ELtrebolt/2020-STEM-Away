from requests import get        
import time                 
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import codecs

topics = []         # scrape all of these from the main pages that contain 30 topics each

views = []
replies = []

postlinks = []      # make a list of each link for the 30 topics
count = 0

upvotes = []        # scrape all of these by accessing each topic link individually
categories = []
tags = []
contents = []
comments = []

# Debug flag. Set to true for print statements to the console
DEBUG = True

url = 'https://discuss.codecademy.com/c/get-help/c-plus-plus/1843'
# test https://discuss.codecademy.com/c/faq/general-coding-FAQ/1800 for 51 topics
# test https://discuss.codecademy.com/c/get-help/c-plus-plus/1843 for 144 topics

DRIVER_PATH = '/Users/leefa_1yhwpme/Desktop/chromedriver/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(url)

SCROLL_PAUSE_TIME = .5

def scroll():

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll()

# write html in a separate document
with codecs.open('Selenium Scraping - html.html', 'w', encoding= 'utf-8') as file:
    file.write(driver.page_source)
with codecs.open('Selenium Scraping - html.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')   # soup object for the main page

topic_containers = soup.find_all('tr', class_ = 'topic-list-item')  # topic containers that each have their own 'title', 'views', and 'replies' elements

for container in topic_containers:  # scrape topics, views, and replies for all 30 topics shown
    topic = container.find('a', class_ = 'title raw-link raw-topic-link').text
    topics.append(topic)

    view = container.find('td', class_=['num views','num views heatmap-high','num views heatmap-med','num views heatmap-low'])
    views.append(view.span.text)

    reply = soup.find('td', class_=['num posts-map posts heatmap-','num posts-map posts heatmap-high','num posts-map posts heatmap-med','num posts-map posts heatmap-low'])
    replies.append(reply.a.span.text)

    base = 'https://discuss.codecademy.com'
    b = container.find('span', class_ = 'link-top-line')
    for a in b.find_all('a', href=True):     # find all links
        postlinks.append(base+a['href'])
        break
          
for link in postlinks:      # repeat for each of the 30 links
    pagey = get(link)
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

import pandas as pd 

df = pd.DataFrame({'Topic': topics,
'Views': views,
'Replies': replies,
'Upvotes': upvotes,
'Categories': categories,
'Tags': tags,
'Content': contents,
'Comments': comments
})

df.to_csv('Selenium Scraping - output.csv', encoding='utf-8-sig', index=False)
print(df)

driver.close()