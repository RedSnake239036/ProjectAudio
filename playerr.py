import sys
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QTextEdit,
                             QAction, QFileDialog, QApplication, QPushButton, QSlider, QWidget, QListWidget)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
# библиотека для работы с регулярными выражениями
import re

# Этот класс будет хранить в себе имя файла и полное имя файла с путём
class plItem(object):
    def __init__(self, fPath, fName):
        self.fPath = fPath
        self.fName = fName


class MediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('TestApp')
        # Создание центрального виджета и настройка лайоута
        self.centerWindow = QWidget()
        self.mainGridLayout = QGridLayout()
        self.setCentralWidget(self.centerWindow)
        self.centralWidget().setLayout(self.mainGridLayout)
        # Создаем кнопки и привязывам к ним обработчики
        self.addBtn = QPushButton('Add File', self)
        self.addBtn.clicked.connect(self.addFile)
        self.removeBtn = QPushButton('Remove File', self)
        self.removeBtn.clicked.connect(self.removeFile)

        # Добавляем кнопки в макет addWidget(ОБЪЕКТ, СТРОКА, СТОЛБЕЦ)
        self.mainGridLayout.addWidget(self.addBtn, 1, 0)
        self.mainGridLayout.addWidget(self.removeBtn, 1, 1)

        self.pause = QPushButton('', self)
        pauseIcon = QIcon()
        pauseIcon.addFile('pause.png')
        self.pause.setIcon(pauseIcon)
        self.mainGridLayout.addWidget(self.pause, 3, 1)
        self.pause.clicked.connect(self.PauseMusic)

        self.play = QPushButton('', self)
        playIcon = QIcon()
        playIcon.addFile('play.png')
        self.play.setIcon(playIcon)
        self.mainGridLayout.addWidget(self.play, 3, 0)
        self.play.clicked.connect(self.PlayMusic)
        #создание и настройка таймера и слайдеров
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.Timercheck)
        self.timer.start()

        self.TimeLine = QSlider(Qt.Horizontal, self)
        self.mainGridLayout.addWidget(self.TimeLine, 2, 0, 1, 2)
        self.TimeLine.sliderPressed.connect(self.TLPress)
        self.TimeLine.sliderReleased.connect(self.TLRelease)

        self.Volume = QSlider(Qt.Vertical, self)
        self.mainGridLayout.addWidget(self.Volume, 1, 2, 3, 1)
        self.Volume.valueChanged[int].connect(self.changeVolume)


        # Создаем QListWidget() в котором будут хранится имена фалов
        self.listbox = QListWidget()

        # Добавляем наш листбокс в макет  addWidget(ОБЪЕКТ, СТРОКА, СТОЛБЕЦ,  в высоту, в ширину )
        self.mainGridLayout.addWidget(self.listbox, 0, 0, 1, 0)

        # Создаем список в котором будут хранится имена и пути файлов в список будем добавлять объекты типа plItem
        self.playList = []
        # создаем экземпляр медиаплеера
        self.player = QMediaPlayer()

    #функционал таймера, кнопок и ползунков
    def addFile(self):
        # Получаем полное имя (с путём)
        fullFileName = QFileDialog.getOpenFileName(self, 'Add File', '',"Music files (*.mp3 *.ogg)")[0]
        # Разбиваем на части, используя re.split(r'[\\/]') из библиотеки работы с регулярными выражениями
        # регулярное выражение r'[\\/]' для того, что бы и виндовс и линукс нормально разбивало путь вин \, лин /
        splittedFileName = re.split(r'[\\/]', fullFileName)
        # Получаем имя файла
        shortFileName = splittedFileName[splittedFileName.__len__() - 1]
        # Добавляем в плейлист (который список) имя и соответсвующий ему полый путь с именем
        self.playList.append(plItem(fullFileName, shortFileName))
        # Добавляем в listbox только имя файла
        self.listbox.addItem(shortFileName)
        file = QUrl.fromLocalFile(self.playList[self.listbox.currentIndex().row()].fPath)
        content = QMediaContent(file)
        self.player.setVolume(100)
        self.player.setMedia(content)

    def removeFile(self):
        # Если выделен элемент
        if self.listbox.selectedItems():
            # Удаляем из плейлиста
            self.playList.pop(self.listbox.currentIndex().row())
            # Удаляем из листбокса
            self.listbox.takeItem(self.listbox.currentIndex().row())

    def TLPress(self):
        self.timer.stop()
        self.player.setPosition((self.player.duration() / 100) * self.TimeLine.value())

    def TLRelease(self):
        self.player.setPosition((self.player.duration() / 100) * self.TimeLine.value())
        self.timer.start()

    def TLMoved(self):
        self.player.setPosition((self.player.duration() / 100) * self.TimeLine.value())
        # ----------------

    def Timercheck(self):
        if self.player.duration() != 0:
            pos = self.player.position() / (self.player.duration() / 100)
            self.TimeLine.setValue(pos.__int__())

    def changeVolume(self, value):
        self.player.setVolume(value)

    def PauseMusic(self):
        self.player.pause()

    def PlayMusic(self):
        self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec_())
