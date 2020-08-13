from bs4 import BeautifulSoup
import requests
import json
from itertools import islice
from pandas import DataFrame

# with open('links.txt', 'w') as f:
#     for page in range(2, 188):
#         html = requests.get('https://www.tarladalal.com/recipes-for-indian-veg-recipes-2?pageindex=' + str(page)).content
#         soup = BeautifulSoup(html, 'html.parser')
#         for r in soup.findAll('article', {'class': 'rcc_recipecard'}):
#             link = ('https://www.tarladalal.com/' +
#                             r.find('span', {'class': 'rcc_recipename'}).a['href'] + '\n')
#             f.write(link)
#             print('writing link ', link)

def get_method():
    lists = soup.find('div',{'id': 'ctl00_cntrightpanel_pnlRcpMethod'}).findAll('ol')
    list_items = []
    for li in lists:
        for list_item in li.findAll('li'):
            list_items.append(list_item)
    out = []
    for i in list_items:
        try:
            out.append(i.span.text.strip())
        except:
            pass
    return out

#
# with open('links.txt', 'r') as f:
#     with open('r.json', 'w') as jsonfile:
#         count = 0
#         for link in f:
#             print('writing r', link.strip(), 'NUMBER:', count)
#             html = requests.get(link.strip()).content
#             soup = BeautifulSoup(html, 'html.parser')
#
#             try:
#                 nutrition_table_rows = soup.find('table', {'id': 'rcpnutrients'}).findAll('tr')
#             except:
#                 nutrition_table_rows = [BeautifulSoup('<td>None None</td>', 'html.parser') for _ in range(7)]
#             try:
#                 energy = nutrition_table_rows[0].findAll('td')[-1].text.split(' ')[0]
#             except:
#                 energy = 'None'
#
#             try:
#                 protein = nutrition_table_rows[1].findAll('td')[-1].text.split(' ')[0]
#             except:
#                 protein = 'None'
#             try:
#                 carbohydrates = nutrition_table_rows[2].findAll('td')[-1].text.split(' ')[0]
#             except:
#                 carbohydrates = 'None'
#             try:
#                 fiber = nutrition_table_rows[3].findAll('td')[-1].text.split(' ')[0]
#             except:
#                 fiber = 'None'
#             try:
#                 fat = nutrition_table_rows[4].findAll('td')[-1].text.split(' ')[0]
#             except:
#                 fat = 'None'
#             try:
#                 cholesterol = nutritin_table_rows[5].findAll('td')[-1].text.split(' ')[0]
#             except:
#                 cholesterol = 'None'
#             try:
#                 sodium = nutrition_table_rows[6].findAll('td')[-1].text.split(' ')[0]
#             except:
#                 sodium = 'None'
#
#             try:
#                 prep_time = soup.find('time', {'itemprop': 'prepTime'}).text.strip()
#             except:
#                 prep_time = 'None'
#
#             try:
#                 cook_time = soup.find('time', {'itemprop': 'cookTime'}).text.strip()
#             except:
#                 cook_time = 'None'
#
#             try:
#                 name = soup.find('span', {'itemprop': 'name',
#                                     'id': 'ctl00_cntrightpanel_lblRecipeName'}).text.strip()
#             except:
#                 name = 'None'
#             try:
#                 views = soup.find('span', {'id': 'ctl00_cntrightpanel_lblViewCount'}).text.split(' ')[-2].strip()
#             except:
#                 views = 'None'
#             try:
#                 descriptions = soup.find('span', {'id': 'ctl00_cntrightpanel_lblDesc'}).text.strip()
#             except:
#                 descriptions = 'None'
#             try:
#                 tags = [tag.text.strip() for tag in soup.find('div', {'class': 'tags'}).findAll('a')]
#             except:
#                 tags = []
#             try:
#                 ingredients = [(ing.span.text.strip(), ing.a.text.strip())
#                                 for ing in soup.find('div', {'id': 'rcpinglist'}).div.findAll('span', {'itemprop': 'recipeIngredient'})]
#             except:
#                 ingredients = 'None'
#
#             try:
#                 image = 'https://www.tarladalal.com/' + \
#                     soup.find('img', {'id': 'ctl00_cntrightpanel_imgRecipe',
#                                     'itemprop': 'image'})['src']
#             except:
#                 image = 'None'
#
#             r = {
#                 'name': name,
#                 'views': views,
#                 'image': image,
#                 'description': descriptions,
#                 'tags': tags,
#                 'preperation_time': prep_time,
#                 'cooking_time': cook_time,
#                 'serves': 5,
#                 'ingredients': ingredients,
#                 'method': get_method(),
#                 'energy': energy,
#                 'protein': protein,
#                 'carbohydrates': carbohydrates,
#                 'fiber': fiber,
#                 'fat': fat,
#                 'cholesterol': cholesterol,
#                 'sodium': sodium
#                 }
#             jsonfile.write(json.dumps(r) + ',' + '\n')
#             count += 1

name = []
view = []
image = []
descriptions = []
tags = []
prep_time = []
cook_time = []
serves = []
ingredients = []
method = []
energy = []
protein = []
carbohydrates = []
fiber = []
fat = []
cholesterol = []
sodium = []

with open('r.json', 'r') as recipie_file:
    data = json.load(recipie_file)
    for r in data:
        name.append(r['name'])
        view.append(r['views'])
        image.append(r['image'])
        descriptions.append(r['description'])
        tags.append(r['tags'])
        prep_time.append(r['preperation_time'])
        cook_time.append(r['cooking_time'])
        serves.append(r['serves'])
        ingredients.append(r['ingredients'])
        method.append(r['method'])
        energy.append(r['energy'])
        protein.append(r['protein'])
        carbohydrates.append(r['carbohydrates'])
        fiber.append(r['fiber'])
        fat.append(r['fat'])
        cholesterol.append(r['carbohydrates'])
        sodium.append(r['sodium'])

final_data = {
    'name': name,
    'view': view,
    'image': image,
    'descriptions': descriptions,
    'tags': tags,
    'prep_time': prep_time,
    'cook_time': cook_time,
    'serves': serves,
    'ingredients': ingredients,
    'method': method,
    'energy': energy,
    'protein': protein,
    'carbohydrates': carbohydrates,
    'fiber': fiber,
    'fat': fat,
    'cholesterol': cholesterol,
    'sodium': sodium
}

df = DataFrame(final_data)

print(df)

df.to_excel('tarla_dalal1.xlsx', index=True, sheet_name='data')
