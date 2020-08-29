# Important Stock Market Data
import yfinance as yf, pandas as pd, shutil, os, time, glob, smtplib, ssl
# Importing Date/Time
import datetime
# Importing Statistics
import statistics
# Get Tickers
from get_all_tickers import get_tickers as gt


# Parameters I want to work with

MAXPRICE = 20
OPENINTEREST = 40
INTHEMONEY = True

mkmin = 150000
mkmax = 10000000

class Option:
   '''This takes in the option information that I want to keep track of and
      will be important in the important information that is needed to analyze
      options. '''
   def __init__(self,name):
      self.strike = 0
      self.price = 0
      self.name = name
   def set_strike(self,strike):
      self.strike = strike
   def set_price(self,price):
      self.price = price
   def __str__(self):
      retStr = "Price: "+str(self.price)+"; Strike: "+str(self.strike)
      return retStr
   def __repr__(self):
      retStr = "Price: "+str(self.price)+"; Strike: "+str(self.strike)
      return retStr

class StockInfo:
   '''This takes in the stock information I want to keep track of and will
      be important in the basic analysis of stocks'''
   def __init__(self,name):
      self.name = name
      self.corona = 0
      self.one_month = 0
      self.five_day = 0
      self.three_m_lp = 0
      self.one_m_lp = 0
   def set_one_month(self, m):
      self.one_month = m
   def set_five_day(self, d):
      self.five_day = d
   def set_corona(self, c):
      self.corona = c
   def set_three_m_lp(self,tmlp):
      self.three_m_lp = tmlp
   def set_one_m_lp(self, omlp):
      self.one_m_lp = omlp
      

def options_in_limit(tkrSymbol):
   tkr = yf.Ticker(tkrSymbol)

   # Current Date
   dateTimeObj = datetime.datetime.now()
   today = str(dateTimeObj.year)+"-"+str(dateTimeObj.month)+"-"+str(dateTimeObj.day)
                                           
   hold = datetime.datetime(datetime.MAXYEAR,12,31)
   holder_date = ""

   # Get Soonest Expiration
   for i in tkr.options:
      dateNice = datetime.datetime(int(i[0:4]),int(i[5:7]),int(i[8:10]))
      if (dateTimeObj < dateNice) and (dateNice < hold):
         hold = dateNice
         holder_date = i
      else:
         continue
      
   # Soonest Date
   # print(holder_date)

   # Iterate Over This df
   tkrDf = tkr.option_chain(holder_date).calls

   tkrDf.head()

   # Potential Options We're Interested in Buying
   potential_buy = {}

   #for ind,row in tkrDf.iterrows():
    #  print(ind,row)

   for ind,row in tkrDf.iterrows():
      if (row['inTheMoney'] == INTHEMONEY):
         # If we are in the money
         if (row['openInterest'] > OPENINTEREST):  
            if (row['lastPrice'] < MAXPRICE):

               # Gettin ticker symbol from contract symbol
               count = 0
               for i in row['contractSymbol']:
                  if i.isalpha() or i =='.':
                     count+=1
                  else:
                      break

               # Adding to the record
               info_ls = ["Price",row['lastPrice'],"Strike",row['strike']]
               temp = Option(row['contractSymbol'][0:count])
               
               temp.set_strike(row['strike'])
               temp.set_price(row['lastPrice'])
               
               try:
                  potential_buy[row['contractSymbol'][0:count]].append(temp)
                  #sorted(potential_buy[row['contractSymbol'][0:count]], key=sort_ls)
               except KeyError:
                  potential_buy[row['contractSymbol'][0:count]] = [temp]
   return potential_buy
def five_day(tkrSymbol):
   '''Passed a symbol, and returns the decimal the stock has moved in
      the past five trading days.'''
   tkr = yf.Ticker(tkrSymbol)

   tkrHistory = tkr.history(period="5d")

   historyLs = []
   for ind,row in tkrHistory.iterrows():
      historyLs.append(row['Close'])
      # print(row['Close'])

   averageLs = []
   for i in range(1,len(historyLs)):
      averageLs.append(historyLs[i]/historyLs[i-1])
   
   average = statistics.mean(averageLs)
   # print(average)

   return average-1
   
   

def one_month(tkrSymbol):
   '''Passed a symbol, and returns the decimal the stock has moved in
      the past one month.'''
   tkr = yf.Ticker(tkrSymbol)

   tkrHistory = tkr.history(period="1mo")

   historyLs = []
   for ind,row in tkrHistory.iterrows():
      historyLs.append(row['Close'])
      # print(row['Close'])

   averageLs = []
   for i in range(1,len(historyLs)):
      averageLs.append(historyLs[i]/historyLs[i-1])
   
   average = statistics.mean(averageLs)
   # print(average)
   
   return average-1

def coronavirus(tkrSymbol):
   '''Passed a symbol, and returns the decimal the stock has moved
      since coronavirus pandemic began affecting the stock market.'''
   tkr = yf.Ticker(tkrSymbol)

   tkrHistory = tkr.history(period="6mo")

   historyLs = []
   for ind,row in tkrHistory.iterrows():
      historyLs.append(row['Close'])
      # print(row['Close'])

   averageLs = []
   for i in range(1,len(historyLs)):
      averageLs.append(historyLs[i]/historyLs[i-1])
   
   average = statistics.mean(averageLs)
   # print(average)
   
   return average-1

def lowestPointThreeMonth(tkrSymbol):
   '''Passed a symbol, and returns the decimal of the current price
   of the stock at the stock at its lowest lowest point in the past
   three months.'''
   tkr = yf.Ticker(tkrSymbol)

   tkrHistory = tkr.history(period="3mo")

   # How many days ago was this at its lowest point
   lowest = float('Inf')
   daysAgo = 0
   # Keep track of the last day so we can take a percentage
   # and we will know how long ago it was at this point
   lastDay = 0

   for ind,row in tkrHistory.iterrows():
      lastDay = row['Close']
      if row['Close'] < lowest:
         lowest = row['Close']
         daysAgo = 0
      daysAgo += 1
   return (1-(lowest/lastDay), daysAgo)

def lowestPointOneMonth(tkrSymbol):
   '''Passed a symbol, and returns the decimal of the current price
   of the stock at the stock at its lowest lowest point in the past
   one month.'''
   tkr = yf.Ticker(tkrSymbol)

   tkrHistory = tkr.history(period="1mo")

   # How many days ago was this at its lowest point
   lowest = float('Inf')
   daysAgo = 0
   # Keep track of the last day so we can take a percentage
   # and we will know how long ago it was at this point
   lastDay = 0

   for ind,row in tkrHistory.iterrows():
      lastDay = row['Close']
      if row['Close'] < lowest:
         lowest = row['Close']
         daysAgo = 0
      daysAgo += 1
   return (1-(lowest/lastDay), daysAgo)
         
   

def stock_info(tkrSymbol):

   StockInfo.set_one_month(one_month(tkrSymbol))
   StockInfo.set_five_day(five_day(tkrSymbol))
   StockInfo.set_coronavirus(cornavirus(tkrSymbol))
   StockInfo.set_three_m_lp(lowestPointThreeMonth(tkrSymbol))
   StockInfo.set_one_m_lp(lowestPointOneMonth(tkrSymbol))

def find_options():
   tickers = gt.get_tickers_filtered(mktcap_min=mkmin, mktcap_max= mkmax)
   # Holds of the API Calls that have been executed
   amt = 0
   Stock_Failure = 0
   Stocks_Not_Imprted = 0

   collection = {}

   # Iterator
   i = 0
   while(i < len(tickers)) and (amt < 1800):
      try:
         stock = tickers[i]
         collection[str(stock)] = len(options_in_limit(str(stock)))
         time.sleep(2)
         amt+=1
         i+=1
      except ValueError:
         print("Yahoo Finance Backend Error, Fixing...")
         if Stock_Failure > 5:
            i+=1
            Stocks_Not_Imprted += 1
         amt+=1
         Stock_Failure+=1
   print("Amount of stocks successfully imported: " + str(i-Stocks_Not_Imprted))
   return collection

def main():
   '''

   vbiv = options_in_limit('vbiv')
   nvax = options_in_limit('nvax')

   ls = [vbiv,nvax]

   for i in ls:
      print(str(i))

   print(five_day('vbiv'))
   print(one_month('vbiv'))
   print(coronavirus('vbiv'))
   print(lowestPointThreeMonth('vbiv'))
   print(lowestPointOneMonth('vbiv'))

   '''
   find_options()
main()
