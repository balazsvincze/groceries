import pandas
import requests
import logging
from bs4 import BeautifulSoup
# from tabulate import tabulate


def get_url_content(url):
    r = requests.get(url)
    return r.content


def get_items(soup):
    category = soup.find('h1',{'class':'heading query'})

    unordered_list = soup.find('ul',{'class':'product-list grid'})
    product = unordered_list.find_all('li',{'class':'product-list--list-item'})

    df = pandas.DataFrame(columns=['Name','Price1','Price2','Measurement','Category','Store'])

    for attr in product:
        #Get the name of the item
        name_link = attr.find("a",{'class':'product-tile--title product-tile--browsable'})
        if name_link:
            name = name_link.text

        #Get the prices of the item
        prices = attr.find_all("span",{'class':'value'})
        if prices:
            price_per_unit = prices[0].text
            price_per_weight = prices[1].text
       
       #Get the measurement
        measurement = attr.find('span',{'class':'weight'})
        if measurement:
            measurement = measurement.text
        
        df = df.append({'Name':[name],'Price1':[price_per_unit],'Price2':[price_per_weight],'Measurement':[measurement],'Category':[category.text],'Store':['Tesco']}, ignore_index=True)
        # print(name, price_per_unit, price_per_weight, measurement)
    
    return df

base_url = "https://bevasarlas.tesco.hu/groceries/hu-HU/shop/"
temp_list = ['hus-hal-felvagott/all', 'zoldseg-gyumolcs/all']
page_number = 1

for link_end in temp_list:
    link = f'{base_url}{link_end}?page={page_number}'
    print(link)
    soup = BeautifulSoup(get_url_content(link),'html.parser')
    empty_pagination_button = soup.find('a',{'class':'pagination--button prev-next disabled'})
    if page_number == 1:
        data = get_items(soup)
        page_number += 1
    elif page_number != 1 and not empty_pagination_button:
        data = get_items(soup)
        page_number += 1
    print (data)