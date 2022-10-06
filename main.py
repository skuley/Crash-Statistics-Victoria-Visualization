import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QDate
import pandas as pd
from progressbar import ProgressBar

form_class = uic.loadUiType("ui/Crash.ui")[0]


def day_of_week(index):
    if index == 0:
        return 'Sunday'
    elif index == 1:
        return 'Monday'
    elif index == 2:
        return 'Tuesday'
    elif index == 3:
        return 'Wednesday'
    elif index == 4:
        return 'Thursday'
    elif index == 5:
        return 'Friday'
    elif index == 6:
        return 'Saturday'

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Crash Satistics Victoria")
        self.load_dataset()
        self.calendarWidget.setMinimumDate(self.minimum_date)
        self.calendarWidget.setMaximumDate(self.maximum_date)

        self.calendarWidget.clicked.connect(self.get_date)
        self.date = None

        self.time_btn.clicked.connect(lambda :self.show_chart("time"))
        self.crash_type_btn.clicked.connect(lambda :self.show_chart("crash_type"))
        self.road_user_type_btn.clicked.connect(lambda :self.show_chart("road_user_type"))
        self.location_btn.clicked.connect(lambda :self.show_chart("location"))
        self.obj_hit_btn.clicked.connect(lambda :self.show_chart("obj_hit"))
        self.conditions_btn.clicked.connect(lambda :self.show_chart('conditions'))


    def load_dataset(self):
        df = pd.read_csv('../외주/Crash Statistics Victoria.csv')
        crash_dates = sorted(list(set(df.ACCIDENT_DATE.tolist())))
        progressbar_widget = ProgressBar()
        progressbar_widget.show()
        date_dict = {}
        for idx, date in enumerate((crash_dates)):
            date_dict[date] = df[df.ACCIDENT_DATE == date]
            progressbar_widget.progressBar.setValue(idx)
        progressbar_widget.close()

        minimum_date = crash_dates[0].split('/')
        maximum_date = crash_dates[-1].split('/')
        self.minimum_date = QDate(int(minimum_date[2]), int(minimum_date[1]), int(minimum_date[0]))
        self.maximum_date = QDate(int(maximum_date[2]), int(maximum_date[1]), int(maximum_date[0]))

    def get_date(self, date):
        year, month, day = date.getDate()
        self.day_of_week = day_of_week(date.dayOfWeek())
        self.date = f'{year}/{month}/{day}'

    def show_chart(self, btn_type):
        if self.date is None:
            QMessageBox.warning(self, "Alert", "select date first")
        else:
            print(btn_type)
            chart_page = self.chart_page
            chart_page.setText(btn_type)
            # if btn_type == 'time':
            #     chart_page
            # elif btn_type =='crash_type':
            #     print()
            # elif btn_type == 'road_user_type':
            #     print()
            # elif btn_type == 'location':
            #     print()
            # elif btn_type == 'obj_hit':
            #     print()
            # elif btn_type == 'conditions':
            #     print()

    def create_bar(self):
        self.chart_page.set



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())