<<<<<<< Updated upstream
import os
import sys
import traceback
import re

# Print a right-aligned message
def rprint(text):

	lines = text.split('\n')
	if len(lines) == 1:
		print(text.rjust(width))
	else:
		for line in lines:
			rprint(line)

# Print an exception nicely to the screen
def printException(e):
	tb = '\n' + traceback.format_exc()
	tb = re.sub(r'File "Main.py",.*\n.*', '', tb) # Remove Main file errors
	tb = re.sub(r'\n\s+\n', '\n', tb)
	lines = tb.split('\n')
	for i in range(len(lines)): # Remove the file path, replace with just file name
		lines[i] = re.sub(r'File ".*\\([A-z\.]+)"', r'File "\1"', lines[i])
	rprint('\n'.join(lines))

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
			rprint(f'Invalid file name "{file}"')
			continue
		# Extract the file name without the extension
		name = file.split('.')[0]
		# Import the module object
		try:
			module = __import__('Crawlers', fromlist = [name])
			# Convert the module objects into key-value pairs
			for (key, value) in module.__dict__.items():
				if(key.startswith('__')):
					continue
				crawlers[key + '.py'] = value
		except Exception as e:
			printException(e)


# Call the fetch(keyword) function within each module
def getSentiment(keyword):
	sumSentiments = 0
	numSentiments = 0
	for (name, module) in crawlers.items():
		print()
		print('_' * width)
		rprint(f'Fetching from {name}')
		if not 'fetch' in dir(module):
			print(f'{name} does not have a fetch() function')
		else:
			try:
				sentiment = module.fetch(keyword)
				sumSentiments += sentiment
				numSentiments += 1
				rprint(f'Sentiment from {name}: {sentiment}')
			except Exception as e:
				printException(e)
				return 0

		print()
	if numSentiments == 0: # Avoid division by zero if there are no files
		return 0
	return sumSentiments / numSentiments

def main(keyword):
	init()
	sentiment = getSentiment(keyword)
	print('=' * width)
	rprint(f'Overall Bitcoin sentiment: {sentiment}')
	if sentiment > 0:
		rprint('(BUY)')
	elif sentiment < 0:
		rprint('(SELL)')

keyword = input('Enter a sentiment topic: ').lower()
main(keyword)
=======
import os
import sys
import traceback
import re

# Print a right-aligned message
def rprint(text):

	lines = text.split('\n')
	if len(lines) == 1:
		print(text.rjust(width))
	else:
		for line in lines:
			rprint(line)

# Print an exception nicely to the screen
def printException(e):
	tb = '\n' + traceback.format_exc()
	tb = re.sub(r'File "Main.py",.*\n.*', '', tb) # Remove Main file errors
	tb = re.sub(r'\n\s+\n', '\n', tb)
	lines = tb.split('\n')
	for i in range(len(lines)): # Remove the file path, replace with just file name
		lines[i] = re.sub(r'File ".*\\([A-z\.]+)"', r'File "\1"', lines[i])
	rprint('\n'.join(lines))

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
			rprint(f'Invalid file name "{file}"')
			continue
		# Extract the file name without the extension
		name = file.split('.')[0]
		# Import the module object
		try:
			module = __import__('Crawlers', fromlist = [name])
			# Convert the module objects into key-value pairs
			for (key, value) in module.__dict__.items():
				if(key.startswith('__')):
					continue
				crawlers[key + '.py'] = value
		except Exception as e:
			printException(e)


# Call the fetch(keyword) function within each module
def getSentiment(keyword):
	sumSentiments = 0
	numSentiments = 0
	for (name, module) in crawlers.items():
		print()
		print('_' * width)
		rprint(f'Fetching from {name}')
		if not 'fetch' in dir(module):
			print(f'{name} does not have a fetch() function')
		else:
			try:
				sentiment = module.fetch(keyword)
				sumSentiments += sentiment
				numSentiments += 1
				rprint(f'Sentiment from {name}: {sentiment}')
			except Exception as e:
				printException(e)
				return 0

		print()
	if numSentiments == 0: # Avoid division by zero if there are no files
		return 0
	return sumSentiments / numSentiments

def main(keyword):
	init()
	sentiment = getSentiment(keyword)
	print('=' * width)
	rprint(f'Overall Bitcoin sentiment: {sentiment}')
	if sentiment > 0:
		rprint('(BUY)')
	elif sentiment < 0:
		rprint('(SELL)')

keyword = input('Enter a sentiment topic: ').lower()
main(keyword)
>>>>>>> Stashed changes
