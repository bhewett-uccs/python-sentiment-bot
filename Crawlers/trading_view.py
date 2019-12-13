import requests
import time
from bs4 import BeautifulSoup
from textblob import TextBlob

def sentiment(sentence):
	opinion = TextBlob(sentence)
	return opinion.sentiment.polarity

# Returns the sentiment for this service
def fetch(keyword):
	url = f'https://www.tradingview.com/ideas/search/{keyword}/'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
	response = requests.get(url, headers=headers, timeout=10)
	#time.sleep(5)
	response.raise_for_status()
	soup = BeautifulSoup(response.text, features='html.parser')
	
	sentimentCounter = 0
	sentimentSum = 0
	elements = soup.find_all('span', class_='tv-idea-label tv-widget-idea__label tv-idea-label--short')
	for element in elements:
		text = element.get_text()
		print(f'{keyword.capitalize()} trading status: {text}')
		if 'short' in text.lower():
			sentimentSum -= 0.5
		else:
			sentimentSum += 0.5
		sentimentCounter += 1


	output = 0
	if sentimentCounter != 0: # Avoid divide by zero
		output = sentimentSum / sentimentCounter

	return output

print('Initialized Trading View')
