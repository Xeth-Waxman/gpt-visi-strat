# gpt-visi-strat
Continuing our exploration of ChatGPT's ability to generate code, this time by creating a trading application that uses multiple strategies, and statistical visualization. We'll be using the recently released ChatGPT-4. ChatGPT-4 comes with a limit of 100 responses every 4 hours, and the responses are much slower than the 3.5 model; the combination of a more sophisticated application, a response limit, and slower responses may mean this project takes substantially longer to complete than previous projects that used the 3.5 model.

__Initial Prompt:__
> Write a python application that takes in a list of stocks, then conducts backtesting of those stocks against several different well-known trading strategies using historical end of day data from yahoo finance's APIs. After completing the backtesting, generate a graph of the strategies performance over time.

__what you'll need to pip:__
pip install pandas yfinance numpy matplotlib backtrader