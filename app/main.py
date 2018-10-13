from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QErrorMessage, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QAbstractItemView
from distraction_detector import start_detection

import sys
import sqlite3
import time, datetime
import threading

# files
db_file = "database.db"




def show_error(message, e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message)
    msg.setInformativeText(str(e))
    msg.setWindowTitle("Message")
    msg.exec_()


def show_message(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle("Message")
    msg.exec_()


# define UI layout
class ProductivityMonitor(QDialog):
    def __init__(self):
        super(ProductivityMonitor, self).__init__()
        loadUi('../GUI/main.ui', self)

        # counters
        self.focus = 0.0
        self.distracted = 0.0
        self.date = str(datetime.date.today())
        self.percentage = 0

        # button definition
        self.test.clicked.connect(self.test_func)
        self.start.clicked.connect(self.start_func)
        self.clear.clicked.connect(self.clear_data_func)
        self.stop.clicked.connect(self.stop_func)

        # table
        self.tableWidget = QTableWidget()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        # set row count
        self.tableWidget.setRowCount(1)

        # set column count
        self.tableWidget.setColumnCount(4)

        self.update_table()

        self.check_status = False

    def update_table(self):
        try:
            con = sqlite3.connect(db_file)
            cursor = con.execute("SELECT * from ProdMonitor")
            data = [i for i in cursor]
            self.tableWidget.setRowCount(len(data))
            for i in range(0, len(data)):
                # iterate over four columns
                for j in range(0, 4):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))
            con.close()

        except Exception as e:
            show_error("Database error!!!", str(e))
        self.layout.addWidget(self.tableWidget)
        self.show()

    def test_func(self):
        start_detection("test", self)

    def clear_data_func(self):
        try:
            clear_conn = sqlite3.connect(db_file)
            sql = 'DELETE FROM ProdMonitor'
            cur = clear_conn.cursor()
            cur.execute(sql)
            clear_conn.commit()
            clear_conn.close()
            show_message("Successfully deleted data.")
            self.update_table()
        except Exception as e:
            show_error("Database error!!!", e)
        pass

    def record(self):
        while True:
            if self.check_status is False:
                break
            start_detection("run", self)

    def start_func(self):
        if not self.check_status:
            self.test.setEnabled(False)
            self.clear.setEnabled(False)
            self.check_status = True
            show_message("Remember to click on STOP to save data.")
            th = threading.Thread(target=self.record)
            th.daemon = True
            th.start()

    def stop_func(self):
        if self.check_status:
            self.test.setEnabled(True)
            self.clear.setEnabled(True)
            self.check_status = False
            add_conn = sqlite3.connect(db_file)
            add_cur = add_conn.cursor()
            try:
                data = add_cur.execute("SELECT * FROM ProdMonitor WHERE date='" + str(self.date) + "'")
                if len([i for i in data]) == 0:
                    add_cur.execute("INSERT INTO ProdMonitor(date, focus, distracted, percentage) VALUES('" +
                            str(self.date) + "','" + str(self.focus) + "','" + str(self.distracted) + "','" + str(self.percentage) + "')")
                else:
                    add_cur.execute("UPDATE ProdMonitor set focus='" + str(self.focus) + "',distracted='" + str(self.distracted) +
                                    "',percentage='" + str(self.percentage) + "' WHERE date='" + str(self.date) + "'")
                add_conn.commit()
            except Exception as e:
                show_error("Database error!!!", e)
            add_conn.close()
            self.update_table()


# start app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProductivityMonitor()
    try:
        conn = sqlite3.connect(db_file)
        conn.close()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        show_error("Database error!!!\n\n", str(e))



