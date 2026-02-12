import os
import sys

import requests
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.z = 5
        self.x = 0
        self.y = 0
        uic.loadUi('dizine.ui', self)
        self.getImage()
        self.run()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
        # Готовим запрос.
        self.text = self.lineEdit.text()
        if not self.text:
            self.text = "Берлин"
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
        map_response = requests.get(
            f'http://geocode-maps.yandex.ru/1.x/?apikey=8013b162-6b42-4997-9691-77b7074026e0&geocode={self.text}&format=json')
        json_response = map_response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        map_request = f"{server_address}ll={toponym_coodrinates.split()[0]},{toponym_coodrinates.split()[1]}&apikey={api_key}&z={10}"
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

    def run(self):
        self.setWindowTitle('Отображение карты')
        ## Изображение
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
