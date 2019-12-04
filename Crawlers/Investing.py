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
	response = requests.get(url, headers=headers, timeout=10)
	#time.sleep(5)
	response.raise_for_status()
	soup = BeautifulSoup(response.text, features='html.parser')
	
	# Data has been parsed, now we fetch all the tweet text
	'''_elements = soup.find_all('div', class_='articleItem')
	for _element in _elements:
		elements = _element.find_all('a') + _element.find_all('p')
		sentimentCounter = 0
		sentimentSum = 0
		for element in elements:
			text = element.get_text()
			if keyword.lower() in text:
				print(text)
				sentimentSum += sentiment(text)
				sentimentCounter += 1'''
	sentimentCounter = 0
	sentimentSum = 0
	elements = soup.find_all('div', class_='articleItem')
	for element in elements:
		text = element.get_text()
		if keyword.lower() in text:
			sentimentSum += sentiment(text)
			sentimentCounter += 1
			print(text)

	output = 0
	if sentimentCounter != 0: # Avoid divide by zero
		output = sentimentSum / sentimentCounter

	return output

print('Initialized Investing.com')
