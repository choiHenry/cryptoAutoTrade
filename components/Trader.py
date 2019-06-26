from PyQt5.QtCore import *
import datetime
import pybithumb
import math

class Trader(QThread):
    '''
    Trader uses overly simplified VRB(volatility range breakout) strategy.
    '''

    bought = pyqtSignal(str)
    sold = pyqtSignal(str)
    tick = pyqtSignal(str)

    def __init__(self, bithumb_account, tickers):
        super().__init__()
        self.bithumb_account = bithumb_account
        self.tickers = tickers

    def run(self):

        now = datetime.datetime.now()
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        target_price = self.get_target_price("BTC")
        ma5 = self.get_yesterday_ma5("BTC")

        while True:
            try:
                now = datetime.datetime.now()
                current_price = pybithumb.get_current_price("BTC")

                if mid < now < mid + datetime.timedelta(seconds=10):
                    target_price = self.get_target_price("BTC")
                    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                    ma5 = self.get_yesterday_ma5("BTC")
                    try:
                        order = self.sell_crypto_currency("BTC")
                        self.sold.emit(order)
                    except TypeError:
                        print("Minimum BTC unit required for sale")

                if (current_price > target_price) and (current_price > ma5):
                    order = self.buy_crypto_currency("BTC")

                    try:
                        self.bought.emit(order)
                    except TypeError:
                        print("Not enough money to buy minimum unit of BTC")


            except:
                print("Unknown Error Occurred")

            self.tick.emit(datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
            self.msleep(1000)

    def get_yesterday_ma5(self, ticker):
        '''

        df = pybithumb.get_ohlcv(ticker)
        close = df['close']
        ma = close.rolling(5).mean()
        return ma[-2]

        '''
        return pybithumb.get_ohlcv(ticker)['close'].rolling(5).mean()[-2]


    def get_target_price(self, ticker):
        df = pybithumb.get_ohlcv(ticker)
        yesterday = df.iloc[-2]

        today_open = yesterday['close']
        yesterday_high = yesterday['high']
        yesterday_low = yesterday['low']
        target = today_open + (yesterday_high - yesterday_low) * 0.5
        print(target)
        return target

    def buy_crypto_currency(self, ticker):
        krw = self.bithumb_account.get_balance(ticker)[2]
        orderbook = pybithumb.get_orderbook(ticker)
        sell_price = orderbook['asks'][0]['price']
        unit = krw / float(sell_price)
        funit = math.floor(unit * 10000) / 10000.0
        order = self.bithumb_account.buy_market_order(ticker, funit)
        return order

    def sell_crypto_currency(self, ticker):
        unit = self.bithumb_account.get_balance(ticker)[0]
        funit = math.floor(unit * 10000) / 10000.0
        order = self.bithumb_account.sell_market_order(ticker, funit)
        return order