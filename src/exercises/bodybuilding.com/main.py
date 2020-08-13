# Param Kapur, Parth Sharma

import requests
from bs4 import BeautifulSoup
import pprint
from pandas import DataFrame

r = ''
with open('a.html', 'r') as f:
    r += f.read()

soup = BeautifulSoup(r, 'html.parser')
exercise_divs = soup.findAll('div', {'class': 'ExResult-row'})


data = []
for d in exercise_divs:
    ex = {'name': d.h3.a.text.strip(),
          'target': d.find('div', {'class': 'ExResult-details ExResult-muscleTargeted'}).a.text.strip(),
          'equipment': d.find('div', {'class': 'ExResult-details ExResult-equipmentType'}).a.text.strip(),
          'rating': d.find('div', {'class': 'ExRating-badge'}).text.strip(),
          'img': d.img['data-src']}
    data.append(ex)

names = [ex['name'] for ex in data]
targets = [ex['target'] for ex in data]
equipments = [ex['equipment'] for ex in data]
ratings = [ex['rating'] for ex in data]
images = [ex['img'] for ex in data]

final_data = {'names': names, 'target': targets, 'equipment': equipments, 'rating': ratings, 'images': images}

df = DataFrame(final_data)
print(df)

df.to_excel('body_building_with_images.xlsx', sheet_name='data', index=False)
