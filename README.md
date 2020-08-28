# Email-Stock-Report

Currently, this is configured to send you an email of the highest OBV movers and the lowest OBV movers. 

# Made this to find potential stocks to invest in *Using OBV Analysis*

If you want to get this running on your computer, first input your email at the bottom of the file. If you are using Gmail, you may have to enable[this](https://myaccount.google.com/lesssecureapps?pli=1).

In your terminal, copy and paste this:

```out
pip3 install yfinance
pip3 install pandas
pip3 install numpy
pip3 install get-all-tickers
```

If you are on Windows and not Mac, I believe you need to install everything manually (or work in a VM). Take a look at this [article](https://medium.com/automated-trading/a-guide-to-automating-your-stock-analysis-with-python-4b6929e54201)-- it may help. 



Changes coming in the future:

I invest in Stock Options, specifically buying Calls. I only want the stock to move up *~+2%*.

In order to identify these stocks, I manually perform this algorithm to look for potential buys. I want to automate this to make my life easier. 

Here is the general algorithm:

```out
curr =Look at current stock price

if curr < 25: 
  # continue we are interested in investing
  
  lowPt = Look 195 days in the past (coronavirus devastated the market)
  highPt = Look 230 days in the past (market was doing very well)

  if curr > lowPt and curr < highPt:
  # look at this stock because it has recovered and it has potential
  # if it has had a downward trend in ONLY the past three days - I think it's going to go back up

  run OBV analysis


# pack up and send email
```

In the future, I plan on implemeting this in order to help me achieve my goal of making an average of *+16%* per week trading options. 
