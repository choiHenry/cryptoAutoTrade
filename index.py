import sys
from PyQt5.QtWidgets import *
import pybithumb
from components.MyWindow import MyWindow

# TICKERS LIST
tickers = ["BTC", "ETH", "BCH", "ETC"]

#BITHUMB API KEY SETTINGS
f = open('src/bithumb_api_key.txt')
lines = f.readlines()
con_key = lines[3].strip()                          #assign bithumb connect key to con_key variable
sec_key = lines[6].strip()                          #assign bithumb secret key to sec_key variable
bithumb_account = pybithumb.Bithumb(con_key, sec_key)

app = QApplication(sys.argv)
win = MyWindow(tickers, bithumb_account)
win.show()
app.exec_()