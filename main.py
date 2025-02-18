import os
import sys

import requests
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [800, 450]



class Example(QWidget):
    ll = [-42.278347,26.703022]
    spn = 0.002
    def __init__(self):
        super().__init__()
        self.initUI()
        self.getImage()


    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'

        # Готовим запрос.

        map_request = f"{server_address}ll={self.ll[0]},{self.ll[1]}&spn={self.spn},{self.spn}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            if self.spn <= 31.948:
                self.spn += 0.05
        if event.key() == Qt.Key.Key_PageDown:
            if self.spn >= 0.052:
                self.spn -= 0.05
        step = 0.01  # Шаг перемещения карты
        if event.key() == Qt.Key.Key_Up:
            self.ll[1] += step
        elif event.key() == Qt.Key.Key_Down:
            self.ll[1] -= step
        elif event.key() == Qt.Key.Key_Left:
            self.ll[0] -= step
        elif event.key() == Qt.Key.Key_Right:
            self.ll[0] += step
        self.ll[0] = max(-180, min(180, self.ll[0]))
        self.ll[1] = max(-90, min(90, self.ll[1]))
        self.getImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())