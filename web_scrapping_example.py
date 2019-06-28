from urllib.request import urlopen
from bs4 import BeautifulSoup

quote_page = 'http://www.kinofilms.ua/afisha/ukr_premieres/?month=05&year=2019'

page = urlopen(quote_page)

soup = BeautifulSoup(page, 'html.parser')

name_box = soup.findAll('a', attrs={'class': 'o'})
for film in name_box:
    print(film.text.strip())
