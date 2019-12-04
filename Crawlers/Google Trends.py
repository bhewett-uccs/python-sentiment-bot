import pytrends
import pandas

# Returns the sentiment for this service
def fetch(keyword):
	pytrend = TrendReq(hl='en-US', tz=360)
	pytrends.build_payload([keyword], cat=0, timeframe='today 7-d', geo='', gprop='')
	print(pytrends.interest_over_time())
	return 1

print('Initialized Google Trends')
