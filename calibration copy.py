
import json
from functools import partial
import openpyxl
from PyQt5.QtWidgets import  QPushButton, QMainWindow, QLabel, QDialog, QDoubleSpinBox
from PyQt5.QtCore import  Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap
from datetime import datetime

# from publisher import GUI_Node
from manual import MyApp
from home import MyHome
from move import MyMove
from info import MyInfo

import setting
from function import xyz_button


class MyCal(QMainWindow):
    goToStartScreen = pyqtSignal()
    def __init__(self,node, parent=None):
        super().__init__()
        self.node = node
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        
        # UI 초기화 코드


####### bnt_1 #####################################################################
        self.cal_1 = QPushButton('01', self)
        self.cal_1.clicked.connect(partial(self.readexcel, 2))
        self.cal_1.setGeometry(200, 100, 50, 50)

####### btn_2 #####################################################################
        self.cal_2 = QPushButton('02', self)
        self.cal_2.clicked.connect(partial(self.readexcel, 3))
        self.cal_2.setGeometry(300, 100, 50, 50)

####### btn_3 #####################################################################
        self.cal_3 = QPushButton('03', self)
        self.cal_3.clicked.connect(partial(self.readexcel, 4))
        self.cal_3.setGeometry(400, 100, 50, 50)

####### btn_4 #####################################################################
        self.cal_4 = QPushButton('04', self)
        self.cal_4.clicked.connect(partial(self.readexcel, 5))
        self.cal_4.setGeometry(500, 100, 50, 50)

####### btn_5 #####################################################################
        self.cal_5 = QPushButton('05', self)
        self.cal_5.clicked.connect(partial(self.readexcel, 6))
        self.cal_5.setGeometry(600, 100, 50, 50)

# ####### bnt_6 #####################################################################
#         self.cal_6 = QPushButton('06', self)
#         self.cal_6.clicked.connect(partial(self.readexcel, 7))
#         self.cal_6.setGeometry(200, 200, 50, 50)

# ####### btn_7 #####################################################################
#         self.cal_7 = QPushButton('07', self)
#         self.cal_7.clicked.connect(partial(self.readexcel, 8))
#         self.cal_7.setGeometry(300, 200, 50, 50)

# ####### btn_8 ####################################################################
#         self.cal_8 = QPushButton('08', self)
#         self.cal_8.clicked.connect(partial(self.readexcel, 9))
#         self.cal_8.setGeometry(400, 200, 50, 50)

# ####### btn_9 #####################################################################
#         self.cal_9 = QPushButton('09', self)
#         self.cal_9.clicked.connect(partial(self.readexcel, 10))
#         self.cal_9.setGeometry(500, 200, 50, 50)

# ####### btn_10 #####################################################################
#         self.cal_10 = QPushButton('10', self)
#         self.cal_10.clicked.connect(partial(self.readexcel, 11))
#         self.cal_10.setGeometry(600, 200, 50, 50)




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
        
        # self.node.publish_xyz( x, y, z)  # Create an instance of xyz_button
        # Excel 파일에서 값을 읽어와서 표시하는 팝업 생성 및 표시
        excel_file_path = "cal.xlsx"  # 엑셀 파일 경로를 지정하세요.
        popup = ExcelPopup(excel_file_path, n, self.node, self)
        popup.exec_()


####### 나머지 코드는 그대로 두고 아래의 ExcelPopup 클래스 추가 ##########################


# x = 0.0
# y = 0.0
# z = -900.0

class ExcelPopup(QDialog):
    # btn = xyz_button(x, y, z)

    def __init__(self, excel_file, row_index, node, parent=None):
        super().__init__(parent)
        self.excel_file = excel_file
        self.row_index = row_index
        self.node = node
        # self.xyz_btn = xyz_btn_instance  # Store the xyz_button instance
        self.initUI()
        self.load_excel_data()

    def initUI(self):
        self.setWindowTitle("Excel Popup")
        self.setGeometry(100, 100, 400, 200)

        # Update Button
        self.btnUpdate = QPushButton('Run', self)
        self.btnUpdate.setGeometry(100, 100, 50, 30)  # Adjust as needed
        # self.btnUpdate.clicked.connect(self.updateXYZ)
        self.btnUpdate.clicked.connect(lambda: print('gogogoogo xyz'))
        

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
        
        self.double_spin_box1.setGeometry(25, 50, 100, 30)
        self.double_spin_box2.setGeometry(150, 50, 100, 30)
        self.double_spin_box3.setGeometry(275, 50, 100, 30)

        # 스핀 박스 값 변경 시그널에 연결
        self.double_spin_box1.valueChanged.connect(self.on_spin_box_changed)
        self.double_spin_box2.valueChanged.connect(self.on_spin_box_changed)
        self.double_spin_box3.valueChanged.connect(self.on_spin_box_changed)


    def load_excel_data(self):
        try:
            wb = openpyxl.load_workbook(self.excel_file)
            sheet = wb["angles"]
            value1 = float(sheet[self.row_index][6].value)
            value2 = float(sheet[self.row_index][7].value)
            value3 = float(sheet[self.row_index][8].value)


            # 엑셀에서 읽어와서 스핀박스에 띄워줌
            self.double_spin_box1.setValue(value1)
                                    # Current value: -400.0
                                    # xㅌㅌ :  -400.0
                                    # yㅛㅛ :  0.0
                                    # zㅋㅋ :  -700.0
            self.double_spin_box2.setValue(value2)
                                    # Current value: -400.0
                                    # xㅌㅌ :  -400.0
                                    # yㅛㅛ :  -400.0
                                    # zㅋㅋ :  -700.0
            self.double_spin_box3.setValue(value3)
                                    # Current value: -900.0
                                    # xㅌㅌ :  -400.0
                                    # yㅛㅛ :  -400.0
                                    # zㅋㅋ :  -900.0


        except Exception as e:
            self.double_spin_box1.setValue(0.0)
            self.double_spin_box2.setValue(0.0)
            self.double_spin_box3.setValue(0.0)

    def on_spin_box_changed(self, value):
        # value 인수로 현재 스핀 박스의 값이 전달됩니다.
        print(f"Current value: {value}")
        # Update the xyz_button instance with new values
        # print(value)
        # if isinstance(value, float) ==True:
        x = self.double_spin_box1.value()
        print('xㅌㅌ : ', x)
        y = self.double_spin_box2.value()
        print('yㅛㅛ : ', y)
        z = self.double_spin_box3.value()
        print('zㅋㅋ : ',  z)
        self.node.publish_xyz(x,y,z)





##########################################################


    def onBackButtonClick(self):
        # Emit the signal when the button is clicked
        self.goToStartScreen.emit()


