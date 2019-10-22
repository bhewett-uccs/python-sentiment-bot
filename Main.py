import os

# Print a right-aligned message
def rprint(text):
	print(text.rjust(width))

# Initialize all modules
def init():
	global width
	global crawlers
	width = 80
	crawlers = {}

	os.system('cls')
	print('_' * width)
	rprint('Initializing modules...')

	# Loop through each file in the Crawlers directory
	for file in os.listdir('Crawlers'):
		if not os.path.isfile('Crawlers/' + file): # directory
			continue
		if not file.endswith('.py') or file.count('.') > 1:
			print(f'Invalid file name "{file}"')
			continue
		# Extract the file name without the extension
		name = file.split('.')[0]
		# Import the module object
		module = __import__('Crawlers', fromlist = [name])
		# Convert the module objects into key-value pairs
		for (key, value) in module.__dict__.items():
			if(key.startswith('__')):
				continue
			crawlers[key + '.py'] = value

# Call the fetch() function within each module
def getSentiment():
	sumSentiments = 0
	numSentiments = 0
	for (name, module) in crawlers.items():
		print()
		print('_' * width)
		rprint(f'Fetching from {name}   ')
		if not 'fetch' in dir(module):
			print(f'{name} does not have a fetch() function   ')
		else:
			sentiment = module.fetch()
			sumSentiments += sentiment
			numSentiments += 1
			rprint(f'Sentiment from {name}: {sentiment}')
		print()
	if numSentiments == 0:
		return 0
	return sumSentiments / numSentiments


init()
sentiment = getSentiment()
print('=' * width)
rprint(f'Overall Bitcoin sentiment: {sentiment}')
if sentiment > 0:
	rprint('BUY')
elif sentiment < 0:
	rprint('SELL')
