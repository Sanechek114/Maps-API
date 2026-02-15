import os
import sys

import requests

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtGui import QPixmap

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

SCREEN_SIZE = [620, 600]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.z = 5
        self.x = 0
        self.y = 0
        self.themes = ["light", "dark"]
        self.theme = self.themes[0]
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        # Готовим запрос.
        if self.z >= 21:
            self.z = 2
        if self.z <= 1:
            self.z = 20
        if self.y <= -80:
            self.y = 80
        if self.y >= 90:
            self.y = -70
        if self.x <= -180:
            self.x = 180
        if self.x >= 180:
            self.x = -180

        map_params = {
            "ll": ",".join([str(self.x), str(self.y)]),
            "z": self.z,
            "apikey": api_key,
            "theme": self.theme
        }

        response = requests.get(server_address, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setFixedSize(*SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        # Изображение
        uic.loadUi('dizine.ui', self)
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)

        self.light.clicked.connect(self.light_theme)
        self.dark.clicked.connect(self.dark_theme)

    def light_theme(self):
        self.theme = self.themes[0]
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)

    def dark_theme(self):
        self.theme = self.themes[1]
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        os.remove(self.map_file)
        if event.key() == Qt.Key.Key_PageUp:
            self.z += 1
        elif event.key() == Qt.Key.Key_PageDown:
            self.z -= 1
        elif event.key() == Qt.Key.Key_Left:
            self.x -= 10
        elif event.key() == Qt.Key.Key_Right:
            self.x += 10
        elif event.key() == Qt.Key.Key_Up:
            self.y += 10
        elif event.key() == Qt.Key.Key_Down:
            self.y -= 10
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
