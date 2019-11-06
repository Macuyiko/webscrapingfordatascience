from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

session = requests.Session()

sp500 = 'https://de.reuters.com/finance/markets/index/.SPX'
officers = 'https://www.reuters.com/companies/{symbol}/people'

page = 1
regex = re.compile(r'\/finance\/stocks\/overview\/.*')
symbols = []

while True:
    print('Scraping page:', page)
    params = params={'sortBy': '', 'sortDir' :'', 'pn': page}
    html = session.get(sp500, params=params).text
    soup = BeautifulSoup(html, "html.parser")
    pagenav = soup.find(class_='pageNavigation')
    if not pagenav:
        break
    companies = pagenav.find_next('table', class_='dataTable')
    for link in companies.find_all('a', href=regex):
        symbols.append(link.get('href').split('/')[-1])
    page += 1

print(symbols)

dfs = []

for symbol in symbols:
    print('Scraping symbol:', symbol)
    html = session.get(officers.format(symbol=symbol)).text
    soup = BeautifulSoup(html, "html.parser")
    officer_table = soup.find('table', {"class" : "table-container"})
    try:
        df = pd.read_html(str(officer_table), header=0)[0]
    except ValueError:
        print("No tables found")
        continue
    df.insert(0, 'symbol', symbol)
    dfs.append(df)

# Store the results
df = pd.concat(dfs)
df.to_pickle('sp500.pkl')