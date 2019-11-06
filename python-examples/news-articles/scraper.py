from selenium import webdriver
import requests
import dataset
from json import loads

db = dataset.connect('sqlite:///news.db')

base_url = 'https://news.google.com/news/'

# You can also use a query to start from like:
# https://news.google.com/search?q=paribas&hl=en-US&gl=US&ceid=US%3Aen
start_url = base_url + '?ned=us&hl=en'
script_url = 'http://www.webscrapingfordatascience.com/readability/Readability.js'

get_article_cmd = requests.get(script_url).text
get_article_cmd += '''

var documentClone = document.cloneNode(true);
var loc = document.location;
var uri = {
  spec: loc.href,
  host: loc.host,
  prePath: loc.protocol + "//" + loc.host,
  scheme: loc.protocol.substr(0, loc.protocol.indexOf(":")),
  pathBase: loc.protocol + "//" + loc.host + 
            loc.pathname.substr(0, loc.pathname.lastIndexOf("/") + 1)
};
var article = new Readability(uri, documentClone).parse();
return JSON.stringify(article);
'''

driver = webdriver.Chrome()
driver.implicitly_wait(10) 

driver.get(start_url)

news_urls = []
for link in driver.find_elements_by_css_selector('main a'):
    news_url = link.get_attribute('href')
    if news_url:
        news_urls.append(news_url)

for news_url in news_urls:
    print('Now scraping:', news_url)
    driver.get(news_url)

    print('Injecting script')
    returned_result = driver.execute_script(get_article_cmd)

    # Convert JSON string to Python dictionary
    article = loads(returned_result)
    if not article:
        # Failed to extract article, just continue
        continue

    # Retrieve the final, non-Google URL
    news_url = driver.current_url
    # Add in the url
    article['url'] = news_url
    # Remove 'uri' as this is a dictionary on its own
    del article['uri']
    # Add to the database
    db['articles'].upsert(article, ['url'])

    print('Title was:', article['title'])
    
driver.quit() 