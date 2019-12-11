import requests
from bs4 import BeautifulSoup
import textblob
import os
import datetime
import time
from dotenv import load_dotenv

load_dotenv()


class NewsSentimentBot:
    def __init__(self, symbol=None):
        if not symbol:
            symbol = "BTC"

        self.keyword_list = self.generate_keywords(symbol)

        # Gets API access and token keys, etc from .env file located in project root directory
        self.api_auth_token = os.getenv('API_AUTH_TOKEN')

    def generate_keywords(self, symbol):
        """
        Generates basic keywords based on user input (symbol)
        :param symbol: user input -> either coin ticker symbol, or coin name
        :return: list of keywords to search for in individual tweets
        """
        url = "https://apiv2.bitcoinaverage.com/symbols/indices/names"
        try:
            response = requests.get(url)
            response.raise_for_status()
            names = response.json()

            for coin_type in names:
                for key, value in names[coin_type].items():
                    if symbol.upper() == key or symbol.lower() == value.lower():
                        return [key, value] if key != "BTC" else [key, value, "XBT"]
        except requests.RequestException as e:
            print(e)

        return [symbol]

    def get_utc_now(self):
        """ Gets a normalized UTC datetime object """
        now = datetime.datetime.utcnow()
        utc_now = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0)
        return utc_now

    def get_sentiment(self, content):
        analysis = textblob.TextBlob(content)
        return analysis.polarity

    def geometric_avg(self, iterable):
        """ Returns the geometric average of a list of sentiment """
        if iterable:
            product = 1
            for polarity in iterable:
                product *= polarity

            return product**(1/len(iterable))
        return 0

    def get_aggregate_geometric_avg(self, pos_scores, neg_scores, neu_scores):
        positive_geometric_avg = self.geometric_avg(pos_scores)
        negative_geometric_avg = self.geometric_avg(neg_scores) if len(neg_scores) % 2 == 0 \
            else self.geometric_avg([abs(score) for score in neg_scores])

        return ((sum(pos_scores)*positive_geometric_avg) - (sum(neg_scores)*negative_geometric_avg))\
            / (sum(pos_scores) + sum(neg_scores) + sum(neu_scores))

    def get_news_sentiment(self):
        """ Generates a list of sentiment from each individual news article over the last trading day """
        url_list = []
        news_sentiment_list = []
        end_date = self.get_utc_now()
        begin_date = (end_date - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'

        base_url = "https://cryptopanic.com/api/v1/posts/?auth_token="
        opt_public = "&public=True"
        opt_currencies = "&currencies=" + self.keyword_list[0]
        opt_kind = "&kind=news"

        api_url = base_url + self.api_auth_token + opt_public + opt_currencies + opt_kind

        building_urls = True
        while building_urls and api_url:
            try:
                response = requests.get(api_url)
                response.raise_for_status()

                response = response.json()
                for result in response['results']:
                    timestamp = result['created_at']
                    if timestamp > end_date:
                        continue
                    elif timestamp < begin_date:
                        building_urls = False
                        break

                    url_list.append(result['url'])

                api_url = response['next']
                time.sleep(0.2)     # API requests limited to 5/sec

            except requests.RequestException as error:
                print(error)

        for url in url_list:
            try:
                response = requests.get(url)
                response.raise_for_status()

                source = BeautifulSoup(response.content, features="html.parser")

                # Get headline content...
                title = source.find('meta', property="og:title")["content"]
                # Get description content...
                description = source.find('meta', property="og:description")["content"]
                news_content = title + ' ' + description

                # Gets sentiment based on headline + description, rather than dealing with the entire article itself...
                news_sentiment_list.append(self.get_sentiment(news_content))

            except requests.RequestException as error:
                print(error)

        return news_sentiment_list

    def build_aggregate_sentiment(self, news_sentiment_list):
        """ Builds and calculates the aggregated sentiment for a list of sentiment """
        positive_scores = []
        negative_scores = []
        neutral_scores = []

        for sentiment in news_sentiment_list:
            if sentiment > 0:
                positive_scores.append(sentiment)
            elif sentiment < 0:
                negative_scores.append(sentiment)
            elif sentiment == 0:
                neutral_scores.append(0)

        return self.get_aggregate_geometric_avg(positive_scores, negative_scores, neutral_scores)

    def fetch(self):
        return self.build_aggregate_sentiment(self.get_news_sentiment())


def fetch(symbol=None):
    bot = NewsSentimentBot(symbol=symbol)
    return bot.fetch()
