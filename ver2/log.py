
import json
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QStackedWidget, QLabel, QRadioButton, QTextBrowser
from PyQt5.QtCore import  Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from datetime import datetime

from publisher import GUI_Node
from manual import MyApp
from home import MyHome
from move import MyMove
from info import MyInfo


class MyLog(QMainWindow):
    goToStartScreen = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        
        # UI 초기화 코드
######## 이미지 넣기 #######################################################
        original_pixmap = QPixmap("img/log.png")
        scaled_pixmap = original_pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # QLabel 생성 및 QPixmap 설정
        lbl_img = QLabel(self)
        lbl_img.setPixmap(scaled_pixmap)
        lbl_img.setGeometry(0, 0, scaled_pixmap.width(), scaled_pixmap.height())
########################################################################
#

####### start ######################################################################
        self.startButton = QPushButton('Re', self)
        # self.startButton.clicked.connect(self.startOperation)
        self.startButton.setGeometry(50, 200, 100, 100)

        # self.text_browser = QTextBrowser(self)
        # # self.text_browser.setGeometry(200, 100, 400, 400)
        # self.update_text_browser()
        # self.startButton.clicked.connect(self.update_text_browser)

####### stop ######################################################################
        # self.stopButton = QPushButton('STOP', self)
        # self.stopButton.clicked.connect(self.stopOperation)
        # self.stopButton.setGeometry(50, 400, 100, 100)

####### 뒤로 가기 버튼 ######################################################################
        self.btnback = QPushButton('<<', self)
        self.btnback.clicked.connect(self.goToStartScreen.emit)
        
        self.btnback.setGeometry(0, 528, 50, 50)

####### 시간 ######################################################################
        # 시간 표시 라벨 설정
        self.time_label = QLabel(self)
        self.time_label.setGeometry(660, 585, 200, 10)
        self.time_label.setStyleSheet("font-size: 14px;")
        self.time_label.setStyleSheet("Color : white")

        # QTimer 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

####### QTextBrowser 위젯 추가 ###############################################
        self.text_browser = QTextBrowser(self)
        self.text_browser.setGeometry(200, 100, 400, 200)
        self.update_text_browser()
        self.startButton.clicked.connect(self.update_text_browser)

        # 텍스트 파일 내용을 읽어와서 QTextBrowser에 표시
        try:
            file_path = 'document/log.txt'  # 실제 파일 경로로 변경
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
                self.text_browser.setPlainText(text_content)
        except Exception as e:
            self.text_browser.setPlainText(f"Error: {str(e)}")



####### 이미지 삽입 ################################################################
        
    def input_image(self, x, y, w, h, img_path):
        pixmap = QPixmap(img_path)
        scaled_pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # QLabel 생성 및 QPixmap 설정
        lbl_img = QLabel(self)
        lbl_img.setPixmap(scaled_pixmap)
        lbl_img.setGeometry(x, y, scaled_pixmap.width(), scaled_pixmap.height())

####### 시간 #################################################################
    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(current_time)

####### start/stop ##########################################################
    def startOperation(self):
        self.startButton.setDisabled(True)
        print("Operation started!!")
        

    # stop 누르면 비활성화
    def stopOperation(self):
        self.startButton.setDisabled(False)
        self.stopButton.setDisabled(False)
        self.stopButton.setDisabled(False)
        print("Operation stopped...")

    def onBackButtonClick(self):
        # Emit the signal when the button is clicked
        self.goToStartScreen.emit()


    def update_text_browser(self):
        try:
            file_path = 'document/log.txt'  # Replace with your actual file path
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
                self.text_browser.setPlainText(text_content)
        except Exception as e:
            self.text_browser.setPlainText(f"Error: {str(e)}")