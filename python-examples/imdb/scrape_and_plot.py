import pickle
import requests
from bs4 import BeautifulSoup

url = 'http://www.imdb.com/title/tt0944947/epdate'

episodes = []
ratings = []

soup = BeautifulSoup(requests.get(url).text, 'html.parser')
table = soup.find(id='tn15content').find('table')
for row in table.find_all('tr'):
    cols = row.find_all('td')
    if not cols:
        continue
    episode = cols[0].get_text(strip=True)
    if episode == '#':
        # This is the header row
        continue
    rating = float(row.find(class_='rating-rating').find(class_='value').get_text(strip=True))
    episodes.append(episode)
    ratings.append(rating)

import matplotlib.pyplot as plt

episodes = ['S' + e.split('.')[0] if int(e.split('.')[1]) == 1 else '' for e in episodes]

plt.figure()
positions = [a*2 for a in range(len(ratings))]
plt.bar(positions, ratings, align='center')
plt.xticks(positions, episodes)
plt.show()