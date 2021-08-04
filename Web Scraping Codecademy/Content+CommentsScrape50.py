# Returns 50 topics from the Top of Get-Help-Java page in 30 seconds

# Web Scraping imports
from requests import get
from bs4 import BeautifulSoup

# Data import
import pandas as pd

# Columns to store data in
topics = []
views = []
replies = []

upvotes = []
categories = []
tags = []
contents = []
comments = []

url = 'https://discuss.codecademy.com/c/get-help/java/1816/l/top'
page = get(url)
soup = BeautifulSoup(page.content, 'html.parser')
topic_containers = soup.find_all('tr', class_ = 'topic-list-item')

# Iterate over topics on the first page
for container in topic_containers:
    topic = container.find('a', class_ = 'title raw-link raw-topic-link').text
    topics.append(topic)

    view = container.find('span', class_ = 'views').text
    views.append(view)

    reply = container.find('span', class_ = 'posts').text
    replies.append(reply)

postlinks = []

# Get a list of all of the links to those topics
for a in soup.find_all('a', href=True):
    if 'https://discuss.codecademy.com/t/' in (a['href']):
        postlinks.append(a['href'])
            
# Extract data from each of the links using html formatting
for link in postlinks:
    pagey = get(link)
    soupy = BeautifulSoup(pagey.content, 'html.parser')

    upvote = soupy.find('span', class_='post-likes')
    if upvote is not None:
        text = upvote.text
        upvotes.append(text)
    else:
        upvotes.append(0)

    category_containers = soupy.find_all('span', class_ = 'category-name')
    categorylist = ''
    for container in category_containers:
        categorylist = categorylist + container.text + ' '
    categories.append(categorylist)

    tag_containers = soupy.find_all('a', class_ = 'discourse-tag')
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

# Build dataframe
df = pd.DataFrame({'Topic': topics,
'Views': views,
'Replies': replies,
'Upvotes': upvotes,
'Categories': categories,
'Tags': tags,
'Content': contents,
'Comments': comments
})

df.to_csv('Code Academy export test.csv', index=False)
#print(df)