from PyQt5 import QtGui, QtWidgets
import sys
from ProcessFW import parsing_fw, save_changes_to_file


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.horizontalLayout.addWidget(self.label)
        self.changes_text = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.horizontalLayout.addWidget(self.changes_text)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.label_2)
        self.version_text = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.version_text)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.start_button)
        self.start_nop_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.start_nop_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.res_success = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.horizontalLayout_4.addWidget(self.res_success)
        self.res_success_nop = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.horizontalLayout_4.addWidget(self.res_success_nop)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.res_faul = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.horizontalLayout_6.addWidget(self.res_faul)
        self.res_faul_nop = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.horizontalLayout_6.addWidget(self.res_faul_nop)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.add_changes = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.horizontalLayout_5.addWidget(self.add_changes)
        self.res_add_changes = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.horizontalLayout_5.addWidget(self.res_add_changes)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.setCentralWidget(self.verticalLayoutWidget)
        self.init_text()

        self.start_button.clicked.connect(self.start_btn_even)
        self.start_nop_button.clicked.connect(self.start_btn_even_nop)
        self.add_changes.clicked.connect(self.add_changes_event)

    def init_text(self):
        self.setWindowTitle("Формирование DevLog")
        self.label.setText("Изменения")
        self.label_2.setText("Версия      ")
        self.start_button.setText("Старт")
        self.start_nop_button.setText("Старт NOP")
        self.res_success.setText("Обработано прошивок: 0")
        self.res_success_nop.setText("Обработано прошивок: 0")
        self.res_faul.setText("Пропущено прошивок: 0")
        self.res_faul_nop.setText("Пропущено прошивок: 0")
        self.add_changes.setText("Добавить изменения в файл")
        self.res_add_changes.setText("")

    def start_btn_even(self):
        success, fault = parsing_fw(
            self.version_text.text(), self.changes_text.toPlainText()
        )
        self.res_success.setText(f"Обработано прошивок: {success}")
        self.res_faul.setText(f"Пропущено прошивок: {fault}")

    def start_btn_even_nop(self):
        success, fault = parsing_fw(
            self.version_text.text(), self.changes_text.toPlainText(), is_nop=True
        )
        self.res_success_nop.setText(f"Обработано прошивок: {success}")
        self.res_faul_nop.setText(f"Пропущено прошивок: {fault}")

    def add_changes_event(self):
        save_changes_to_file(self.version_text.text(), self.changes_text.toPlainText())
        self.res_add_changes.setText("Готово!!!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
