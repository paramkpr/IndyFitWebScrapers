from itertools import islice
import requests
import json
from bs4 import BeautifulSoup
from pandas import DataFrame
from pprint import pprint



def get_metadata_from_recipe_page(soup):
    main_ingredients, region, course = [i.find('span', {'class': 'clrblack'}).text for i in soup.findAll('h4', {'class': 'clrlightgray'})]

    r = {'veg_nonveg' : soup.find('a', {'class': 'vegicon'}).img['src'].split('Images/')[-1].split('-')[0],
        'main_ingredients': main_ingredients,
        'region': region,
        'course': course}

    return r

def get_data_from_print_page(soup):
    def get_ingredients(soup):
        li = soup.find('div', {'class': 'ingrdntdiv'}).ul
        list_items = li.findAll('li')
        x = []
        for i in list_items:
            x.append(i.text.strip())
        return x


    r = {'title': soup.find('h3', {'id': 'headingh1'}).text.split('- SK')[0].strip(),
        'description': soup.find('div', {'class': 'shortdisc', 'itemprop': 'description'}).text.strip(),
        'prep_time': soup.find('meta', {'itemprop': 'prepTime'}).parent.text.split(':')[-1].strip(),
        'cook_time': soup.find('meta', {'itemprop': 'cookTime'}).parent.text.split(':')[-1].strip(),
        'servings': soup.find('span', {'itemprop': 'recipeYield'}).text,
        'ingredients': get_ingredients(soup),
        'method': [i.text.strip() for i in soup.findAll('span', {'itemprop': 'recipeInstructions'})],
        }

    return r

count = 0

with open('data.json', 'w+') as out:
    with open('links.txt', 'r') as f:
        for link in islice(f, 2086, None):
            print('getting66 r ' + link + '   number:  ' + str(count))

            r = {}
            link = link[:-1]
            html = requests.get(link).content
            soup = BeautifulSoup(html, 'html.parser')
            name = soup.find('div', {'class': 'htmlbread hidden-xs'}).findAll('a')[-1].text
            print_page_url = 'https://www.sanjeevkapoor.com/recipe/printrecipe.aspx?recipe_name=' + requests.utils.quote(name, safe='')
            print_page_soup = BeautifulSoup(requests.get(print_page_url).content, 'html.parser')
            try:
                r.update(get_data_from_print_page(print_page_soup))
                r.update(get_metadata_from_recipe_page(soup))
            except:
                pass
            out.write(json.dumps(r) + ',' + '\n')
            count += 1
