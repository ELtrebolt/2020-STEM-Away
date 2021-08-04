# Imports
# Keyword Extraction
from rake_nltk import Rake

# Store Data
import pandas as pd
import numpy as np

# Regular Expression = Match Strings
import re

# Create dataframe from web-scraped csv
df = pd.read_csv('Codecademy Bag Of Words - sample data.csv', encoding='utf-8')

# Separate columns of data
contents = []
comments = []
categories = []
tags = []

# Will store all in one column
bagofwords = []

length = len(df['Topic'])
r = Rake()

# Add keywords from content of forum post
for index, row in df.iterrows():
    if(str(row['Content']) == 'none'):
        contents.append('')
    else:
        r.extract_keywords_from_text(row['Content'])
        key_words_dict_scores = r.get_word_degrees()
        contentword = []
        contentword = list(key_words_dict_scores.keys())
        contentwordy = ''
        for a in range(0, len(contentword)):
            contentwordy = contentwordy + contentword[a] + ' '
        contents.append(re.sub(r"[^a-zA-Z]+", ' ', contentwordy))

# Add keywords from comments of forum post
for index, row in df.iterrows():
    if(str(row['Comments']) == 'none'):
        comments.append('')
    else:
        r.extract_keywords_from_text(str(row['Comments']))
        key_words_dict_scores = r.get_word_degrees()
        commentword = list(key_words_dict_scores.keys())
        commentwordy = ''
        for a in range(0, len(commentword)):
            commentwordy = commentwordy + commentword[a] + ' '
        comments.append(re.sub(r"[^a-zA-Z]+", ' ', commentwordy))

# Add keywords from categories & tags of forum post
for i in range (0, length):
    category = df['Categories']
    str(category[i]).replace(' ','')
    str(category[i]).lower()
    if(str(category[i]) == 'nan'):
        categories.append('')
    else:
        categories.append(str(category[i]))

    tag = df['Tags']
    if(tag[i] == 'none'):
        tags.append('')
    else:
        tags.append(tag[i])

# Combine all keywords into one column
for i in range (0, length):
    words = str(categories[i]) + str(tags[i]) + str(contents[i] + str(comments[i]))
    wordy = ''
    for x in range(0, len(words)):
        wordy += words[x]
    bagofwords.append(wordy)

# Build and export dataframe
df2 = pd.DataFrame({'Topic': df['Topic'],
'Bag of Words': bagofwords
})
df2.to_csv('Codecademy Bag Of Words - output.csv', encoding='utf-8-sig', index=False)