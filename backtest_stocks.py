import yfinance as yf
import pandas as pd
import backtrader as bt
import matplotlib.pyplot as plt
from datetime import datetime


class SMAStrategy(bt.Strategy):
    params = (('sma_period', 30),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.sma_period)

    def next(self):
        if self.position.size == 0 and self.data.close[0] > self.sma[0]:
            self.buy()
        elif self.position.size > 0 and self.data.close[0] < self.sma[0]:
            self.sell()


class EMAStrategy(bt.Strategy):
    params = (('ema_period', 30),)

    def __init__(self):
        self.ema = bt.indicators.ExponentialMovingAverage(
            self.data.close, period=self.params.ema_period)

    def next(self):
        if self.position.size == 0 and self.data.close[0] > self.ema[0]:
            self.buy()
        elif self.position.size > 0 and self.data.close[0] < self.ema[0]:
            self.sell()


class MACDStrategy(bt.Strategy):
    params = (('macd1', 12), ('macd2', 26), ('macdsignal', 9))

    def __init__(self):
        self.macd = bt.indicators.MACD(self.data.close,
                                       period_me1=self.params.macd1,
                                       period_me2=self.params.macd2,
                                       period_signal=self.params.macdsignal)

    def next(self):
        if self.position.size == 0 and self.macd.macd[0] > self.macd.signal[0]:
            self.buy()
        elif self.position.size > 0 and self.macd.macd[0] < self.macd.signal[0]:
            self.sell()

def download_data(stock, start, end):
    df = yf.download(stock, start=start, end=end)
    df.index = pd.to_datetime(df.index)
    return df

class EquityCurve(bt.Analyzer):
    def __init__(self):
        self.equity_curve = [self.strategy.broker.getcash()]
        self.dates = []

    def next(self):
        self.equity_curve.append(self.strategy.broker.getvalue())
        self.dates.append(self.strategy.datetime.date())

    def get_analysis(self):
        return self.dates, self.equity_curve

def backtest_strategy(stock_data, strategy):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy)
    cerebro.addanalyzer(EquityCurve, _name='equity_curve')

    data = bt.feeds.PandasData(dataname=stock_data)
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)

    results = cerebro.run()
    dates, equity_curve = results[0].analyzers.equity_curve.get_analysis()
    return dates, equity_curve


if __name__ == '__main__':
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'LPLA', 'IBM']
    strategies = [SMAStrategy, EMAStrategy, MACDStrategy]
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2023, 3, 14)

    # Download the historical data for each stock
    stock_data = {stock: download_data(stock, start_date, end_date) for stock in stocks}

    # Plot the results
    for stock in stocks:
        fig, ax = plt.subplots(figsize=(10, 6))

        for strategy in strategies:
            equity_curve_dates, equity_curve = backtest_strategy(stock_data[stock], strategy)
            ending_value = equity_curve[-1]

            # Ensure the lengths of equity_curve_dates and equity_curve match
            if len(equity_curve_dates) != len(equity_curve):
                min_len = min(len(equity_curve_dates), len(equity_curve))
                equity_curve_dates = equity_curve_dates[:min_len]
                equity_curve = equity_curve[:min_len]

            ax.plot(equity_curve_dates, equity_curve, label=f'{strategy.__name__}: ${ending_value:,.2f}')

        ax.set_xlabel('Date')
        ax.set_ylabel('Total Return')
        ax.set_title(f'Strategy Performance for {stock}')
        ax.legend()

        # Automatically format the x-axis dates
        fig.autofmt_xdate()

        plt.savefig(f'strategy_performance_{stock}.png', dpi=300)