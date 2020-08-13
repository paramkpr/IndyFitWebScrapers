from bs4 import BeautifulSoup
import requests
from pprint import pprint
from pandas import DataFrame

url = 'http://www.myhomepersonaltrainer.com/exercises/Exercise-Database.htm'
html = requests.get(url).content
soup = BeautifulSoup(html, 'html.parser')    

rows = soup.findAll('td', {'class': 'black12Text'})[1].findAll('td')


d = {}
for row in rows:
    try:
        if row['class'][0] == 'black14BoldCaption':
            print(row)
            d[row.text.strip()] = []
            current_key = row.text.strip()
    except KeyError:
        try:
            d[current_key].append(('http://www.myhomepersonaltrainer.com/exercises/' + row.a['href'],
             row.a.text.strip()))
        except:
            print(row)

pprint(d)


def get_exercise_details(link, target, name):
    html = requests.get(link).content
    soup = BeautifulSoup(html)
    try:
        imgs = [i['src'] for i in soup.find('div', {'id': 'maintext'}).findAll('img')]
    except:
        imgs = ['no_img', 'no_img']
    if imgs == []:
        imgs = ['no_img', 'no_img']
    print('imgs: ', imgs)
    try:
        description = soup.find('div',
         {'id': 'maintext'}).findAll(
             'td', {'class': 'black12Caption'})[1].text.strip().split('\n')[0].strip()
    except:
        description = 'no description'
    ex = {
        'image_1': imgs[0],
        'image_2': imgs[1],
        'description': description,
        'name': name,
        'target': target
    }
    return ex

exercises = []

for muscle, exs in d.items():
    for ex in exs:
        print('getting ex', ex[1])
        exercises.append(get_exercise_details(ex[0], muscle, ex[1]))

pprint(exercises)
print('Total: ', len(exercises))

names = [ex['name'] for ex in exercises]
targets = [ex['target'] for ex in exercises]
descriptions = [ex['description'] for ex in exercises]
image_ones = [ex['image_1'] for ex in exercises]
image_twos = [ex['image_2'] for ex in exercises]

final_data = {'names': names, 'target': targets,
              'description': descriptions, 'image_1': image_ones,
              'image_2': image_twos}

df = DataFrame(final_data)

df.to_excel('my_home_personal_trainer1.xlsx', sheet_name='data', index=True)
