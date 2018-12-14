import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QPushButton, QSlider)
from PyQt5.QtGui import QIcon, QPixmap
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
        self.TimeLine.setGeometry(50, 250, 300, 20)
        #self.TimeLine.valueChanged.connect(self.player.setPosition)
        #self.player.positionChanged.connect(self.Timeline.setValue)
        #--------- Обработка перетаскивания ползунка --------
        self.TimeLine.sliderPressed.connect(self.tlPress)
        self.TimeLine.sliderReleased.connect(self.tlRelease)
        #----------------------------------------------------

        #--------- Кнопка Play ---------------
        self.play = QPushButton('', self)
        playIcon = QIcon()
        playIcon.addFile('play.png')
        self.play.setIcon(playIcon)
        self.play.resize(self.play.sizeHint())
        self.play.move(110, 200)
        self.play.clicked.connect(self.PlayMusic)
        #--------------------------------

        #-----------Кнопка Pause--------------
        self.pause = QPushButton('', self)
        pauseIcon = QIcon()
        pauseIcon.addFile('pause.png')
        self.pause.setIcon(pauseIcon)
        self.pause.resize(self.play.sizeHint())
        self.pause.move(200, 200)
        self.pause.clicked.connect(self.PauseMusic)
        #---------------------------------------
        self.Volume = QSlider(Qt.Vertical, self)
        self.Volume.setFocusPolicy(Qt.NoFocus)
        self.Volume.setGeometry(350, 55, 30, 100)
        self.Volume.valueChanged[int].connect(self.changeVolume)

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.Timercheck)
        self.timer.start()

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Mediaplayer')
        self.player = QMediaPlayer()
        self.show()

        #---------------- Обработка перемещения ползунка ------------------
    def tlPress(self):
        self.timer.stop()
        self.player.setPosition((self.player.duration()/100) * self.TimeLine.value())
        
    def tlRelease(self):
        self.player.setPosition((self.player.duration()/100) * self.TimeLine.value())
        self.timer.start()
    
    def tlMoved(self):
        self.player.setPosition((self.player.duration()/100) * self.TimeLine.value())
        #---------------- 

    def Timercheck(self):
        if self.player.duration() !=0:
            pos =  self.player.position()/(self.player.duration()/100)
            self.TimeLine.setValue(pos.__int__())

    def showDialog(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open file', '')[0]
        file = QUrl.fromLocalFile(self.filename)
        content = QMediaContent(file)
        self.player.setMedia(content)


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