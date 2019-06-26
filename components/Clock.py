from PyQt5.QtCore import *


class Clock(QThread):
    tick = pyqtSignal(str)

    def run(self):
        while True:

            cur_time = QTime.currentTime()
            str_time = cur_time.toString("hh:mm:ss")

            self.tick.emit(str_time)
            self.msleep(1000)
