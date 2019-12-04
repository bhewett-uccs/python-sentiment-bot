import requests
import time
from bs4 import BeautifulSoup
from textblob import TextBlob

def sentiment(sentence):
	opinion = TextBlob(sentence)
	return opinion.sentiment.polarity

# Returns the sentiment for this service
def fetch(keyword):
	url = f'https://www.investing.com/search/?q={keyword}&tab=news'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
	response = requests.get(url, headers=headers)
	#time.sleep(5)
	response.raise_for_status()
	soup = BeautifulSoup(response.text, features='html.parser')
	
	# Data has been parsed, now we fetch all the tweet text
	elements = soup.find_all('p', class_='js-news-item-content')
	sentimentCounter = 0
	sentimentSum = 0
	for element in elements:
		text = element.get_text()
		if keyword.lower() in text:
			sentimentSum += sentiment(text)
			sentimentCounter += 1

	output = 0
	if sentimentCounter != 0: # Avoid divide by zero
		output = sentimentSum / sentimentCounter

	return output

print('Initialized Investing.com')
