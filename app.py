# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from pytube import YouTube
from moviepy.editor import *
import os
import concurrent.futures
from PyQt5.QtWidgets import QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(251, 355)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.downloadBtn = QtWidgets.QPushButton(self.centralwidget)
        self.downloadBtn.setGeometry(QtCore.QRect(10, 290, 231, 41))
        self.downloadBtn.setObjectName("downloadBtn")
        self.linkBox = QtWidgets.QTextEdit(self.centralwidget)
        self.linkBox.setGeometry(QtCore.QRect(10, 40, 231, 221))
        self.linkBox.setObjectName("linkBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.mp3Radio = QtWidgets.QRadioButton(self.centralwidget)
        self.mp3Radio.setGeometry(QtCore.QRect(10, 270, 82, 17))
        self.mp3Radio.setObjectName("mp3Radio")
        self.wavRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.wavRadio.setGeometry(QtCore.QRect(100, 270, 82, 17))
        self.wavRadio.setObjectName("wavRadio")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pobieranie z YouTube"))
        self.downloadBtn.setText(_translate("MainWindow", "Pobierz"))
        self.label.setText(_translate("MainWindow", "Wpisz adresy YouTube"))
        self.mp3Radio.setText(_translate("MainWindow", "Format MP3"))
        self.wavRadio.setText(_translate("MainWindow", "Format WAV"))
        self.downloadBtn.clicked.connect(self.get_songs)
    
    def get_songs(self):
        urls = self.linkBox.toPlainText().split('\n')
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.get_single_song, url) for url in urls]
            executor.shutdown(wait=True)
        msg = QMessageBox()
        msg.setWindowTitle("Zakończono")
        msg.setText("Zakończono pracę")
        msg.exec()

    def get_single_song(self, url):
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        song_title = stream.title
        path = sys.path[0]

        full_path = path + '\\pobrane\\'
        stream.download(output_path = full_path, filename=song_title)
        conv = AudioFileClip(full_path + song_title+'.mp4')
        conv.write_audiofile(full_path + song_title+'.mp3')
        conv.close()
        os.remove(full_path + song_title+'.mp4')
        
if __name__ == "__main__":
    import sys
    try:
        path = sys.path[0]
        os.mkdir("pobrane")
    except FileExistsError:
        pass
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

