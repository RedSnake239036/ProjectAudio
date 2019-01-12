import sys
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QTextEdit,
                             QAction, QFileDialog, QApplication, QPushButton, QSlider, QWidget, QListWidget, QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
# библиотека для работы с регулярными выражениями
import re
import time

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
        self.setWindowTitle('MediaPlayer')
        # Создание центрального виджета и настройка лайоута для поддержания формы интерфейса
        self.centerWindow = QWidget()
        self.mainGridLayout = QGridLayout()
        self.setCentralWidget(self.centerWindow)
        self.centralWidget().setLayout(self.mainGridLayout)
        # кнопки добавления и удаления трека
        self.addBtn = QPushButton('Add File', self)
        self.addBtn.clicked.connect(self.addFile)
        self.removeBtn = QPushButton('Remove File', self)
        self.removeBtn.clicked.connect(self.removeFile)
        self.mainGridLayout.addWidget(self.addBtn, 1, 0)
        self.mainGridLayout.addWidget(self.removeBtn, 1, 1)
        # Кнопка prev
        self.prevBtn = QPushButton('', self)
        prevIcon = QIcon()
        prevIcon.addFile('prev.png') 
        # Назначаем иконку кнопке
        self.prevBtn.setIcon(prevIcon)
        # Размещаем кнопку на макете (лайоуте)
        self.mainGridLayout.addWidget(self.prevBtn, 3, 0)
        self.prevBtn.clicked.connect(self.PreviousTrack)
        # Кнопка play
        self.playBtn = QPushButton('', self)
        playIcon = QIcon()
        playIcon.addFile('play.png')
        self.playBtn.setIcon(playIcon)
        self.mainGridLayout.addWidget(self.playBtn, 3, 1)
        self.playBtn.clicked.connect(self.PlayMusic)
        # Кнопка pause
        self.pause = QPushButton('', self)
        pauseIcon = QIcon()
        pauseIcon.addFile('pause.png')
        self.pause.setIcon(pauseIcon)
        self.mainGridLayout.addWidget(self.pause, 3, 2)
        self.pause.clicked.connect(self.PauseMusic)
        # Кнопка next
        self.nextBtn = QPushButton('',self)
        nextIcon = QIcon()
        nextIcon.addFile('next.png')
        self.nextBtn.setIcon(nextIcon)
        self.mainGridLayout.addWidget(self.nextBtn,         3, 3)
        self.nextBtn.clicked.connect(self.NextTrack)
        # создание и настройка таймера и слайдеров
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.Timercheck)
        self.timer.start()
        # Таймлайн
        self.TimeLine = QSlider(Qt.Horizontal, self)
        self.mainGridLayout.addWidget(self.TimeLine, 2, 0, 1, 4)
        self.TimeLine.sliderPressed.connect(self.TLPress)
        self.TimeLine.sliderReleased.connect(self.TLRelease)
        # Громкость
        self.Volume = QSlider(Qt.Vertical, self)
        self.Volume.setValue(50)
        self.mainGridLayout.addWidget(self.Volume, 1, 4, 3, 1)
        self.Volume.valueChanged[int].connect(self.changeVolume)
        # создаем экземпляр медиаплеера
        self.player = QMediaPlayer()
        self.player.stateChanged.connect(self.media_status_changed)
        # Создаем QListWidget() в котором будут хранится имена фалов
        self.listbox = QListWidget()
        self.listbox.doubleClicked.connect(self.PlayMusic)
        # Добавляем наш листбокс в макет  addWidget(ОБЪЕКТ, СТРОКА, СТОЛБЕЦ,  в высоту, в ширину )
        self.mainGridLayout.addWidget(self.listbox, 0, 0, 1, 0)
        self.LoopCheckbox = QCheckBox('Зациклить', self)
        self.mainGridLayout.addWidget(self.LoopCheckbox, 1, 2)
        self.LoopCheckbox.stateChanged.connect(self.CheckboxState)
        # Создаем список в котором будут хранится имена и пути файлов в список будем добавлять объекты типа plItem
        self.playList = []
        # Признак зацикленности плейлиста и флаг изменения состояния плеера
        self.loop = True
        self.IgnoreStateChange = False

    def CheckboxState(self, state):
        if state == Qt.Checked:
            self.IgnoreStateChange = True
        else:
            self.IgnoreStateChange = False
    # функционал таймера, кнопок и ползунков
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

        # Удаление файла из листбокса
    def removeFile(self):
        if self.listbox.selectedItems():
            self.playList.pop(self.listbox.currentIndex().row())
            self.listbox.takeItem(self.listbox.currentIndex().row())

    # Зависимости таймера и таймлайна
    def TLPress(self):
        self.timer.stop()
        self.player.setPosition((self.player.duration() / 100) * self.TimeLine.value())

    def TLRelease(self):
        self.player.setPosition((self.player.duration() / 100) * self.TimeLine.value())
        self.timer.start()

    def TLMoved(self):
        self.player.setPosition((self.player.duration() / 100) * self.TimeLine.value())

    def Timercheck(self):
        if self.player.duration() != 0:
            pos = self.player.position() / (self.player.duration() / 100)
            self.TimeLine.setValue(pos.__int__())

    # Предыдущий трэк
    def PreviousTrack(self):
        if self.listbox.selectedItems() and (self.listbox.currentRow() != 0):
            self.IgnoreStateChange = True
            self.listbox.setCurrentRow(self.listbox.currentIndex().row() - 1)
            self.PlayMusic()
            self.IgnoreStateChange = False
        elif self.listbox.selectedItems() and (self.listbox.currentRow() == 0):
            self.IgnoreStateChange = True
            self.listbox.setCurrentRow(self.listbox.__len__() - 1)
            self.PlayMusic()
            self.IgnoreStateChange = False

    # Следующий трэк
    def NextTrack(self):
        if self.listbox.selectedItems() and (self.listbox.currentRow() != self.listbox.__len__() - 1):
            self.IgnoreStateChange = True
            self.listbox.setCurrentRow(self.listbox.currentIndex().row() + 1)
            self.PlayMusic()
            self.IgnoreStateChange = False
        elif self.listbox.selectedItems() and (self.listbox.currentRow() == self.listbox.__len__() - 1):
            self.IgnoreStateChange = True
            self.listbox.setCurrentRow(0)
            self.PlayMusic()
            self.IgnoreStateChange = False

    # громкость, play, pause
    def changeVolume(self, value):
        self.player.setVolume(value)

    def PauseMusic(self):
        self.player.pause()

    def PlayMusic(self):
        if self.listbox.selectedItems():
            file = QUrl.fromLocalFile(self.playList[self.listbox.currentIndex().row()].fPath)
            content = QMediaContent(file)
            self.player.setMedia(content)
            self.player.setVolume(self.Volume.value())
            self.player.play()
        elif self.listbox.__len__() > 0:
            self.listbox.setCurrentRow(0)
            file = QUrl.fromLocalFile(self.playList[self.listbox.currentIndex().row()].fPath)
            content = QMediaContent(file)
            self.player.setMedia(content)
            self.player.setVolume(self.Volume.value())
            self.player.play()

    # Переход на след трек
    def media_status_changed(self, status):
        if not self.IgnoreStateChange:
            if status == QMediaPlayer.StoppedState:
                if (self.listbox.currentIndex().row() == self.listbox.__len__()-1) and self.loop:
                    self.listbox.setCurrentRow(0)
                    file = QUrl.fromLocalFile(self.playList[self.listbox.currentIndex().row()].fPath)
                    content = QMediaContent(file)
                    self.player.setMedia(content)
                    self.player.play()
                elif self.listbox.currentIndex().row() < self.listbox.__len__()-1:
                    self.listbox.setCurrentRow(self.listbox.currentIndex().row()+1)
                    file = QUrl.fromLocalFile(self.playList[self.listbox.currentIndex().row()].fPath)
                    content = QMediaContent(file)
                    self.player.setMedia(content)
                    self.player.play()
        if self.IgnoreStateChange:
            self.player.play()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MediaPlayer()
    ex.show()
    sys.exit(app.exec())
