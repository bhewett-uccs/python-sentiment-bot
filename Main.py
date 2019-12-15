from __future__ import print_function # Replacing the print function to send into the user interface
try:
	import __builtin__
except ImportError: # Python 3
	import builtins as __builtin__
import shelve
import datetime
import os
import sys
import traceback
import re
from PySide2 import QtGui
from PySide2.QtCore import QFile
from PySide2.QtCore import Slot
from PySide2.QtGui import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
import ctypes	# Used to make message boxes
from yaspin import yaspin
from yaspin.spinners import Spinners

sentiment_data = {}


# Initialize the user interface window
def initializeUserInterface():
	global app
	global window
	global outputTxt
	global computeBtn
	global subjectTxt
	global progressBar
	global calendar

	app = QApplication(sys.argv)
	uiFile = QFile('Resources/interface.ui')
	uiFile.open(QFile.ReadOnly)
	loader = QUiLoader()
	window = loader.load(uiFile)
	uiFile.close()

	outputTxt = window.findChild(QPlainTextEdit, 'outputTxt')
	computeBtn = window.findChild(QPushButton, 'computeBtn')
	subjectTxt = window.findChild(QLineEdit, 'subjectTxt')
	progressBar = window.findChild(QProgressBar, 'progressBar')
	calendar = window.findChild(QCalendarWidget, 'calendar')
	computeBtn.clicked.connect(computeBtnClick)
	window.show()

	sys.exit(app.exec_())

def save_data(keyword):
	""" Saves retrieved data for quick accessing when needed """
	filename = keyword + '_sentiment_data'
	shelf_file = shelve.open(filename)
	shelf_file[filename] = sentiment_data
	shelf_file.close()

def load_data(keyword):
	""" Loads previously saved sentiment data """
	global sentiment_data
	filename = keyword + '_sentiment_data'
	shelf_file = shelve.open(filename)
	sentiment_data = shelf_file.get(filename, {})

def get_date_string():
	""" Returns the date string for the date we are fetching sentiment data for """
	return (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def get_sma(data, length):
	""" Returns the simple moving average over a period of LENGTH """
	if len(data) < length:
		return "Not enough Data"

	subset = data[-length:]
	return sum(subset) / len(subset)

def display_overview():
	""" Outputs some basic, relevant information to the user """
	print()
	rprint("-------------- 7 Day Sentiment Average ---")
	for sentiment_source in sentiment_data:
		data = [item[1] for item in sentiment_data[sentiment_source]]
		sma = get_sma(data, 7)
		rprint("%s: %s" % (sentiment_source, sma))
	print()
	rprint("------------------- Last Day Sentiment ---")
	for sentiment_source in sentiment_data:
		data = sentiment_data[sentiment_source]
		sentiment = data[-1][1]
		rprint("%s: %s" % (sentiment_source, sentiment))
		if len(data) > 1:
			if data[-1][1] > data[-2][1]:
				rprint("Sentiment is INCREASING  ")
			elif data[-1][1] < data[-2][1]:
				rprint("Sentiment is DECREASING  ")
			else:
				rprint("Sentiment is NEUTRAL  ")
		print()

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
	crawlers = {}

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
@yaspin(Spinners.arc, text="Working...")
def getSentiment(keyword):
	sumSentiments = 0
	numSentiments = 0
	count = 0
	countMax = len(crawlers.items())
	load_data(keyword)
	for (name, module) in crawlers.items():
		print()
		print('_' * width)
		rprint(f'Fetching from {name}')
		if not 'fetch' in dir(module):
			print(f'{name} does not have a fetch() function')
		else:
			key = name[:-3]
			if key not in sentiment_data:
				sentiment_data[key] = []

			try:
				if not len(sentiment_data[key]) or (sentiment_data[key][-1][0] != get_date_string()):
					sentiment = module.fetch(keyword)
					sentiment_data[key].append((get_date_string(), sentiment))
				else:
					sentiment = sentiment_data[key][-1][1]

				sumSentiments += sentiment
				numSentiments += 1
				rprint(f'Sentiment from {name}: {sentiment}')
			except Exception as e:
				printException(e)
				return 0

		count += 1
		progressBar.setValue(count / countMax * 100)

		print()
	save_data(keyword)
	if numSentiments == 0: # Avoid division by zero if there are no files
		return 0
	return sumSentiments / numSentiments

# Called on button press
@Slot()
def computeBtnClick():
	keyword = subjectTxt.text().lower()

	init()
	sentiment = getSentiment(keyword)
	print('=' * width)
	rprint(f'Overall {keyword.capitalize()} sentiment: {sentiment}')
	display_overview()
	# if sentiment > 0:
	# 	rprint('(BUY)')
	# 	alert(f'The conclusion for "{keyword.capitalize()}" is BUY\n\nSentiment = {sentiment}', 'Sentiment: BUY.')
	# elif sentiment < 0:
	# 	rprint('(SELL)')
	# 	alert(f'The conclusion for "{keyword.capitalize()}" is SELL\n\nSentiment = {sentiment}', 'Sentiment: SELL.')
	# else:
	# 	alert(f'The conclusion for "{keyword.capitalize()}" is WAIT\n\nSentiment = {sentiment}', 'Sentiment: WAIT.')

# Make a message dialog
def alert(msg, title):
	if os.name == "nt":
		ctypes.windll.user32.MessageBoxW(0, msg, title, 0)

# Overrides the current print
def print(*args, **kwargs):
	try:
		if(len(args) > 0):
			outputTxt.appendPlainText(str(args[0]))
		else:
			outputTxt.appendPlainText('')
		window.update()
	except:
		pass

	#__builtin__.print('My overridden print() function!')
	return __builtin__.print(*args, **kwargs)

width = 69
os.system('cls')
print('=' * width)
rprint('Starting application...')
print('=' * width)
initializeUserInterface()
#main(keyword)
