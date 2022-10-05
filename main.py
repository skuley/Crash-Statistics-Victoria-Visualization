import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDate
import pandas as pd

form_class = uic.loadUiType("ui/Crash.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Crash Satistics Victoria")
        self.load_dataset()
        self.calendarWidget.setMinimumDate(self.minimum_date)
        self.calendarWidget.setMaximumDate(self.maximum_date)

        self.calendarWidget.clicked.connect(self.get_date)

    def load_dataset(self):
        df = pd.read_csv('../외주/Crash Statistics Victoria.csv')
        crash_dates = sorted(list(set(df.ACCIDENT_DATE.tolist())))
        minimum_date = crash_dates[0].split('/')
        maximum_date = crash_dates[-1].split('/')
        self.minimum_date = QDate(int(minimum_date[2]), int(minimum_date[1]), int(minimum_date[0]))
        self.maximum_date = QDate(int(maximum_date[2]), int(maximum_date[1]), int(maximum_date[0]))


    def get_date(self, date):
        year, month, day = date.getDate()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())