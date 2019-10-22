
import os
#import sys

#crawlers = __import__('Crawlers', fromlist=[])
#print(dir(crawlers))
#print(crawlers.__file__)
#sys.path.append('Crawlers')

def printWall(fill = '_'):
	print(fill * width)

def message(text):
	print(text.rjust(width))

def init():
	global width
	global crawlers
	width = 80
	crawlers = {}

	os.system('cls')
	printWall()
	message('Initializing modules...')
	# Loop through each file in the Crawlers directory
	for file in os.listdir('Crawlers'):
		name = '.'.join(file.split('.')[:-1]) # Remove file extension
		module = __import__('Crawlers', fromlist = [name])
		for (key, value) in module.__dict__.items():
			if(key.startswith('__')):
				continue
			crawlers[key + '.py'] = value

def getSentiments():
	sumSentiments = 0
	numSentiments = 0
	for (name, module) in crawlers.items():
		print()
		printWall()
		message(f'Fetching from {name}   ')
		if not 'fetch' in dir(module):
			message(f'Error. {name} does not have a fetch() function.')
		else:
			sentiment = module.fetch()
			sumSentiments += sentiment
			numSentiments += 1
			message(f'Sentiment from {name}: {sentiment}')
		print()
	printWall('=')
	return sumSentiments / numSentiments


init()
message(f'Total Bitcoin sentiment: {getSentiments()}')