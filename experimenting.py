import yfinance as yf

# Importing Date/Time

import datetime

# Important Stock Market Data

# Parameters I want to work with

MAXPRICE = 20
OPENINTEREST = 40
INTHEMONEY = True

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
      self.three_day = 0
      self.three_m_lp = 0
      self.one_m_lp = 0
   def set_one_month(self, m):
      self.one_month = m
   def set_three_day(self, d):
      self.three_day = d
   def set_corona(self, c):
      self.corona = c
   def set_three_m_lp(self,tmlp):
      self.three_m_lp = tmlp
   def set_one_m_lp(self, omlp):
      self.one_m_lp = omlp
      

def options_in_limit(name):
   tkr = yf.Ticker(name)

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

def three_day(tkrSymbol):
   '''Passed a symbol, and returns the decimal the stock has moved in
      the past three trading days.'''
   pass

def one_month(tkrSymbol):
   '''Passed a symbol, and returns the decimal the stock has moved in
      the past one month.'''
   pass

def coronavirus(tkrSymbol):
   '''Passed a symbol, and returns the decimal the stock has moved
      since coronavirus pandemic began affecting the stock market.'''
   pass

def lowestPointThreeMonthPercentage(tkrSymbol):
   '''Passed a symbol, and returns the decimal of the current price
   of the stock at the stock at its lowest lowest point in the past
   three months.'''
   pass



def main():

   vbiv = options_in_limit('vbiv')
   nvax = options_in_limit('nvax')

   ls = [vbiv,nvax]

   for i in ls:
      print(str(i))
main()
