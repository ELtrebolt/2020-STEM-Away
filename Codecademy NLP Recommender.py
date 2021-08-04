# Takes 1 minute to run - is a full recommender system for all of the Codecademy data
# Based off of the Movies NLP Recommender, tutorial by James Ng (Black Raven) from TowardsDataScience

from rake_nltk import Rake
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import re

# contains data about posts from online forum
df = pd.read_csv('Codecademy NLP Recommender - data.csv', encoding='utf-8')

# Store keywords separately first
titles = []
contents = []
comments = []
categories = []
tags = []

# Will store everything into 1 column
bagofwords = []
length = len(df['Title'])

# Perform data cleaning to remove links and keep only keywords
for i in range(0, length):
    contentwords = str(df['Post'][i]).split()
    for word in contentwords:
        if('http' in word or '.png' in word or '.jpeg' in word or '.jpg' in word or '.com' in word):
            contentwords.remove(word)
    contentwordo = ''
    for word in contentwords:
        contentwordo += word + ' '
    df['Post'][i] = contentwordo

    commentwords = str(df['Comments'][i]).split()
    for word in commentwords:
        if('http' in word or '.png' in word or '.jpeg' in word or '.jpg' in word or '.com' in word):
            commentwords.remove(word)
    commentwordo = ''
    for word in commentwords:
        commentwordo += word + ' '
    df['Comments'][i] = commentwordo

# used to extract keywords for each forum post
r = Rake()

# Extract keywords from title of forum post
for index, row in df.iterrows():
    r.extract_keywords_from_text(str(row['Title']))
    key_words_dict_scores = r.get_word_degrees()
    titleword = []
    titleword = list(key_words_dict_scores.keys())
    titlewordy = ''
    for a in range(0, len(titleword)):
        titlewordy = titlewordy + titleword[a] + ' '
    titles.append(re.sub(r"[^a-zA-Z]+", ' ', titlewordy))

# Extract keywords from content of forum post
for index, row in df.iterrows():
    if(str(row['Post']).lower().replace(' ', '') == 'nan'):
        contents.append('')
    else:
        r.extract_keywords_from_text(str(row['Post']))
        key_words_dict_scores = r.get_word_degrees()
        contentword = []
        contentword = list(key_words_dict_scores.keys())
        contentwordy = ''
        for a in range(0, len(contentword)):
            contentwordy = contentwordy + contentword[a] + ' '
        contents.append(re.sub(r"[^a-zA-Z]+", ' ', contentwordy))

# Extract keywords from comments of forum post
for index, row in df.iterrows():
    if(str(row['Comments']).lower().replace(' ', '') == 'nan'):
        comments.append('')
    else:
        r.extract_keywords_from_text(str(row['Comments']))
        key_words_dict_scores = r.get_word_degrees()
        commentword = list(key_words_dict_scores.keys())
        commentwordy = ''
        for a in range(0, len(commentword)):
            commentwordy = commentwordy + commentword[a] + ' '
        comments.append(re.sub(r"[^a-zA-Z]+", ' ', commentwordy))

# Extract keywords from categories & tags of forum post
for i in range (0, length):
    category = df['Categories']
    strcategory = str(category[i]).lower().replace(',',' ').replace(';',' ')
    if(strcategory[len(strcategory)-1] == ' '):
        categories.append(strcategory)
    else:
        categories.append(strcategory + ' ')

    tag = df['Tags']
    tagy = str(tag[i]).lower().replace(',',' ')
    if(tagy == 'nan'):
        tags.append('')
    elif(tagy[len(tagy)-1] == ' '):
        tags.append(tagy)
    else:
        tags.append(tagy + ' ')

# Create dataframe with post title and its Bag of Words
for i in range (0, length):
    words = str(categories[i]) + str(tags[i]) + str(titles[i]) + str(contents[i] + str(comments[i]))
    wordy = ''
    for x in range(0, len(words)):
        wordy += words[x]
    bagofwords.append(wordy)

df2 = pd.DataFrame({'Topic': df['Title'],
                    'Bag of Words': bagofwords
                    })

# Create a frequency count of each unique keyword in Bag of Words
count = CountVectorizer()
count_matrix = count.fit_transform(df2['Bag of Words'])

# Computes similarity between all posts' Bag of Words
cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices = pd.Series(df2['Topic'])

# Return posts with the highest cosine scores to a query
def recommend(title, cosine_sim = cosine_sim):
    recommended_topics = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indices = list(score_series.iloc[1:11].index)    
    
    for i in top_10_indices:
        recommended_topics.append(list(df2['Topic'])[i])
        
    print(recommended_topics)

recommend('SQL code please help')
# bagofwords: get help sql code please help lesson still showing error trying exactly right section

# df2.to_csv('Codecademy NLP Recommender - bagofwords.csv', encoding='utf-8-sig', index=False)