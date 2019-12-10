from __future__ import print_function # Replacing the print function to send into the user interface
try:
	import __builtin__
except ImportError: # Python 3
	import builtins as __builtin__
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
def getSentiment(keyword):
	sumSentiments = 0
	numSentiments = 0
	count = 0
	countMax = len(crawlers.items())
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

		count += 1
		progressBar.setValue(count / countMax * 100)

		print()
	if numSentiments == 0: # Avoid division by zero if there are no files
		return 0
	return sumSentiments / numSentiments

# Called on button press
@Slot()
def computeBtnClick():
	global keyword
	keyword = subjectTxt.text().lower()

	init()
	sentiment = getSentiment(keyword)
	print('=' * width)
	rprint(f'Overall {keyword.capitalize()} sentiment: {sentiment}')
	if sentiment > 0:
		rprint('(BUY)')
		alert(f'The conclusion for "{keyword.capitalize()}" is BUY\n\nSentiment = {sentiment}', 'Sentiment: BUY.')
	elif sentiment < 0:
		rprint('(SELL)')
		alert(f'The conclusion for "{keyword.capitalize()}" is SELL\n\nSentiment = {sentiment}', 'Sentiment: SELL.')
	else:
		alert(f'The conclusion for "{keyword.capitalize()}" is WAIT\n\nSentiment = {sentiment}', 'Sentiment: WAIT.')

# Make a message dialog
def alert(msg, title):   
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

global width
width = 69
os.system('cls')
print('=' * width)
rprint('Starting application...')
print('=' * width)
initializeUserInterface()
#main(keyword)
