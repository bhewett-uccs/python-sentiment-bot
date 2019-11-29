import tweepy
import textblob
import requests
import preprocessor as tweet_scrubber
import re
import datetime
import os
from dotenv import load_dotenv
from collections import deque
import pprint

load_dotenv()


class TwitterSentimentBot:
    lookback_period = 1

    def __init__(self, symbol=None):
        if not symbol:
            symbol = "BTC"

        self.user_list = self.get_user_list()
        self.keyword_list = self.generate_keywords(symbol)

        # Gets API access and token keys, etc from .env file located in project root directory
        consumer_key = os.getenv('CONSUMER_KEY')
        consumer_secret = os.getenv('CONSUMER_SECRET')
        access_token = os.getenv('ACCESS_TOKEN')
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

        try:
            # Initialize api instance
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            self.twitter_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        except:
            print("ERROR: Failed Authentication!")

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
        utc_now = datetime.datetime(now.year, now.month, now.day, 6, 0, 0, 0)
        return utc_now

    def get_user_list(self):
        """ Gets the list of users from file stored in root directory"""
        with open("user_list.txt", "r") as f:
            content = f.read().splitlines()
            return list(filter(None, content))

    def get_sentiment(self, tweet_content):
        analysis = textblob.TextBlob(tweet_content)
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

    def harvest_twitter_user_sentiment(self):
        """ Builds a list of individual sentiment scores (and their timestamps) for each user in the user list """
        sentiment_dict = {}
        end_date = self.get_utc_now() - datetime.timedelta(days=self.lookback_period)
        keywords = re.compile("(%s)" % "|".join(self.keyword_list), re.IGNORECASE)
        tweet_scrubber.set_options(tweet_scrubber.OPT.URL, tweet_scrubber.OPT.MENTION)

        for user in self.user_list:
            for tweet in tweepy.Cursor(self.twitter_api.user_timeline, id=user,
                                       tweet_mode="extended", include_rts=True).items():
                # If tweet timestamp is beyond the date range we're interested in, break out of loop
                if tweet.created_at < end_date:
                    break

                # A user's retweeted tweets are handled differently than normal tweets
                if tweet.truncated:
                    text = tweet.retweeted_status.full_text
                else:
                    text = tweet.full_text

                # Remove misc items (links, mentions) from a tweet before checking for keywords
                text = tweet_scrubber.clean(text)

                # If there's a keyword match, we've found a relevant tweet. Get the sentiment + timestamp, and save it
                if keywords.search(text):
                    this_sentiment = (self.get_sentiment(text), tweet.created_at)
                    try:
                        sentiment_dict[user].append(this_sentiment)
                    except KeyError:
                        sentiment_dict[user] = deque([this_sentiment])

        return sentiment_dict

    def build_aggregate_sentiment(self, user_sentiment_dict):
        """ Builds and calculates the aggregated sentiment across all users for a range of given time periods """
        aggregate_sentiment_dict = {}

        now = self.get_utc_now()
        # for period in sorted(time_periods):
        for i in range(self.lookback_period):
            positive_scores = []
            negative_scores = []
            neutral_scores = []
            end_date = now - datetime.timedelta(days=i+1)
            begin_date = end_date + datetime.timedelta(days=1)

            for user in user_sentiment_dict:
                user_sentiment = user_sentiment_dict[user]
                while user_sentiment:
                    this_sentiment = user_sentiment.popleft()
                    timestamp = this_sentiment[1]
                    if timestamp > begin_date:
                        continue
                    if timestamp < end_date:
                        user_sentiment.appendleft(this_sentiment)
                        break

                    score = this_sentiment[0]
                    if score > 0:
                        positive_scores.append(score)
                    elif score < 0:
                        negative_scores.append(score)
                    elif score == 0:
                        neutral_scores.append(0)

            aggregate_sentiment_dict[end_date.strftime("%Y-%m-%d")] = self.get_aggregate_geometric_avg(positive_scores,
                                                                                                       negative_scores,
                                                                                                       neutral_scores)
        return aggregate_sentiment_dict

    def fetch(self, num_days_sentiment=None):
        """ Main public-facing function used to grab total aggregate sentiment and return it """
        if num_days_sentiment:
            self.lookback_period = num_days_sentiment

        return self.build_aggregate_sentiment(self.harvest_twitter_user_sentiment())
