import requests
from bs4 import BeautifulSoup
from textblob import TextBlob


def sentiment(sentence):
	opinion = TextBlob(sentence)
	return opinion.sentiment.polarity

def analyzeTwitterProfile(handle):
	url = 'https://twitter.com/' + handle
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
	response = requests.get(url, headers=headers)
	response.raise_for_status()
	soup = BeautifulSoup(response.text, features='html.parser')
	
	# Data has been parsed, now we fetch all the tweet text
	elements = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
	tweets = []
	for element in elements:
		tweets.append(element.text.lower())
	
	# Add up each tweet's sentiment
	sentimentCounter = 0
	sentimentSum = 0
	for tweet in tweets:
		if 'bitcoin' in tweet:
			sentimentSum += sentiment(tweet)
			sentimentCounter += 1

	output = 0
	if sentimentCounter != 0: # Avoid divide by zero
		output = sentimentSum / sentimentCounter
	print(f'The sentiment for @{handle} is {output}')

	return output


# Returns the sentiment for this service
def fetch():
	sentimentSum = 0;
	sentimentCounter = 0

	# A list of the top Bitcoin experts and market movers
	sentimentSum += analyzeTwitterProfile('aantonop')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('brian_armstrong')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('brucefenton')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('brockpierce')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('lopp')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('jonmatonis')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('NickSzabo4')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('peterktodd')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('pwuille')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('kyletorpey')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('eric_lombrozo')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('erikfinman')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('TheDeadReds')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('CoinFestUK')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('queentatiana')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('victoriavaneyk')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('BryceWeiner')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('derose')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('brianchoffman')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('blythemasters')
	sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('rogerkver')
	sentimentCounter += 1
	return sentimentSum / sentimentCounter

print('Initialized Twitter')