#!/usr/bin/python

import datetime

### GLOBAL CONSTANTS

# stock types
COMMON = 0
PREFERRED = 1

# buy/sell
BUY = 0
SELL = 1

# time frame for Volume Weighted Stock Price calculation
VWSP_TIME_DELTA = datetime.timedelta(minutes = 15)


### CLASSES DEFINITIONS
class cTrade:
	"""A record of a stock trade"""

	def __init__(self, shares_cnt, trade_type, price):
		if trade_type != BUY and trade_type != SELL:
			raise TypeError

		# both shares_cnt and price expected to be numbers
		if not hasattr(shares_cnt, '__int__') or not hasattr(price, '__int__'):
			raise TypeError

		self.timestamp = datetime.datetime.now()
		self.shares_cnt = shares_cnt
		self.trade_type = trade_type
		self.price = price


class cStock:
	"""A simple stock class"""

	def __init__(self, symbol, stock_type, last_div, par_value, fixed_div = None):
		if stock_type != COMMON and stock_type != PREFERRED:
			raise TypeError
		
		self.symbol = symbol
		self.stock_type = stock_type
		self.last_div = last_div
		self.par_value = par_value
		self.fixed_div = fixed_div
		
		#list of objects cTrade - keeps trading history
		self.trade_history = []


	# calculate the dividend yield
	def calc_div_yield(self, price):
		if price == 0:
			return None

		if self.stock_type == COMMON:
			return float(self.last_div) / price
		else:
			return float(self.fixed_div * 0.01 * self.par_value) / price


	# calculate the P/E ratio
	def calc_PE_ratio(self, price):

		dividend = self.calc_div_yield(price)

		if dividend != 0 and dividend != None:
			return price / dividend
		else:
			return None


	# calculate the Volume Weighted Stock Price
	def calc_VWSP(self):
		now = datetime.datetime.now()

		# go back through history and look for the first trade not older than the time limit
		idx = len(self.trade_history)
		while idx > 0 and self.trade_history[idx - 1].timestamp >= now - VWSP_TIME_DELTA:
			idx -= 1

		# from this point on - sum of the current and all following (younger) trades
		sum_prices = 0
		sum_quantity = 0
		while idx < len(self.trade_history):
			sum_prices += self.trade_history[idx].shares_cnt * self.trade_history[idx].price
			sum_quantity += self.trade_history[idx].shares_cnt
			idx += 1

		if sum_quantity == 0:
			return None

		return float(sum_prices) / sum_quantity


	# populates the trade history
	def do_trade(self, shares_cnt, buy, price):
		self.trade_history.append(cTrade(shares_cnt, buy, price))



### GLOBAL FUNCTION
def calc_geo_mean(values):
	# calculates geometric mean from a list of values
	
	mean = 1
	count = len(values)
	if count == 0:
		return None

	# square root for every value individially, so that the partial result doesn't get too big
	for i in range (0, count):
		mean *= values[i]**(1 / float(count))

	return mean



### some tests
def run_tests():
	stocks = []
	prices = []

	stocks.append(cStock('TEA', COMMON, 0, None, 100))
	stocks.append(cStock('POP', COMMON, 8, None, 100))
	stocks.append(cStock('ALE', COMMON, 23, None, 60))
	stocks.append(cStock('GIN', PREFERRED, 8, 2, 100))
	stocks.append(cStock('JOE', COMMON, 13, None, 250))
	
	stocks[0].do_trade(10.2, BUY, 40)
	stocks[0].do_trade(10, BUY, 40.5)
	stocks[0].do_trade(10.9, BUY, 20.03)
	stocks[0].do_trade(40, BUY, 2)

	stocks[1].do_trade(1, BUY, 1)

	stocks[2].do_trade(5, BUY, 1000)
	stocks[2].do_trade(18, BUY, 1500)

	stocks[3].do_trade(2000, BUY, 1)

	stocks[4].do_trade(10, BUY, 10)
	stocks[4].trade_history[0].timestamp -= 2 * VWSP_TIME_DELTA # make it older than 15 minutes
	stocks[4].do_trade(12, BUY, 7)
	stocks[4].do_trade(13, BUY, 5)
	
	for i in range (0, 5):
		print "Test of stock", stocks[i].symbol
		print "dividend:", stocks[i].calc_div_yield(10)
		print "P/E ratio:", stocks[i].calc_PE_ratio(12)
		
		price = stocks[i].calc_VWSP()
		if price != None:
			prices.append(price)
		
		print "VWSP:", price
		print ""

	# honestly, it's not clear to me from the assignment what prices are supposed to be on the input,
	# so I used the Volume Weighted Stock Prices of every stock previously calculated
	print "geometric mean of all prices:", calc_geo_mean(prices)

run_tests()