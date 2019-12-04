import requests
from bs4 import BeautifulSoup
from textblob import TextBlob


def sentiment(sentence):
	opinion = TextBlob(sentence)
	return opinion.sentiment.polarity

def analyzeTwitterProfile(handle, keyword):
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
		if keyword.lower() in tweet:
			sentimentSum += sentiment(tweet)
			sentimentCounter += 1

	output = 0
	if sentimentCounter != 0: # Avoid divide by zero
		output = sentimentSum / sentimentCounter
	print(f'The sentiment for @{handle} is {output}')

	return output


# Returns the sentiment for this service
def fetch(keyword):
	sentimentSum = 0;
	sentimentCounter = 0

	# A list of the top Bitcoin experts and market movers
	sentimentSum += analyzeTwitterProfile('aantonop', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('brian_armstrong', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('brucefenton', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('brockpierce', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('lopp', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('jonmatonis', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('NickSzabo4', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('peterktodd', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('pwuille', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('kyletorpey', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('eric_lombrozo', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('erikfinman', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('TheDeadReds', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('CoinFestUK', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('queentatiana', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('victoriavaneyk', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('BryceWeiner', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('derose', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('brianchoffman', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('blythemasters', keyword)
	if sentimentSum != 0: sentimentCounter += 1
	sentimentSum += analyzeTwitterProfile('rogerkver', keyword)
	if sentimentSum != 0: sentimentCounter += 1

	if sentimentCounter == 0:
		return 0 # Avoid division by zero
	else:
		return sentimentSum / sentimentCounter

print('Initialized Twitter')