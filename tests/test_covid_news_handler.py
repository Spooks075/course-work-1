from covid_news_handler import news_API_request
from covid_news_handler import update_news
from covid_news_handler import call_articles

def test_news_API_request():
    assert news_API_request(), "news_API_request: FAILED "

def test_update_news():
    articles = update_news(news_API_request())
    for article in articles:
        assert type(article['title']) == str, "update_news: FAILED"

def test_call_articles():
    articles = call_articles()
    for article in articles:
        assert type(article['title']) == str, "call_articles: FAILED"

if __name__ == "__main__":
    try:
        test_update_news()
        test_news_API_request()
        test_call_articles()
    except AssertionError as message:
        print(message)