from bs4 import BeautifulSoup
from urllib import request
novel_names = []
url = 'https://syosetu.com/'
res = request.urlopen(url)
soup = BeautifulSoup(res,'html.parser')
for i in range(10):
    novel = soup.find(class_ = 'p-ranking__item p-ranking__item--col2 p-ranking__item--' + str(i+1) + ' c-novel-item c-novel-item--ranking')
    url2 = novel.get('href')
    res2 = request.urlopen(url2)
    soup2 = BeautifulSoup(res2,'html.parser')
    title = soup2.find('title')
    novel_names.append(title.get_text())
    print('第' + str(i+1)+ '位:' + title.get_text())
