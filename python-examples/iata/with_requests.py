import requests
from bs4 import BeautifulSoup
import pandas

url = 'https://www.iata.org/publications/Pages/code-search.aspx'

def get_form_data(html_soup, airline_name):
    data = {}
    for inp in html_soup.find_all(['input', 'select']):
        name = inp.get('name')
        value = inp.get('value')
        if not name:
            continue
        if name.endswith('ddlImLookingFor'):
            value = 'ByAirlineName'
        elif name.endswith('txtSearchCriteria'):
            value = airline_name
        data[name] = value if value else ''
    return data

def get_results(airline_name):
    session = requests.Session()
    # Spoof the user agent as a precaution
    session.headers.update({
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        })
    
    r = session.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    form = html_soup.find(id='aspnetForm')
    data = get_form_data(form, airline_name)

    r = session.post(url, data=data)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    
    table = html_soup.find('table', class_='datatable')
    df = pandas.read_html(str(table))
    return df

df = get_results('Lufthansa')
print(df)