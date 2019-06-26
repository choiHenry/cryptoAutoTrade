from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from components.Worker import Worker
from components.Trader import Trader
from components.Clock import Clock
from PyQt5 import uic

# make 'MyWindow.ui' file using QT DESIGNER and load it
form_class = uic.loadUiType("src/MyWindow.ui")[0]

class MyWindow(QMainWindow, form_class):

    def __init__(self, tickers, bithumb_account):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("src/its_me.jpeg"))

        self.tickers = tickers
        self.bithumb_account = bithumb_account

        self.tableWidget.setRowCount(len(self.tickers)+1)
        self.worker = Worker(bithumb_account, tickers)
        self.worker.finished.connect(self.update_table_widget)
        self.worker.start()

        self.clock = Clock()
        self.clock.tick.connect(self.update_time)
        self.clock.start()

        self.trader = Trader(bithumb_account, tickers)
        self.trader.sold.connect(self.srecord)
        self.trader.bought.connect(self.brecord)
        self.trader.tick.connect(self.printTime)
        self.trader.start()

    @pyqtSlot(dict)
    def update_table_widget(self, data):
        try:
            for ticker, infos in data.items():

                index = self.tickers.index(ticker)

                self.tableWidget.setItem(index, 0, QTableWidgetItem(ticker))
                self.tableWidget.setItem(index, 1, QTableWidgetItem(str(infos[0])))
                self.tableWidget.setItem(index, 2, QTableWidgetItem(str(infos[1])))
                self.tableWidget.setItem(index, 3, QTableWidgetItem(str(infos[2])))
                self.tableWidget.setItem(index, 4, QTableWidgetItem(str(infos[3][0])))

                if index + 1 == len(self.tickers):
                    self.tableWidget.setItem(4, 0, QTableWidgetItem("KRW"))
                    self.tableWidget.setItem(4, 4, QTableWidgetItem(str(infos[3][2])))


        except:
            pass

    @pyqtSlot(str)
    def update_time(self, str_time):
        try:
            self.statusBar().showMessage(str_time)
        except:
            pass

    @pyqtSlot(str)
    def srecord(self, orderId):
        try:
            print("Sold BTC | Order ID: ", orderId)
        except:
            pass

    @pyqtSlot(str)
    def brecord(self, orderId):
        try:
            print("Bought BTC | Order ID: ", orderId)
        except:
            pass

    @pyqtSlot(str)
    def printTime(self, timestampStr):
        print(timestampStr)