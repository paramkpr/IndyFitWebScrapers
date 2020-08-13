import requests
from bs4 import BeautifulSoup, Comment
from pandas import DataFrame
from pprint import pprint

def get_data_from_row(row):
    imgs = row.findAll('img')
    paras = row.findAll('td')[2].findAll('p')
    ex = {'image_1': 'https://www.jefit.com/' + imgs[0]['src'][3:],
          'image_2': 'https://www.jefit.com/' + imgs[1]['src'][3:],
          'name': row.h4.text.strip(),
          'equipment': paras[2].text.split(':')[-1].strip(),
          'target': paras[0].text.split(':')[-1].strip(),
          'type': paras[1].text.split(':')[-1].strip(),
          'difficulty': str(row.findAll(text=lambda text:isinstance(text, Comment))[0]).split(':')[-1][:-4].strip()
          }
    return ex


exercise_rows = []

for page in range(1, 131): 
    url = f"https://www.jefit.com/exercises/bodypart.php?id=11&exercises=All&All=0&Bands=0&Bench=0&Dumbbell=0&EZBar=0&Kettlebell=0&MachineStrength=0&MachineCardio=0&Barbell=0&BodyOnly=0&ExerciseBall=0&FoamRoll=0&PullBar=0&WeightPlate=0&Other=0&Strength=0&Stretching=0&Powerlifting=0&OlympicWeightLifting=0&Beginner=0&Intermediate=0&Expert=0&page=" + str(page)
    html= requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'hor-minimalist_3'}).table
    for row in table.findAll('tr'):
        exercise_rows.append(row)
    print('got data from page number', page)

print('\n\n Total number of exercises is,', len(exercise_rows), '\n\n')

exercises = []

c = 0
for ex_row in exercise_rows:
    c += 1
    exercises.append(get_data_from_row(ex_row))
    print('processed data for exercise ', c)


names = [ex['name'] for ex in exercises]
targets = [ex['target'] for ex in exercises]
equipments = [ex['equipment'] for ex in exercises]
difficulties = [ex['difficulty'] for ex in exercises]
types = [ex['type'] for ex in exercises]
image_ones = [ex['image_1'] for ex in exercises]
image_twos = [ex['image_2'] for ex in exercises]

final_data = {'names': names,
              'target': targets,
              'type': types,
              'equipment': equipments,
              'difficulty': difficulties,
              'image_1': image_ones,
              'image_2': image_twos
            }

df = DataFrame(final_data)
print(df)

df.to_excel('jefit1.xlsx', sheet_name='data', index=True)

