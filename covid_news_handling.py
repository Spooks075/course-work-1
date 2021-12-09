'''

Description:

    gets news articles from an api and then creates a list
    of dictionaries contatining the title, content and link
    to each of those articles

'''
import sched
import time
import json
import requests
from flask import Markup

s = sched.scheduler(time.time,time.sleep)

#gets settings from config file
#with open('config.json',encoding="utf-8") as f:
#    config_data = json.load(f)

def news_API_request(search_terms:str = 'covid COVID-19 coronavirus') -> json:
    '''

    Description:

        Function that gets news articles from the news api

    Arguments:

        search_terms {string} : search terms for news articles

    Returns:

        articles {json} : list of dictionaries contatining articles with sub dictionaries:
                            {title} {content} {url}

    '''

    #creates url
    complete_url =  'https://newsapi.org/v2/everything?q=' + search_terms
    complete_url += '&apiKey=' + "1019ef69744f449cb833019a1222dc37"#config_data["apikey"]
    #request data from api
    articles = requests.get(complete_url).json()
    return articles


def news_list(news_articles_json:json) -> list:
    '''

    Description:

        Function that creates a list of dictinaries containitng articles with their
        title, content and a link to the article

    Arguments:

        news_articles_json {json} : list of dictionaries contatining articles with sub dictionaries:
                            {title} {content} {url}

    Returns:

        news_articles_list {list} : list of dictinaries containitng articles with sub ditionaries:
                                    {title} {content}

    '''
    news_articles_list = []
    news_articles_dict = news_articles_json['articles']
    #goes through each article in list and takes its title,
    #description and creates a link to article using url
    for articals in news_articles_dict:
        artical = {"title": articals['title'],
        "content":articals['description'] +
        Markup(" <a href=" +articals['url'] + ">" + "read more ...")}
        news_articles_list.append(artical)
    return news_articles_list


def call_articles() -> list:
    '''

    Description:

        passes list of news articles into flask module

    Arguments:

        None

    Returns:

        articles {list} : list of dictinaries containitng articles with sub ditionaries:
                                    {title} {content}

    '''

    articles = news_list(news_API_request())#config_data["default news terms"])
    return articles

def update_news(update_name:str) -> sched.Event|str:
    '''
    Description:

        Function that schedules a covid news update

    Arguments:

        update_name {string} : name of update

    Returns:

        sched_update {event} : scheduled update event
        update_name {string} : name of update

    '''
    sched_update = s.enter(1,1,news_list,(news_API_request()))#config_data["default news terms"])

    return sched_update,update_name
