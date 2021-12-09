from covid_news_handling import news_API_request, news_list
from covid_news_handling import update_news
from covid_news_handling import call_articles

def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_update_news():
    update_news('test')


def test_news_list():
    articles = news_list(news_API_request())
    for article in articles:
        assert type(article['title']) == str, "update_news: FAILED"

def test_call_articles():
    articles = call_articles()
    for article in articles:
        assert type(article['title']) == str, "call_articles: FAILED"

if __name__ == "__main__":
    try:
        test_news_list()
        test_update_news()
        test_news_API_request()
        test_call_articles()
    except AssertionError as message:
        print(message)