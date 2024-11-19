import requests
import pandas as pd

from lxml import html
from pprint import pprint
from bs4 import BeautifulSoup

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

url = 'https://news.mail.ru/'
session = requests.session()
response = session.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
news_top = soup.find_all('a', {'class': 'photo__inner'})


all_news_top = list()
for nws in news_top[:5]:
    all_news_top.append(nws.get('href'))

dom = html.fromstring(response.text)

links = dom.xpath("//a[@class='list__text']/@href")
for i in range(1, 7):
    all_news_top.append(links[i])

# pprint(all_news_top)

news_list = list()
for news in all_news_top:
    news_info = dict()
    url_1 = news
    response_1 = requests.get(url_1, headers=headers)
    dom_1 = html.fromstring(response_1.text)

    try:
        name = dom_1.xpath("//h1[@data-qa='Title']/text()")
    except:
        name = None
    try:
        title = dom_1.xpath("//div[contains(@class,'c6d5585012')]/p/text()")
    except:
        title = None
    try:
        source = dom_1.xpath("//a[@class='dfe7838f95 f5ff795bf1 ce3581ad10']/text()")[0]
    except:
        source = None
    try:
        url_source = dom_1.xpath("//a[@class='dfe7838f95 f5ff795bf1 ce3581ad10']/text()/../@href")[0]
    except:
        url_source = None
    try:
        tag_news = dom_1.xpath("//a[@class='c0b0b8dab3']/text()")[1]
    except:
        tag_news = None

    try:
        news_info['name'] = name
    except:
        news_info['name'] = None
    try:
        news_info['title'] = title
    except:
        news_info['title'] = None
    try:
        news_info['source'] = source
    except:
        news_info['source'] = None
    try:
        news_info['url_source'] = url_source
    except:
        news_info['url_source'] = None
    try:
        news_info['tag_news'] = tag_news
    except:
        news_info['tag_news'] = None



    news_list.append(news_info)

df = pd.DataFrame(news_list)
df.to_csv('mail_news.csv', index=False)

