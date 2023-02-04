import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import re
import os
import time
current_dir = os.getcwd()
def get_area():
    area_urls = []
    area_names = []
    top_url = 'https://tabelog.com/'
    r = requests.get(top_url)
    soup = BeautifulSoup(r.content,'html.parser')
    prefecture = soup.find_all(class_="rsttop-area-search__target js-area-swicher-target")
    for i in prefecture:
        are_url = i.get('data-swicher-city').replace('{','').replace('}','').replace('[','').replace(']','').split(',')[3].replace('cityName','').replace(':','',1).replace('"','').replace('url','')
        area_name = i.get('data-swicher-city').replace('{','').replace('}','').replace('[','').replace(']','').split(',')[0].replace('cityName','').replace(':','',1).replace('"','').replace('url','')
        area_urls.append(are_url)
        area_names.append(area_name)
    area_urls = area_urls[6:]
    area_names = area_names[6:]
    time.sleep(1)
    return area_names,area_urls
    #-8,-12,-14,-20,-21
    # k = prefecture[3]
    # #prefecture[0] = 東京 prefecture[3] = 大阪

    # # print(k)
    # # p = r'\>(.*)\</a>'
    # # # p = r'>.*?</a>'  # アスタリスクに囲まれている任意の文字
    # # pre_name = re.findall(p,str(k))
    # # print(pre_name[0])
    # # print()
    # list2 = []
    # chimei_list = []
    # url_list = []
    # list_ = k.get('data-swicher-popular-area-list').split('},')#その都道府県の地域を取る
    # for i in list_:
    #     list2.append(i.replace('{','').replace('}','').replace('[','').replace(']','').split(','))#整形
    # for i in list2:
    #     chimei_list.append(i[0].replace('areaName','').replace(':','',1).replace('"',''))#地域名のみ
    #     url_list.append(i[1].replace('url','').replace(':','',1).replace('"',''))#URLのみ
    # print(chimei_list)
    # print(url_list)
    # return url_list[-1]

def get_detail_area(prefecture,url,f):
    r = requests.get(url)
    urls=[]
    names=[]
    soup = BeautifulSoup(r.content,'html.parser')
    more = soup.find_all(class_ ="list-sidebar__recommend")
    areas = more[1]
    areas1 = areas.find_all(class_ ="list-sidebar__recommend-item")
    areas = areas1
    for i in areas:
        p = i.find('a')
        url_ = p.get('href')
        name = i.get_text()
        urls.append(url_)
        names.append(name.replace(' ','').replace('\n',''))
        time.sleep(1)
    for url1 in urls:
        get_restaurant(url1,prefecture,f)

def get_restaurant(url,prefecture,f):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    # type_and_abst = soup.find_all(class_="list-rst__rst-name-wrap")
    # for i in type_and_abst:
    #     print(i.get_text())
    a = soup.find(class_="navi-rstlst__label navi-rstlst__label--review")
    new_url =a.get('href')
    r = requests.get(new_url)
    soup = BeautifulSoup(r.content,'html.parser')
    if prefecture == '東京' or prefecture == '大阪':
        for cnt in range(5):
            type_list = []
            restaurant_list = []
            url_list = []
            type_ = soup.find_all(class_ = 'list-rst__area-genre cpy-area-genre')#和食とか洋食とか
            abst = soup.find_all(class_="list-rst__rst-name-target cpy-rst-name")#その店のURLを取りたい
            for i in type_:
                type_list.append(i.get_text().replace(' ',''))
            for i in abst:
                restaurant_list.append(i.get_text())
                url_list.append(i.get('href'))
            for i in range(len(url_list)):
                extract_information(url_list[i],type_list[i].split('/')[0],f)
            ak = soup.find(class_="c-pagination__arrow c-pagination__arrow--next")
            new_url =ak.get('href')
            r = requests.get(new_url)
            soup = BeautifulSoup(r.content,'html.parser')
    else:
        type_list = []
        restaurant_list = []
        url_list = []
        type_ = soup.find_all(class_ = 'list-rst__area-genre cpy-area-genre')#和食とか洋食とか
        abst = soup.find_all(class_="list-rst__rst-name-target cpy-rst-name")#その店のURLを取りたい
        for i in type_:
            type_list.append(i.get_text().replace(' ',''))
        for i in abst:
            restaurant_list.append(i.get_text())
            url_list.append(i.get('href'))
            time.sleep(1)
        for i in range(len(url_list)):
            extract_information(url_list[i],type_list[i].split('/')[0],f)

def extract_information(url,nearest,f):
    list_ = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    p = soup.find(class_="rdheader-rating__score-val-dtl")
    review = p.get_text()
    table = soup.find(class_ = "c-table c-table--form rstinfo-table__table")
    th = table.find_all('th')
    table = table.find_all('td')#0は店名 1はジャンル 2は電話番号 3は予約の可否　4は住所 5はアクセス　6は営業時間　7は予算　8はよくわからん口コミ集計予算分布?　9は支払方法
    
    for i in table:
        list_.append(i.get_text().replace('予算分布を見る','').replace('\t','').replace(' ','').replace('\n','').replace('大きな地図を見る周辺のお店を探す','').replace('新型コロナウイルス感染拡大により、営業時間・定休日が記載と異なる場合がございます。ご来店時は事前に店舗にご確認ください。','').replace('\r',''))
    try:
        if th[1].get_text() == '受賞・選出歴':
            f.write(list_[0].replace('\n','') + '\t' + list_[2].replace('\n','') + '\t' + list_[5].replace('\n','') + '\t' + list_[6].replace('\n','') + '\t' + list_[7].replace('\n','') + '\t' + list_[8].replace('\n','') + '\t' + review  + '\t' + nearest + '\n')
        else:    
            f.write(list_[0].replace('\n','') + '\t' + list_[1].replace('\n','') + '\t' + list_[4].replace('\n','') + '\t' + list_[5].replace('\n','') + '\t' + list_[6].replace('\n','') + '\t' + list_[7].replace('\n','') + '\t' + review  + '\t' + nearest +  '\n')
    except IndexError:
        return
    time.sleep(1)

def main():
    area_names,area_urls=get_area()

    for i in range(len(area_urls)):
        with open(os.path.join(current_dir,f'tabelog_scrape/{area_names[i]}_restaurants_1.tsv'),mode='w',encoding='utf-8') as f:
            get_detail_area(area_names[i],area_urls[i],f)
            print(area_names[i] + ' ended')

    #get_restaurant(url)
    # extract_information()

if __name__ == '__main__':
    main()