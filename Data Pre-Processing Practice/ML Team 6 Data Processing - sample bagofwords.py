# Takes 30 secs to run - exports all LESS DATA topics and their cleaned bag of words from the Stack Overflow forum

import pandas as pd
import numpy as np
import re
import nltk

from rake_nltk import Rake
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

# create a dataframe based off of the csv file
df = pd.read_csv('ML Team 6 Data Processing - sample data.csv', encoding='utf-8')

# 4 categories - topics, content, category, tag (list)
titles = []
contents = []
categories = []
tags = []

bagofwords = []
length = len(df['Topics'])

r = Rake()

# extract keywords from the Title of the Topic and add to a list
for index, row in df.iterrows():
    r.extract_keywords_from_text(str(row['Topics']))
    key_words_dict_scores = r.get_word_degrees()
    titleword = []
    titleword = list(key_words_dict_scores.keys())
    titlewordy = ''
    for a in range(0, len(titleword)):
        titlewordy = titlewordy + titleword[a] + ' '
    titles.append(re.sub(r"[^a-zA-Z]+", ' ', titlewordy))

# extract keywords from the Content of the Topic and add to a list
for index, row in df.iterrows():
    if(str(row['Content']).lower().replace(' ', '') == 'nan'):
        contents.append('')
    else:
        r.extract_keywords_from_text(str(row['Content']))
        key_words_dict_scores = r.get_word_degrees()
        contentword = []
        contentword = list(key_words_dict_scores.keys())
        contentwordy = ''
        for a in range(0, len(contentword)):
            contentwordy = contentwordy + contentword[a] + ' '
        contents.append(re.sub(r"[^a-zA-Z]+", ' ', contentwordy))

for i in range (0, length):
    category = df['Category']
    strcategory = str(category[i]).lower().replace(',',' ').replace(';',' ')
    if(strcategory[len(strcategory)-1] == ' '):
        categories.append(strcategory)
    else:
        categories.append(strcategory + ' ')

    tag = df['Tag']
    tagy = str(tag[i]).replace('[','').replace(',','').replace(']','').replace('\'','')
    tags.append(tagy + ' ')

for i in range (0, length):
    words = str(categories[i]) + str(tags[i]) + str(titles[i]) + str(contents[i])
    wordy = list(words.split(' '))
    bagofwords.append(str(wordy).replace('[','').replace(',','').replace(']','').replace('\'',''))

df2 = pd.DataFrame({'Topic': df['Topics'],
'Bag of Words': bagofwords,
'Category': categories,
'Tags': tags
})

print('Topics + String Bag of Words:')
print(df2.head())

# Tokenization
tokenizer = RegexpTokenizer(r'\w+')
df2['Bag of Words'] = df2['Bag of Words'].apply(lambda x: tokenizer.tokenize(x.lower()))

print('Tokenized Bag of Words:')
print(df2['Bag of Words'].head())

# Functions
lemmatizer = WordNetLemmatizer()
def word_lemmatizer(text):
    lem_text = ' '.join([lemmatizer.lemmatize(i) for i in text])
    return lem_text

stemmer = PorterStemmer()
def word_stemmer(text):
    stem_text = ' '.join([stemmer.stem(i) for i in text])
    return stem_text

df2['Bag of Words'] = df2['Bag of Words'].apply(lambda x: word_lemmatizer(x))

print('Lemmatized Bag of Words:')
print(df2['Bag of Words'].head())

for i in range (0, length):
    words = df2['Bag of Words'][i]
    wordy = list(words.split(' '))
    freq_dist = nltk.FreqDist(wordy)
    df2['Bag of Words'][i] = str(list(freq_dist.keys())).replace('[','').replace(',','').replace(']','').replace('\'','')

print('Lemmatized Bag of Words Combined Duplicates:')
print(df2['Bag of Words'].head())

df2.to_csv('ML Team 6 Data Processing - sample bagofwords.csv', encoding='utf-8-sig', index=False)