import yfinance as yf, pandas as pd, shutil, os, time, glob, smtplib, ssl
from get_all_tickers import get_tickers as gt

# Define Market Cap
mkmin = 150000
mkmax = 10000000
trading_days = 10

tickers = gt.get_tickers_filtered(mktcap_min=mkmin, mktcap_max= mkmax)

# Check that the that we are not targeting more than 2000 tickers because YFinance API has 2000 calls per hour limit
shutil.rmtree('<PATH ON COMPUTER>/Daily_Stock_Reports/Stocks')
os.mkdir('<PATH ON COMPUTER>/Daily_Stock_Reports/Stocks')
# Holds of the API Calls that have been executed
amt = 0
Stock_Failure = 0
Stocks_Not_Imprted = 0

i = 0
while (i < len(tickers)) and (amt < 1800):
    try:
        stock = tickers[i]
        temp = yf.Ticker(str(stock))
        Hist_data = temp.history(period="max")
        Hist_data.to_csv('<PATH ON YOUR COMPUTER>/Daily_Stock_Report/Stocks/'+stock+'.csv')
        time.sleep(2) #this payses the loop for 2 seconds so no issues are caused
        amt+=1
        Stock_Failure = 0
        i+=1
    except ValueError:
        print("Yahoo Finance Backend Error, Fixing...")
        if Stock_Failure > 5:
            i+=1
            Stocks_Not_Imprted += 1
        amt+=1
        Stock_Failure+=1
print("Amount of stocks successfully imported: " + str(i-Stocks_Not_Imprted))

# On-Balance Volume Analysis - Using Volume flow to predict changes in Stock Price
list_files = (glob.glob('<PATH ON COMPUTER>/Daily_Stock_Report/Stocks/*csv'))
new_data = []
interval = 0
while interval < len(list_files):
    Data = pd.read_csv(list_files[interval]).tail(trading_days) #gets the last x days of trading
    pos_move = []
    neg_move = []
    OBV_Value = 0
    count = 0
    while (count < trading_days): #because we're looking at the last x trading days
        if Data.iloc[count, 1] < Data.iloc[count, 4]:
            pos_move.append(count)
        elif Data.iloc[count, 1] > Data.iloc[count, 4]:
            neg_move.append(count)
        count+=1
    count2 = 0
    for i in pos_move:
        OBV_Value = round(OBV_Value + (Data.iloc[i,5]/Data.iloc[i,1]))
    for i in neg_move:
        OBV_Value = round (OBV_Value - (Data.iloc[i,5]/Data.iloc[i,1]))
    Stock_Name = ((os.path.basename(list_files[interval])).split(".csv")[0]) # Get the name of the current stock that we are analyzing
    new_data.append([Stock_Name, OBV_Value])
    interval+=1
df = pd.DataFrame(new_data, columns = ['Stock', 'OBV_Value']) #This creates a new dataframe for the new data
df["Stocks_Ranked"] = df["OBV_Value"].rank(ascending = False) #Rank by OBV Values
df.sort_values("OBV_Value", inplace = True, ascending = False) #Sort by OBV Values
df.to_csv('<PATH ON COMPUTER>/Daily_Stock_Report/OBV_Ranked.csv', index = False)
Analysis = pd.read_csv('<PATH ON COMPUTER>/Daily_Stock_Report/OBV_Ranked.csv')

top = Analysis.head(trading_days)
bottom = Analysis.tail(trading_days)

Email_Body = """\
Subject: Daily Stonk Report

Your highest ranked On-Balance Volume stocks of the day:

""" + top.to_string(index=False) +"""\

Your lowest ranked On-Balance Volume stocks of the day:


""" + bottom.to_string(index=False) + """\

Trust your intuition,
Python"""
context = ssl.create_default_context()
Email_Port = 465
with smtplib.SMTP_SSL("smtp.gmail.com", Email_Port, context=context) as server:
    server.login("<YOUR EMAIL>", "<YOUR EMAIL PASSWORD>")
    server.sendmail("<YOUR EMAIL>", "<YOUR EMAIL>",Email_Body )

