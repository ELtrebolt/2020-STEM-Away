# https://towardsdatascience.com/content-based-recommender-using-natural-language-processing-nlp-159d0925a649

from rake_nltk import Rake
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv('Movies NLP Recommender - data.csv', encoding= 'utf-8')

keywords = []
genres = []
actors = []
directors = []
bagofwords = []
length = len(df['Title'])

r = Rake()

for index, row in df.iterrows():
    r.extract_keywords_from_text(row['Plot'])
    key_words_dict_scores = r.get_word_degrees()
    keyword = []
    keyword = list(key_words_dict_scores.keys())
    keywords.append(keyword)

df['Genre'] = df['Genre'].map(lambda x: x.split(','))
df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])
df['Director'] = df['Director'].map(lambda x: x.split(','))

for index, row in df.iterrows():
    genres.append([x.lower().replace(' ','') for x in row['Genre']])
    actors.append([x.lower().replace(' ','') for x in row['Actors']])
    directors.append([x.lower().replace(' ','') for x in row['Director']])

for i in range (0, length):
    words = genres[i] + directors[i] + actors[i] + keywords[i]
    wordy = ''
    for x in range(0, len(words)):
        wordy += words[x] + ' '
    bagofwords.append(wordy)

df2 = pd.DataFrame({'Title': df['Title'],
'Bag_of_Words': bagofwords
})

count = CountVectorizer()
count_matrix = count.fit_transform(df2['Bag_of_Words'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices = pd.Series(df2['Title'])

def recommend(title, cosine_sim = cosine_sim):
    recommended_movies = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indices = list(score_series.iloc[1:11].index)
    
    for i in top_10_indices:
        recommended_movies.append(list(df2['Title'])[i])
        
    print(recommended_movies)

recommend('The Avengers')

# print (cosine_sim)
# df2.to_csv('Movies NLP Recommender - bagofwords.csv', encoding='utf-8-sig', index=False)