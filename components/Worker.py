from PyQt5.QtCore import *
import pybithumb


class Worker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, bithumb_account, tickers):
        super().__init__()
        self.bithumb_account = bithumb_account
        self.tickers = tickers

    def run(self):
        while True:
            data = {}

            for ticker in self.tickers:
                data[ticker] = self.get_market_infos(ticker)

            self.finished.emit(data)
            self.msleep(500)

    def get_market_infos(self, ticker):
        try:

            df = pybithumb.get_ohlcv(ticker)
            ma5 = df['close'].rolling(window=5).mean()

            price = pybithumb.get_current_price(ticker)
            balance = self.bithumb_account.get_balance(ticker)
            last_ma5 = ma5[-2]

            state = None
            if price > last_ma5:
                state = "Ascending"
            else:
                state = "Descending"

            return (price, last_ma5, state, balance)

        except:
            return (None, None, None, None)