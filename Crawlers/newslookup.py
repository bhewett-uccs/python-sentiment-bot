import requests
import time
from bs4 import BeautifulSoup
from textblob import TextBlob

def sentiment(sentence):
	opinion = TextBlob(sentence)
	return opinion.sentiment.polarity

# Returns the sentiment for this service
def fetch(keyword):
	url = f'https://newslookup.com/results?q={keyword}'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
	response = requests.get(url, headers=headers, timeout=10)
	response.raise_for_status()
	soup = BeautifulSoup(response.text, features='html.parser')
	
	sentimentCounter = 0
	sentimentSum = 0
	elements = soup.find_all('p', class_='desc')
	for element in elements:
		text = element.get_text()
		if keyword.lower() in text:
			num = sentiment(text)
			sentimentSum += num
			sentimentCounter += 1
			print(text)


	output = 0
	if sentimentCounter != 0: # Avoid divide by zero
		output = sentimentSum / sentimentCounter

	return output * 5

print('Initialized Youtube')
