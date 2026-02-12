import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.coords = [37.530887, 55.703118]
        self.spn = 0.002
        self.themes = ["light", "dark"]
        self.theme = self.themes[0]
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = 'll=37.530887,55.703118&spn=0.002,0.002'
        # Готовим запрос.

        map_params = {
            "ll": ",".join([str(self.coords[0]), str(self.coords[1])]),
            "spn": ",".join([str(self.spn), str(self.spn)]),
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
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageDown:
            pass
        if event.key() == Qt.Key.Key_PageUp:
            pass
        if event.key() == Qt.Key.Key_Up:
            self.coords[1] += 100 * self.spn
        
        if event.key() == Qt.Key.Key_Down:
            self.coords[1] -= 10 * self.spn
        
        if event.key() == Qt.Key.Key_Left:
            self.coords[0] -= 10 * self.spn
        
        if event.key() == Qt.Key.Key_Right:
            self.coords[1] += 10 * self.spn
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
    
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())