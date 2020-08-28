# Important Stock Market Data

# Parameters I want to work with

MAXPRICE = 20
OPENINTEREST = 40
INTHEMONEY = True

import yfinance as yf

# Imorting Date/Time

import datetime

tkr = yf.Ticker('vbiv')

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
print(holder_date)

# Iterate Over This df
tkrDf = tkr.option_chain(holder_date).calls

tkrDf.head()

# Potential Options We're Interested in Buying
potential_buy = {}

for ind,row in tkrDf.iterrows():
   if (row['inTheMoney'] == INTHEMONEY):
      # If we are in the money
      if (row['openInterest'] > OPENINTEREST):  
         if (row['lastPrice'] < MAXPRICE):

            # Gettin ticker symbol from contract symbol
            count = 0
            for i in row['contractSymbol']:
               if i.isalpha():
                  count+=1
               else:
                   break

            # Adding to the record
            try:
               potential_buy[row['contractSymbol'][0:count]].append(row['lastPrice'])
               sort(potential_buy['contractSymbol'][0:count])
            except:
               potential_buy[row['contractSymbol'][0:count]] = [row['lastPrice']]


for key in potential_buy:
   yf.download(key,'2020-02-19',today)


            
print(potential_buy)
