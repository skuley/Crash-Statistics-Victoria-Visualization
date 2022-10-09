import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout
from PyQt5.QtCore import QDate
import pandas as pd
from progressbar import DatasetCounting
# from dataset_counting import DatasetCounting
import matplotlib
matplotlib.use('qtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

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
        self.prev = None
        self.count = 0

        self.time_btn.clicked.connect(lambda :self.show_chart("hours"))
        self.crash_type_btn.clicked.connect(lambda :self.show_chart("crash_type"))
        self.road_user_type_btn.clicked.connect(lambda :self.show_chart("road_user_type"))
        self.location_btn.clicked.connect(lambda :self.show_chart("locations"))
        self.obj_hit_btn.clicked.connect(lambda :self.show_chart("obj_hit"))
        self.conditions_btn.clicked.connect(lambda :self.show_chart('conditions'))

        self.figure, (self.ax1, self.ax2) = plt.subplots(2,1)
        self.canvas = FigureCanvasQTAgg(self.figure.axes[0].figure)
        self.verticalLayout_5.addWidget(self.canvas)


    def load_dataset(self):
        # TODO: csv file directory
        self.categories = DatasetCounting('db/Crash Statistics Victoria.csv')
        self.categories.load_categories()
        crash_dates = list(self.categories.crashed_dates.keys())

        # -----------------------------------------------------------------------------
        # import json
        # with open('test_db.json', 'r') as file:
        #     data = file.read()
        # self.crash_dates = json.loads(data)
        # crash_dates = list(self.crash_dates.keys())
        # -----------------------------------------------------------------------------

        minimum_date = crash_dates[0].split('/')
        maximum_date = crash_dates[-1].split('/')
        self.minimum_date = QDate(int(minimum_date[2]), int(minimum_date[1]), int(minimum_date[0]))
        self.maximum_date = QDate(int(maximum_date[2]), int(maximum_date[1]), int(maximum_date[0]))

    def get_date(self, date):
        year, month, day = date.getDate()
        # self.day_of_week = day_of_week(date.dayOfWeek())
        # self.date = f'{year}/{month}/{day}'
        self.date = f'{day}/{month}/{year}'
        self.count = 0
        self.prev = None


    def show_chart(self, btn_type):
        if self.date is None:
            QMessageBox.warning(self, "Alert", "select date first")
        else:
            graph_data = self.crash_dates[self.date][btn_type]
            self.ax1.clear()
            self.ax2.clear()
            if btn_type == 'hours':
                if self.prev == None:
                    self.prev = btn_type
                x, y = list(graph_data.keys()), list(graph_data.values())
            else:
                if self.prev == btn_type:
                    self.count += 1
                else:
                    self.prev = btn_type
                    self.count = 0
                length = len(graph_data.keys()) - 1
                if self.count > length:
                    self.count = 0
                data = graph_data[list(graph_data.keys())[self.count]]
                print(data.keys())
                x, y = list(data.keys()), list(data.values())

            self.plot_canvas(x, y, btn_type)


    def plot_canvas(self, key, values, btn_type):
        self.ax1.set_title(btn_type)
        self.ax1.bar(key, values, color='red', width=0.5)
        total = sum(values)
        self.ax2.pie([value/total for value in values])
        # plt.plot(values)


        self.canvas.draw()
        # self.canvas2.draw()

    def create_bar(self):
        self.chart_page.set



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())