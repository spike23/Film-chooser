import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup


month = int(sys.argv[1])
year = int(sys.argv[2])

quote_page = 'http://www.kinofilms.ua/afisha/ukr_premieres/?month={month}&year={year}'.format(month=month, year=year)

page = urlopen(quote_page)

soup = BeautifulSoup(page, 'html.parser')

name_box = soup.findAll('a', attrs={'class': 'o'})

for film in name_box:
    print(film.text.strip())
    print('http://www.kinofilms.ua' + film.get('href'))
