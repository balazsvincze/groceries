import requests
from bs4 import BeautifulSoup

def tesco():
    r = requests.get('https://bevasarlas.tesco.hu/groceries/HU.hu.plp.sitemap.xml')
    soup = BeautifulSoup(r.content,'html.parser')
    print(soup.get_text())

def auchan():
    # https://online.auchan.hu/sitemap.xml
    r = requests.get('https://online.auchan.hu/shop/elektronika/tv-audio-szorakozas')
    soup = BeautifulSoup(r.content, 'html.parser')

    tal = soup.find_all("div",{'class':'col-md-3 col-sm-4 col-xs-6'})
    for t in tal:
        asd = t.find('a')
        print(asd['href'].split('/')[4])