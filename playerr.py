import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QPushButton, QSlider)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from time import sleep

class AudioPlayer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.TimeLine = QSlider(Qt.Horizontal, self)
        #self.TimeLine.setFocusPolicy(Qt.NoFocus)
        self.TimeLine.setGeometry(50, 75, 300, 200)
        #self.TimeLine.valueChanged.connect(self.player.setPosition)
        #self.player.positionChanged.connect(self.Timeline.setValue)


        self.play = QPushButton('⏵', self)
        self.play.resize(self.play.sizeHint())
        self.play.move(110, 200)
        self.play.clicked.connect(self.PlayMusic)

        self.play = QPushButton('⏸', self)
        self.play.resize(self.play.sizeHint())
        self.play.move(200, 200)
        self.play.clicked.connect(self.PauseMusic)

        self.Volume = QSlider(Qt.Vertical, self)
        self.Volume.setFocusPolicy(Qt.NoFocus)
        self.Volume.setGeometry(350, 55, 30, 100)
        self.Volume.valueChanged[int].connect(self.changeVolume)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Mediaplayer')
        self.player = QMediaPlayer()
        self.show()


    def showDialog(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        file = QUrl.fromLocalFile(self.filename)
        content = QMediaContent(file)
        self.player.setMedia(content)
        self.TimeLine.setMinimum(0)
        self.TimeLine.setMaximum(self.player.duration())
        self.TimeLine.valueChanged.connect(self.player.setPosition)
        self.player.positionChanged.connect(self.TimeLine.setValue)

        #app.exhjkec()

    def ChangeTime(self):
        #self.TimeLine.setMinimum(0)
        #self.TimeLine.setMaximum(self.player.duration())
        #self.TimeLine.valueChanged.connect(self.player.setPosition)
        #self.player.positionChanged.connect(self.TimeLine.setValue)

    def changeVolume(self, value):
        self.player.setVolume(value)

    def PauseMusic(self):
        self.player.pause()

    def PlayMusic(self):
        self.player.play()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = AudioPlayer()
    sys.exit(app.exec_())