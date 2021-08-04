from requests import get
url = "http://editorial.rottentomatoes.com/guide/best-comedy-shows-of-all-time/4/"
response = get(url)

from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
show_containers = html_soup.find_all('div', class_ = 'row countdown-item')

names = []
years = []
ranks = []

for container in show_containers:
    name = container.h2.a.text
    names.append(name)

    year = container.h2.span.text
    years.append(year)

num = 1
for number in range(1, 51):
    ranks.append(num)
    num = num + 1

import pandas as pd 
test_df = pd.DataFrame({'TV Show': reversed(names),
'Year': reversed(years),
'Rank': ranks
})

print(test_df.info())
print(test_df)