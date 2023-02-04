import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog

NAME = ''


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.search()
        self.Search_button.clicked.connect(self.search)

    def initUi(self):
        uic.loadUi('Интерфейс.ui', self)  # Загружаем дизайн

    def search(self):
        global NAME
        NAME = self.search_lineEdit.text()
        print(NAME)
        self.search_lineEdit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())


print(NAME)