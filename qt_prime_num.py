# -*- coding: utf-8 -*-
# This Python file uses the following encoding: utf-8
import sys
from prime_num import get_primenum_list_2, is_prime, is_happy_func
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QHBoxLayout
)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont

class NumSmallError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("素数の検証")
        self.setFixedSize(QSize(1080, 700))
        self.widget = QWidget()
        self.layout = QVBoxLayout()

        self.is_happy = False
        self.is_prime = True

        # 最大数と最小数入力画面
        label = QLabel("最小数: ")
        self.layout.addWidget(label)
        self.min_num_edit = QLineEdit()
        self.layout.addWidget(self.min_num_edit)

        label = QLabel("最大数: ")
        self.layout.addWidget(label)
        self.max_num_edit = QLineEdit()
        self.layout.addWidget(self.max_num_edit)
        
        # 平行並
        checkbox_layout = QHBoxLayout()
        # 素数
        self.is_prime_check = QCheckBox("素数？")
        self.is_prime_check.setChecked(self.is_prime)
        self.is_prime_check.clicked.connect(self.toggle_prime)
        checkbox_layout.addWidget(self.is_prime_check)
        
        # ハッピー
        self.is_happy_check = QCheckBox("ハッピー?")
        self.is_happy_check.setChecked(self.is_happy)
        self.is_happy_check.clicked.connect(self.toggle_happy)
        checkbox_layout.addWidget(self.is_happy_check)
        self.layout.addLayout(checkbox_layout)


        # 素数二次元表ボタン
        self.tableOkButton = QPushButton("確定")
        self.tableOkButton.clicked.connect(self.btn_click)
        self.layout.addWidget(self.tableOkButton)

        # 提示
        self.tableMsg = QLabel("")
        self.tableMsg.setStyleSheet("color: black")
        self.layout.addWidget(self.tableMsg)

        # 素数二次元表
        self.tableTitle = QLabel("")
        self.tableTitle.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.tableTitle)
        self.make_table()

        # 素数判定
        label = QLabel("素数判定: ")
        self.layout.addWidget(label)
        self.prime = QLineEdit()
        self.layout.addWidget(self.prime)

        self.judgeOkButton = QPushButton("確定")
        self.judgeOkButton.clicked.connect(self.btn_click2)
        self.layout.addWidget(self.judgeOkButton)

        self.judgeMsg = QLabel("")
        self.judgeMsg.setStyleSheet("color: black")
        self.layout.addWidget(self.judgeMsg)


        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)





#        # set dialog layout
#        self.setLayout(layout)
#        self.button.clicked.connect(self.greeting)
        # 最大数と最小数入力画面
#        self.label = QLabel("最小数: ")
#        self.layout.addWidget(self.label)
#        self.min_num_edit = QLineEdit("min num")
#        self.layout.addWidget(self.min_num_edit)
#        self.label = QLabel("最大数: ")
#        self.layout.addWidget(self.label)
#        self.max_num_edit = QLineEdit("max num")
#        self.layout.addWidget(self.max_num_edit)

#        # 確定ボタン
#        self.tableOkButton = QPushButton("確定")
#        self.layout.addWidget(self.tableOkButton)

#        self.setLayout(self.layout)

    # def the_button_was_clicked(self):
    #     print("Clicked!")

    # def the_button_was_toggled(self, checked):
    #     self.button_is_checked = checked
    #     print(self.button_is_checked)

    def make_table(self):
        column = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        self.table = QTableWidget()
        self.table.setColumnCount(len(column))
        self.table.setHorizontalHeaderLabels(column)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table)


    def btn_click(self):
        self.table.clear()
        column = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        self.table.setColumnCount(len(column))
        self.table.setHorizontalHeaderLabels(column)
        
        if self.is_happy and self.is_prime:
            self.tableTitle.setText("ハッピー素数表")
        elif self.is_prime:
            self.tableTitle.setText("素数表")
        
        elif self.is_happy:
            self.tableTitle.setText("ハッピー表")
        min_num = self.min_num_edit.text()
        max_num = self.max_num_edit.text()
        try:
            max_num = int(max_num)
            min_num = int(min_num)
            if min_num > max_num:
                raise(NumSmallError)
            self.tableMsg.setText("")
            if max_num < 7:
                self.tableMsg.setText("7から計算する")

            self.tableMsg.setStyleSheet("color: black")

            prime_list, prime_dict = get_primenum_list_2(max_num, min_num, self.is_happy, self.is_prime)
            count = min_num // 10
            row_count = max_num // 10
            self.table.setRowCount(row_count - count)
#            self.table.setItem(count,0,QTableWidgetItem(str(count)))
            while count <= max_num:
                self.table.setVerticalHeaderItem(count - min_num // 10, QTableWidgetItem(str(count)))
                # self.table.setItem(count - min_num // 10,0,QTableWidgetItem(str(count)))
                if prime_dict.get(str(count)):
                    count_2 = 0
                    for col in prime_dict[str(count)]:
                        self.table.setItem(count - min_num // 10,count_2, QTableWidgetItem(str(col))
                        )
                        count_2 += 1

                count += 1
        except ValueError:
            self.tableMsg.setText("自然数しか受けない")
            self.tableMsg.setStyleSheet("color: red")
        except NumSmallError:
            self.tableMsg.setText("受けた最小数は最大数より大きい")
            self.tableMsg.setStyleSheet("color: red")


    def toggle_happy(self, check):
        self.is_happy = check
        self.is_happy_check.setChecked(self.is_happy)
        
    def toggle_prime(self, check):
        self.is_prime = check
        self.is_prime_check.setChecked(self.is_prime)

    def btn_click2(self):
        prime_num = self.prime.text()
        try:
            prime_num = int(prime_num)
            result, divitor = is_prime(prime_num)
            happy = is_happy_func(prime_num)
            if result:
                self.judgeMsg.setText("素数")
                if happy:
                    self.judgeMsg.setText("素数且つハッピー素数")
            else:
                self.judgeMsg.setText(f"素数ではない、少なくとも{divitor}に割れる")
                if happy:
                    self.judgeMsg.setText(f"素数ではない、少なくとも{divitor}に割れる、ハッピー数")
            self.judgeMsg.setStyleSheet("color: black")
        except ValueError:
            self.judgeMsg.setText(f"数字ではない")
            self.judgeMsg.setStyleSheet("color: red")











if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QTableWidgets{background-color: black; color: white}")
#    label = QLabel("<font color=red size=40>Hello World!</font>")
#    label.show()
    window = MainWindow()
    window.show()

    app.exec()
