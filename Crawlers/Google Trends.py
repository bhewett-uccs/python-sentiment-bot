from pytrends.request import TrendReq
import pandas
import time

# Returns the sentiment for this service
def fetch(keyword):
	try:
		pytrend = TrendReq(hl='en-US', tz=360, retries=20, backoff_factor=0.5)
		pytrend.build_payload([keyword], cat=0, timeframe='today 3-m', geo='', gprop='')
		interest = pytrend.interest_over_time()
		print(interest)
		searches = list(interest[keyword])
		searches = [10, 20]
		differenceSum = 0
		differenceCount = -1
		prevNum = searches[0]
		for num in searches: # Compute the slope of the number of searches
			differenceSum += num - prevNum
			prevNum = num
			differenceCount += 1
		return differenceSum / differenceCount / 10 # Every ten sloped searches increases the sentiment by 1
	except:
		return 0

print('Initialized Google Trends')
