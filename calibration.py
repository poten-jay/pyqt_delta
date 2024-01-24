
import json
from functools import partial
import openpyxl
from PyQt5.QtWidgets import  QPushButton, QMainWindow, QLabel, QDialog, QDoubleSpinBox
from PyQt5.QtCore import  Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap
from datetime import datetime

from publisher import GUI_Node
from manual import MyApp
from home import MyHome
from move import MyMove
from info import MyInfo

import setting


class MyCal(QMainWindow):
    goToStartScreen = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        
        # UI 초기화 코드


####### start #####################################################################
        self.startButton = QPushButton('START', self)
        self.startButton.clicked.connect(partial(self.readexcel, 5))
        self.startButton.setGeometry(200, 300, 100, 100)


####### start #####################################################################
        self.startButton = QPushButton('START', self)
        self.startButton.clicked.connect(partial(self.readexcel, 4))
        self.startButton.setGeometry(100, 300, 100, 100)


####### stop ######################################################################
        self.stopButton = QPushButton('STOP', self)
        # self.stopButton.clicked.connect(self.stopOperation)
        self.stopButton.setGeometry(400, 300, 100, 100)

####### 뒤로 가기 버튼 ###############################################################
        self.btnback = QPushButton('<<', self)
        self.btnback.clicked.connect(self.goToStartScreen.emit)
        
        self.btnback.setGeometry(0, 528, 50, 50)

####### 시간 #######################################################################
        # 시간 표시 라벨 설정
        self.time_label = QLabel(self)
        self.time_label.setGeometry(660, 585, 200, 10)
        self.time_label.setStyleSheet("font-size: 14px;")
        self.time_label.setStyleSheet("Color : white")

        # QTimer 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)



####### 이미지 삽입 #################################################################
        
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

###### 엑셀읽어오기 #############################################################
    def readexcel(self, n):
        self.n = n
        # Excel 파일에서 값을 읽어와서 표시하는 팝업 생성 및 표시
        excel_file_path = "cal.xlsx"  # 엑셀 파일 경로를 지정하세요.
        popup = ExcelPopup(excel_file_path, n, self)
        popup.exec_()


####### 나머지 코드는 그대로 두고 아래의 ExcelPopup 클래스 추가 ##########################



class ExcelPopup(QDialog):
    def __init__(self, excel_file, row_index, parent=None):
        super().__init__(parent)
        self.excel_file = excel_file
        self.row_index = row_index
        self.initUI()
        self.load_excel_data()

    def initUI(self):
        self.setWindowTitle("Excel Popup")
        self.setGeometry(100, 100, 400, 200)

        # 더블 스핀 박스 추가
        self.double_spin_box1 = QDoubleSpinBox(self)
        self.double_spin_box2 = QDoubleSpinBox(self)
        self.double_spin_box3 = QDoubleSpinBox(self)
        self.double_spin_box1.setRange(setting.x_min, setting.x_max)
        self.double_spin_box2.setRange(setting.y_min, setting.y_max)
        self.double_spin_box3.setRange(setting.z_min, setting.z_max)
        # self.double_spin_box1.setRange(setting.x_min, setting.x_max)
        # self.double_spin_box1.setRange(setting.y_min, setting.y_max)
        # self.double_spin_box1.setRange(setting.z_min, setting.z_max)
        
        self.double_spin_box1.setGeometry(50, 50, 100, 30)
        self.double_spin_box2.setGeometry(175, 50, 100, 30)
        self.double_spin_box3.setGeometry(300, 50, 100, 30)

    def load_excel_data(self):
        try:
            wb = openpyxl.load_workbook(self.excel_file)
            sheet = wb["angles"]
            value1 = float(sheet[self.row_index][0].value)
            value2 = float(sheet[self.row_index][1].value)
            value3 = float(sheet[self.row_index][2].value)

            self.double_spin_box1.setValue(value1)
            self.double_spin_box2.setValue(value2)
            self.double_spin_box3.setValue(value3)
        except Exception as e:
            self.double_spin_box1.setValue(0.0)
            self.double_spin_box2.setValue(0.0)
            self.double_spin_box3.setValue(0.0)



##########################################################
    # stop 누르면 비활성화
    def stopOperation(self):
        self.startButton.setDisabled(False)
        self.stopButton.setDisabled(False)
        self.mainButton.setDisabled(False)
        self.homingButton.setDisabled(False)
        self.movingButton.setDisabled(False)
        self.infoButton.setDisabled(False)
        self.connectButton.setDisabled(False)
        self.onButton.setDisabled(False)
        self.stopButton.setDisabled(False)
        self.offButton.setDisabled(False)
        print("Operation stopped...")

    def onBackButtonClick(self):
        # Emit the signal when the button is clicked
        self.goToStartScreen.emit()


