import sys
import rclpy
import json
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QStackedWidget, QLabel, QRadioButton, QDialog, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import  Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from datetime import datetime

from example import MyEx
from publisher import GUI_Node
from manual import MyApp
from home import MyHome
from move import MyMove
from info import MyInfo
from calibration import MyCal

import receive


class StartWindow(QMainWindow):
    def __init__(self, parent=None, io_data=None):
        super().__init__()
        self.parent = parent
        self.io_data = io_data  # io_data 매개변수를 추가하여 저장
        self.initUI()
        
    def initUI(self):
        # UI 초기화 코드


####### start ######################################################################
        self.startButton = QPushButton('START', self)
        self.startButton.clicked.connect(self.startOperation)
        self.startButton.setGeometry(200, 300, 100, 100)

####### stop ######################################################################
        self.stopButton = QPushButton('STOP', self)
        self.stopButton.clicked.connect(self.stopOperation)
        self.stopButton.setGeometry(400, 300, 100, 100)

####### ON ######################################################################
        self.onButton = QPushButton('ON', self)
        self.onButton.clicked.connect(self.onOperation)
        self.onButton.setGeometry(200, 450, 100, 100)

####### OFF ######################################################################
        self.offButton = QPushButton('OFF', self)
        self.offButton.clicked.connect(self.offOperation)
        self.offButton.setGeometry(400, 450, 100, 100)

####### connect ######################################################################
        self.connectButton = QPushButton('Connect', self)
        self.connectButton.clicked.connect(self.connectToReceiver)
        self.connectButton.setGeometry(600, 300, 100, 50)

####### go main ######################################################################
        self.mainButton = QPushButton('Manual', self)
        self.mainButton.clicked.connect(self.parent.gotoMain)
        self.mainButton.setGeometry(10, 100, 100, 50)

####### go home ######################################################################
        self.homingButton = QPushButton('Home', self)
        self.homingButton.clicked.connect(self.parent.gotoHome)
        self.homingButton.setGeometry(10, 150, 100, 50)

####### go move ######################################################################
        self.movingButton = QPushButton('Move', self)
        self.movingButton.clicked.connect(self.parent.gotoMove)
        self.movingButton.setGeometry(10, 200, 100, 50)

####### go Info ######################################################################
        self.infoButton = QPushButton('Information', self)
        self.infoButton.clicked.connect(self.parent.gotoInfo)
        self.infoButton.setGeometry(10, 250, 100, 50)

# ####### go calibration ######################################################################
#         self.infoButton = QPushButton('calibration', self)
#         self.infoButton.clicked.connect(self.parent.gotoCalibration)
#         self.infoButton.setGeometry(10, 300, 100, 50)

####### go calibration need password ######################################################################
        self.calButton = QPushButton('calibration', self)
        self.calButton.clicked.connect(self.showCalibrationDialog)
        self.calButton.setGeometry(10, 300, 100, 50)     

####### go example ######################################################################
        self.examButton = QPushButton('exmaple', self)
        self.examButton.clicked.connect(self.parent.gotoExample)
        self.examButton.setGeometry(10, 500, 100, 50)

####### # Initially disable XYZ buttons ######################################
        self.startButton.setDisabled(True)
        self.stopButton.setDisabled(True)
        self.mainButton.setDisabled(True)
        self.homingButton.setDisabled(True)
        self.movingButton.setDisabled(True)
        self.infoButton.setDisabled(True)
        self.connectButton.setDisabled(True)
        self.calButton.setDisabled(True)

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

####### I/O 신호 관련 텍스트 ###################################################
        self.sig_robot = QLabel(f"Robot", self)
        self.sig_robot.setStyleSheet("Color : white")
        self.sig_robot.setAlignment(Qt.AlignRight)
        self.sig_robot.setGeometry(300, 100, 60, 30)

        self.sig_conveyor = QLabel(f"conveyor", self)
        self.sig_conveyor.setStyleSheet("Color : white")
        self.sig_conveyor.setAlignment(Qt.AlignRight)
        self.sig_conveyor.setGeometry(300, 130, 60, 30)

        self.sig_vision = QLabel(f"vision", self)
        self.sig_vision.setStyleSheet("Color : white")
        self.sig_vision.setAlignment(Qt.AlignRight)
        self.sig_vision.setGeometry(300, 160, 60, 30)

        self.sig_encoder = QLabel(f"encoder", self)
        self.sig_encoder.setStyleSheet("Color : white")
        self.sig_encoder.setAlignment(Qt.AlignRight)
        self.sig_encoder.setGeometry(300, 190, 60, 30)

        # io update 설정 - 시간 설정은 이미 위에서 했음
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_io)  ### 살리면 1초당 업뎃
        # self.timer.timeout.connect(self.connectToReceiver)
        # self.timer.start(1000)  # 1초마다 업데이트

        with open("document/io.json", "r") as io_file:
            self.io_data = json.load(io_file)

        # self.ioPoint()

        self.loadIoImages()

        self.radiobuttons()



###
### def###
###
        

###### if drawpoint #####################################################
    def ioPoint(self):
        if self.io_data is not None: 
            if self.io_data["robot"] == True:
                self.drawPoint(700, 100, 'green')
                print('conneted')
            else:
                self.drawPoint(700, 100, 'red')
                print('Caution! : Disconneted - Robot')

            if self.io_data["conveyor"] == True:
                self.drawPoint(700, 130, 'green')
            else:
                self.drawPoint(700, 130, 'red')
                print('Caution! : Disconneted - Conveyor')

            if self.io_data["vision"] == True:
                self.drawPoint(700, 160, 'green')
            else:
                self.drawPoint(700, 160, 'red')
                print('Caution! : Disconneted - Vision')

            if self.io_data["encoder"] == True:
                self.drawPoint(700, 190, 'green')
            else:
                self.drawPoint(700, 190, 'red')
                print('Caution! : Disconneted - Encoder')


####### 점 찍기 #########################################################
    def drawPoint(self, x, y, color):
        # 점 찍을 좌표 계산
        point_x = x  # 예시: x 좌표 계산
        point_y = y  # 예시: y 좌표 계산


        # QLabel을 생성하여 점을 표시
        # point_label = setPen(Qpen)

        point_label = QLabel(self)
        point_label.setGeometry(point_x, point_y, 5, 5)  # 점의 크기와 위치 설정
        point_label.setStyleSheet("background-color: "+color+"; border-radius: 10px;")  # 점의 스타일 설정


######## 주기적으로 io.json 파일을 읽고 UI를 업데이트 ##########################
    def update_io(self):
        with open("document/io.json", "r") as io_file:
            # updated_io_data = json.load(io_file)
            self.io_data = json.load(io_file)
            print('open documents')

        # if self.io_data != updated_io_data:
        #     self.io_data = updated_io_data
            # I/O 신호 이미지 업데이트
            self.loadIoImages()

            # 점찍기
            self.ioPoint()

            # 라디오 버튼 업데이트
            self.radiobuttons()

            # UI 업데이트
            # self.update()



####### connect ##########################################################
    def connectToReceiver(self):
        # io.json 파일 읽기
        with open("document/io.json", "r") as io_file:
            self.io_data = json.load(io_file)

            # I/O 신호 이미지 업데이트
            self.loadIoImages()

            # 점찍기
            self.ioPoint()

            # 라디오 버튼 업데이트
            self.radiobuttons()

            # new_start_window = StartWindow(parent=self.parent, io_data=self.io_data)
            # new_start_window.show()
            # UI 업데이트
            # self.update()

            # pyqtSignal()
            print("Connected to receiver")

### radio buttons #######################################################
    def radiobuttons(self):
        if self.io_data is not None:  # io_data가 None이 아닌 경우에만 처리
            rbtn1 = QRadioButton('robot', self)
            rbtn1.move(400, 100)
            rbtn1.setAutoExclusive(False)
            rbtn1.repaint()
            if self.io_data["robot"]:
                rbtn1.setChecked(True)
            else:
                rbtn1.setChecked(False)
            
            rbtn2 = QRadioButton(self)
            rbtn2.move(400, 130)
            rbtn2.setText('conveyor')
            rbtn2.setAutoExclusive(False)
            rbtn2.repaint()
            if self.io_data["conveyor"]:
                rbtn2.setChecked(True)
            else:
                rbtn2.setChecked(False)

            rbtn3 = QRadioButton(self)
            rbtn3.move(400, 160)
            rbtn3.setText('vision')
            rbtn3.setAutoExclusive(False)
            rbtn3.repaint()
            if self.io_data["vision"]:
                rbtn3.setChecked(True)
            else:
                rbtn3.setChecked(False)

            rbtn4 = QRadioButton(self)
            rbtn4.move(400, 190)
            rbtn4.setText('encoder')
            rbtn4.setAutoExclusive(False)
            rbtn4.repaint()
            if self.io_data["encoder"]:
                rbtn4.setChecked(True)
            else:
                rbtn4.setChecked(False)

####### I/O 신호 관련 이미지 #######################################################
    def loadIoImages(self):
        if self.io_data is not None:  # io_data가 None이 아닌 경우에만 처리
            if self.io_data["robot"] == True:
                self.input_image(370, 100, 17, 17, "img/on.png")
            else:
                self.input_image(370, 100, 17, 17, "img/off.png")
            if self.io_data["conveyor"] == True:
                self.input_image(370, 130, 17, 17, "img/on.png")
            else:
                self.input_image(370, 130, 17, 17, "img/off.png")
            if self.io_data["vision"] == True:
                self.input_image(370, 160, 17, 17, "img/on.png")
            else:
                self.input_image(370, 160, 17, 17, "img/off.png")
            if self.io_data["encoder"] == True:
                self.input_image(370, 190, 17, 17, "img/on.png")
            else:
                self.input_image(370, 190, 17, 17, "img/off.png")

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

####### on / off ##########################################################
    def onOperation(self):
        self.startButton.setDisabled(False)
        self.stopButton.setDisabled(False)
        self.mainButton.setDisabled(False)
        self.homingButton.setDisabled(False)
        self.movingButton.setDisabled(False)
        self.infoButton.setDisabled(False)
        self.connectButton.setDisabled(False)
        self.calButton.setDisabled(False)
        print("Robot ON!!")

    # stop 누르면 비활성화
    def offOperation(self):
        self.startButton.setDisabled(True)
        self.stopButton.setDisabled(True)
        self.mainButton.setDisabled(True)
        self.homingButton.setDisabled(True)
        self.movingButton.setDisabled(True)
        self.infoButton.setDisabled(True)
        self.connectButton.setDisabled(True)
        self.calButton.setDisabled(True)
        print("Good Bye...")

####### start/stop ##########################################################
    def startOperation(self):
        self.startButton.setDisabled(True)
        # self.stopButton.setDisabled(True)
        self.mainButton.setDisabled(True)
        self.homingButton.setDisabled(True)
        self.movingButton.setDisabled(True)
        # self.infoButton.setDisabled(True)
        self.connectButton.setDisabled(True)
        self.onButton.setDisabled(True)
        self.offButton.setDisabled(True)
        self.calButton.setDisabled(True)
        print("Operation started!!")

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
        self.calButton.setDisabled(False)
        print("Operation stopped...")


    def showCalibrationDialog(self):
        # 비밀번호 입력 다이얼로그 생성
        dialog = PasswordDialog(self)
        result = dialog.exec_()  # 다이얼로그를 모달로 표시하고 결과를 받음

        # 다이얼로그 결과 확인
        if result == QDialog.Accepted:
            self.parent.gotoCalibration()  # 올바른 비밀번호가 입력되면 calibration 페이지로 이동

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Password')
        self.setFixedSize(300, 150)

        self.label = QLabel('Please Enter password', self)
        self.label.setGeometry(20, 20, 260, 30)

        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(20, 60, 260, 30)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_button = QPushButton('OK', self)
        self.confirm_button.setGeometry(20, 100, 120, 30)
        self.confirm_button.clicked.connect(self.checkPassword)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.setGeometry(160, 100, 120, 30)
        self.cancel_button.clicked.connect(self.reject)

    def checkPassword(self):
        # 입력된 비밀번호 확인
        if self.password_input.text() == '1234':
            self.accept()  # 올바른 비밀번호인 경우 다이얼로그를 종료하고 Accepted 반환
        else:
            QMessageBox.warning(self, 'Erorr', 'Invalied password!.')
            self.password_input.clear()



# class AppManager(QStackedWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('W-ECOBOT Application')
#         self.setWindowIcon(QIcon('img/eth.png'))
#         self.setFixedSize(800, 600)
#         self.setStyleSheet("QStackedWidget {background-image: url('img/start.png');}")
#         self.node = GUI_Node()  # GUI_Node 객체 생성
#         self.initUI()
        
#     def initUI(self):
#         # MyApp, MyHome, MyMove, MyInfo 등 모든 페이지를 생성
        
#         self.my_app = MyApp(self.node)  # MyApp 객체 생성 시 노드 객체 전달
#         self.home_app = MyHome(self.node)  # MyHome 객체 생성 시 노드 객체 전달
#         # self.move_app = MyMove(self.node)  # MyMove 객체 생성 시 노드 객체 전달
#         self.info_app = MyInfo(self.node)  # MyInfo 객체 생성 시 노드 객체 전달
#         self.move_app = None  # 초기에 None으로 설정 (애러서 버튼 호출 할때마다 새로운 창을 열기 위함)
        
#         # StartWindow를 생성하고 스택에 추가
#         self.start_window = StartWindow(parent=self)
#         self.addWidget(self.start_window)

#         # 나머지 페이지들도 스택에 추가
#         self.addWidget(self.my_app)
#         self.addWidget(self.home_app)
#         # self.addWidget(self.move_app)
#         self.addWidget(self.info_app)

#         # 뒤로가기 버튼에서 돌아오는 길 지정
#         self.my_app.goToStartScreen.connect(self.gotoStart)
#         self.home_app.goToStartScreen.connect(self.gotoStart)
#         # 
#         self.info_app.goToStartScreen.connect(self.gotoStart)

#     # 시작 페이지
#     def gotoStart(self):
#         self.setCurrentWidget(self.start_window)

#     # 메인 페이지
#     def gotoMain(self):
#         self.setCurrentWidget(self.my_app)
        
#     # 호밍페이지
#     def gotoHome(self):
#         self.setCurrentWidget(self.home_app)

#     # 무빙(수동)페이지
#     def gotoMove(self):
#         # self.setCurrentWidget(self.move_app)
#         if self.move_app is None:
#             # node = GUI_Node()  # 새로운 GUI_Node 객체 생성
#             self.move_app = MyMove()  # MyMove 객체 생성 시 새로운 노드 객체 전달
#             self.addWidget(self.move_app)  # 스택에 페이지 추가
    
#         self.setCurrentWidget(self.move_app)
#         self.move_app.goToStartScreen.connect(self.gotoStart)

#     # 인포메이션 페이지
#     def gotoInfo(self):
#         self.setCurrentWidget(self.info_app)

# if __name__ == '__main__':
#     app = QApplication(sys.argv) # QApplication : 프로그램을 실행시켜주는 클래스
#     rclpy.init(args=None)
#     app_manager = AppManager()
#     app_manager.show()
#     sys.exit(app.exec_())
#     rclpy.shutdown()
