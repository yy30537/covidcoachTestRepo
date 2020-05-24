from newsapi import NewsApiClient
import pandas as pd
import requests
import json
import sqlite3


def get_news_list():
    newsapi = NewsApiClient(api_key="31119c92ed55433d9083373aba50327b")
    topheadlines = newsapi.get_top_headlines(q='covid' or 'coronavirus', language='en', page_size=100)

    articles = topheadlines['articles']
    countList = []
    news_description = []
    news_title = []
    news_image = []
    news_url = []

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # c.execute('DROP TABLE IF EXISTS news_table')
    # c.execute(
    #     'CREATE TABLE IF NOT EXISTS news_table(news_id INTEGER PRIMARY KEY, author TEXT, title TEXT, description TEXT, url TEXT, url_to_image TEXT, publish_date TEXT, content TEXT)')
    # 该表字段包括：
    # news_id           :   新闻编号（可考虑automatic increment） - p.k.主键
    # author            :   作者名称
    # title             :   标题
    # description       :   描述
    # url               :   原文链接
    # url_to_image      :   图片地址
    # publish_date      :   发布日期
    # content           :   文章的内容

    c.execute('SELECT count(*) FROM news_table')
    count = c.fetchone()[0]
    #print("number of fetched news: ", count)
    for i in range(len(articles)):
        count = count + 1
        countList.append(count)
        myarticles = articles[i]
        news_title.append(myarticles['title'])
        news_description.append(myarticles['description'])
        news_image.append(myarticles['urlToImage'])
        news_url.append(myarticles['url'])
        c.execute('INSERT INTO news_table(author, title, description, url, url_to_image, publish_date, content) VALUES(?,?,?,?,?,?,?)', (myarticles['author'],myarticles['title'],myarticles['description'],myarticles['url'],myarticles['urlToImage'],myarticles['publishedAt'],myarticles['content']))
    conn.commit()

    news_list = zip(news_title, news_description, news_image, news_url, countList)

    # dataframe = pd.DataFrame(articles)
    return news_list


def get_stats_list():
    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "4d79bf1779msh12322835c66a566p1dc930jsnaa9f4295d835"
    }

    # Get latest data for whole world.
    url_Totals = "https://covid-19-data.p.rapidapi.com/totals"
    querystring_Totals = {"format": "json"}
    response_Totals = requests.request("GET", url_Totals, headers=headers, params=querystring_Totals)
    obj = response_Totals.json()
    data_world = obj[0]

    # Get latest data for specific country. (in this case, USA)
    url_USA = "https://covid-19-data.p.rapidapi.com/country"
    querystring_USA = {"format": "json", "name": "USA"}
    response_USA = requests.request("GET", url_USA, headers=headers, params=querystring_USA)
    obj = response_USA.json()
    data_USA = obj[0]
    data_USA_1 = {'confirmed': data_USA['confirmed'], 'recovered': data_USA['recovered'],
                  'critical': data_USA['critical'], 'deaths': data_USA['deaths']}

    list_of_two_dicts = [data_world, data_USA_1]
    #print(list_of_two_dicts[0])
    #print(list_of_two_dicts[1])

    return list_of_two_dicts
