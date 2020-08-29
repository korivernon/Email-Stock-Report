# Email-Stock-Report

Currently, this is configured to send you an email of the highest OBV movers and the lowest OBV movers. 

# Made this to find potential stocks to invest in *Using OBV Analysis*

If you want to get this running on your computer, first input your email at the bottom of the file. If you are using Gmail, you may have to enable [this](https://myaccount.google.com/lesssecureapps?pli=1).

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
## Options Analysis

In the future, I plan on implemeting this in order to help me achieve my goal of making an average of *+16%* per week trading options. 

I'm getting an issue when it comes to finding Options to analyze based on ```get-all-tickers```. It is throwing an error and this is something that some people have run into. 

Below is the error:

```out
Traceback (most recent call last):
  File "/Users/trapbookpro/Documents/Computer Science/Projects/Email-Stock-Report/experimenting.py", line 289, in <module>
    main()
  File "/Users/trapbookpro/Documents/Computer Science/Projects/Email-Stock-Report/experimenting.py", line 288, in main
    find_options()
  File "/Users/trapbookpro/Documents/Computer Science/Projects/Email-Stock-Report/experimenting.py", line 256, in find_options
    collection[str(stock)] = len(options_in_limit(str(stock)))
  File "/Users/trapbookpro/Documents/Computer Science/Projects/Email-Stock-Report/experimenting.py", line 72, in options_in_limit
    for i in tkr.options:
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/yfinance/ticker.py", line 195, in options
    self._download_options()
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/yfinance/ticker.py", line 61, in _download_options
    return r['optionChain']['result'][0]['options'][0]
IndexError: list index out of range
```
I've seen this issue before [here](https://aroussi.com/post/download-options-data)
