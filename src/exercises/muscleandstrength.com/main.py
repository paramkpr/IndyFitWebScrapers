import requests
from bs4 import BeautifulSoup
from pprint import pprint
from pandas import DataFrame

type_urls = ['https://www.muscleandstrength.com/exercises/compound',
             'https://www.muscleandstrength.com/exercises/isolation']

headers = {
     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


exercises_urls = []

for url in type_urls:
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser')
    exercise_blocks = soup.findAll('div', {'class': 'exerciseBlocks'})
    for ex in exercise_blocks:
        exercises_urls.append('https://www.muscleandstrength.com/' + ex.h5.a['href'])
    
print(exercises_urls)

def clean_name(name):
    words = name.split(' ')
    words.remove('Video')
    words.remove('Guide')
    return ' '.join(words)

def clean_instructions(instructions):
    out = []
    for ins in instructions:
        out.append(ins.text.strip())
    return out

def get_data_from_exercise_page(url):
    html = requests.get(url,
                  headers=headers).content
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('h1', {'class': 'no-header'}).text.strip()
    details = [d.find('div', {'class': 'wrap'}).text.strip().split('\n')[-1].strip() \
            for d in soup.findAll('li', {'class': 'qg-half'})]
    instructions = [l.findAll('li') for l in soup.findAll('div', {'class': 'field-item even'})[:2]][-1]

    images = [img.a['href'] for img in soup.findAll('div', {'class': 'imgWrapper'})]
    if images == []:
        images = ['None', 'None']

    try:
        video = 'https:' + soup.find('video').source['src']
    except:
        video = 'None'
    print(details)


    ex = {'name': clean_name(name),
        'target': details[0],
        'exercise_type': details[1],
        'equipment': details[2],
        'mechanics': details[3],
        'force': details[4],
        'level': details[5],
        'secondary': soup.find('li', {'class': 'last'}).div.text.split('\n')[-1].strip(),
        'instructions': clean_instructions(instructions),
        'video': video,
        'image_1': images[0],
        'image_2': images[1]
        }
    return ex

exercises = []

for url in exercises_urls:
    ex = get_data_from_exercise_page(url)
    print('getting __________________')
    print(ex)
    exercises.append(ex)

print(exercises)
print('\n\n total', len(exercises), '\n\n')

names = [ex['name'] for ex in exercises]
targets = [ex['target'] for ex in exercises]
equipments = [ex['equipment'] for ex in exercises]
mechanics = [ex['mechanics'] for ex in exercises]
levels = [ex['level'] for ex in exercises]
types = [ex['exercise_type'] for ex in exercises]
forces = [ex['force'] for ex in exercises]
intrsuctions = [ex['instructions'] for ex in exercises]
videos = [ex['video'] for ex in exercises]
secondaries = [ex['secondary'] for ex in exercises]
image_ones = [ex['image_1'] for ex in exercises]
image_twos = [ex['image_2'] for ex in exercises]

final_data = {'names': names,
              'target': targets,
              'type': types,
              'equipment': equipments,
              'mechanics': mechanics,
              'video': videos,
              'force': forces,
              'level': levels,
              'instructions': intrsuctions,
              'secondary': secondaries,
              'image_1': image_ones,
              'image_2': image_twos
            }

df = DataFrame(final_data)
print(df)

df.to_excel('muscle_and_strength.xlsx', index=True, sheet_name='data')
