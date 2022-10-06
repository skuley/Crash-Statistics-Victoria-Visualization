import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
import pandas as pd
from tqdm import tqdm

widget_ui = uic.loadUiType("ui/progressbar.ui")[0]

df = pd.read_csv('../외주/Crash Statistics Victoria.csv')
crash_dates = sorted(list(set(df.ACCIDENT_DATE.tolist())))

class ProgressBar(QWidget, widget_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Crash Satistics Victoria")
        self.progressBar.setValue(0)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    progressbar_widget = ProgressBar()
    progressbar_widget.show()
    date_dict = {}
    for idx, date in enumerate((crash_dates)):
        date_dict[date] = df[df.ACCIDENT_DATE == date]
        progressbar_widget.progressBar.setValue(idx)
    sys.exit(app.exec_())