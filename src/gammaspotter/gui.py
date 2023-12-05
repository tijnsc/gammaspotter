import sys

from PySide6 import QtWidgets
import pyqtgraph as pg
import pandas as pd

from PySide6.QtCore import Slot


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        hbox_main = QtWidgets.QHBoxLayout(central_widget)
        self.plot_widget = pg.PlotWidget()
        hbox_main.addWidget(self.plot_widget)

        vbox_menu = QtWidgets.QVBoxLayout()
        hbox_main.addLayout(vbox_menu)

        form = QtWidgets.QFormLayout()
        vbox_menu.addLayout(form)

        open_btn = QtWidgets.QPushButton("Open Measurement")
        form.addRow(open_btn)

        open_btn.clicked.connect(self.open_file)

    @Slot()
    def open_file(self):
        # filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if filename:
            self.opened_file = pd.read_csv(filename)
            self.energy = self.opened_file.iloc[:, 0]
            self.counts = self.opened_file.iloc[:, 1]
            self.plot()

    def plot(self):
        self.plot_widget.plot(
            x=self.energy, y=self.counts, symbol=None, pen={"color": "w", "width": 5}
        )
        self.plot_widget.setLabel("left", "Counts")
        self.plot_widget.setLabel("bottom", "Energy")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
