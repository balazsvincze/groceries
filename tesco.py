import pandas
import requests
import logging
from bs4 import BeautifulSoup


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
    
    return df


def scrape_tesco():
    base_url = "https://bevasarlas.tesco.hu/groceries/hu-HU/shop/"
    temp_list = ['zoldseg-gyumolcs/all','hus-hal-felvagott/all','alapveto-elelmiszerek/all','fagyasztott-elelmiszerek/all','italok/all','alkohol/all']
    df = pandas.DataFrame(columns=['Name','Price1','Price2','Measurement','Category','Store'])

    for link_end in temp_list:
        page_number = 1
        empty_pagination_button = ""

        if page_number == 1:
            link = f'{base_url}{link_end}?page={page_number}'
            print(link)
            soup = BeautifulSoup(get_url_content(link),'html.parser')
            data = get_items(soup)
            page_number += 1
            df = df.append(data)

        while (page_number != 1 and not empty_pagination_button):
            link = f'{base_url}{link_end}?page={page_number}'
            print(link)
            soup = BeautifulSoup(get_url_content(link),'html.parser')
            empty_pagination_button = soup.find('a',{'class':'pagination--button prev-next disabled'})
            data = get_items(soup)
            page_number += 1
            df = df.append(data)
    
    df = df.reset_index(drop=True)
    print(df)