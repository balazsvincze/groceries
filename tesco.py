import pandas
import requests
from bs4 import BeautifulSoup
# from tabulate import tabulate

def get_url_content(url):
    r = requests.get(url)
    return r.content


def get_items(soup):
    unordered_list = soup.find('ul',{'class':'product-list grid'})
    product = unordered_list.find_all('li',{'class':'product-list--list-item'})

    df = pandas.DataFrame(columns=['Name','Price1','Price2','Measurement'])

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
        
        df = df.append({'Name':[name],'Price1':[price_per_unit],'Price2':[price_per_weight],'Measurement':[measurement]}, ignore_index=True)
        # print(name, price_per_unit, price_per_weight, measurement)
    print(df)


def get_table_contents(soup):
    table = soup.find_all('table')
    for i in range(len(table)):
        df = pandas.read_html(str(table[i]))
        print(df)

    # print(table)
    # print(len(table))
    # print(type(table))

    # df = pandas.read_html(str(table))
    # print(df)
    
    # Create a list
    # destination = df["Hová"].tolist()
    # print(destination)

    # Print as an ascii table
    # print(tabulate(df[0], headers='keys', tablefmt='psql'))


def main():
    url = "https://bevasarlas.tesco.hu/groceries/hu-HU/shop/zoldseg-gyumolcs/gyumolcsok/deligyumolcsok"

    soup = BeautifulSoup(get_url_content(url),'html.parser')

    get_items(soup)

if __name__ == "__main__":
    main()