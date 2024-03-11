import sys
import rclpy
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QStackedWidget, QLabel, QRadioButton
from PyQt5.QtCore import  Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from datetime import datetime

from publisher import GUI_Node
from manual import MyApp
from home import MyHome
from move import MyMove
from info import MyInfo

import receive

class StartWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
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
        self.mainButton = QPushButton('main', self)
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

####### # Initially disable XYZ buttons ######################################
        self.startButton.setDisabled(True)
        self.stopButton.setDisabled(True)
        self.mainButton.setDisabled(True)
        self.homingButton.setDisabled(True)
        self.movingButton.setDisabled(True)
        self.infoButton.setDisabled(True)
        self.connectButton.setDisabled(True)

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

        self.loadIoImages()

        self.radiobuttons()


###
### def###
###
        
### radio buttons #######################################################
    def radiobuttons(self):

        rbtn1 = QRadioButton('robot', self)
        rbtn1.move(400, 100)
        rbtn1.setAutoExclusive(False)
        rbtn1.repaint()
        if receive.robot == True:
            rbtn1.setChecked(True)
        else :
            rbtn1.setChecked(False)
        
        rbtn2 = QRadioButton(self)
        rbtn2.move(400, 130)
        rbtn2.setText('conveyor')
        rbtn2.setAutoExclusive(False)
        rbtn2.repaint()
        if receive.conveyor == True:
            rbtn2.setChecked(True)
        else :
            rbtn2.setChecked(False)

        rbtn3 = QRadioButton(self)
        rbtn3.move(400, 160)
        rbtn3.setText('vision')
        rbtn3.setAutoExclusive(False)
        rbtn3.repaint()
        if receive.vision == True:
            rbtn3.setChecked(True)
        else :
            rbtn3.setChecked(False)

        rbtn4 = QRadioButton(self)
        rbtn4.move(400, 190)
        rbtn4.setText('encoder')
        rbtn4.setAutoExclusive(False)
        rbtn4.repaint()
        if receive.encoder == True:
            rbtn4.setChecked(True)
        else :
            rbtn4.setChecked(False)



    def loadIoImages(self):
        import receive
####### I/O 신호 관련 이미지 #######################################################
        if receive.robot == True:
            self.input_image(370, 100, 17, 17, "img/on.png")
            print("OK")
        else:
            self.input_image(370, 100, 17, 17, "img/off.png")
            print("No")

        if receive.conveyor == True:
            self.input_image(370, 130, 17, 17, "img/on.png")
            print("OK")
        else:
            self.input_image(370, 130, 17, 17, "img/off.png")
            print("No")

        if receive.vision == True:
            self.input_image(370, 160, 17, 17, "img/on.png")
            print("OK")
        else:
            self.input_image(370, 160, 17, 17, "img/off.png")
            print("No")

        if receive.encoder == True:
            self.input_image(370, 190, 17, 17, "img/on.png")
            print("OK")
        else:
            self.input_image(370, 190, 17, 17, "img/off.png")
            print("No")

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
        print("Operation stopped...")

####### connect ##########################################################
    def connectToReceiver(self):
        # import receive
        self.loadIoImages()
        self.radiobuttons()
        self.update()

        # UI 업데이트
        # self.start_window.update()
        
        print("Connected to receiver")





class AppManager(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('W-ECOBOT Application')
        self.setWindowIcon(QIcon('img/eth.png'))
        self.setFixedSize(800, 600)
        self.setStyleSheet("QStackedWidget {background-image: url('img/start.png');}")
        
        self.initUI()
        
    def initUI(self):
        # MyApp, MyHome, MyMove, MyInfo 등 모든 페이지를 생성
        node = GUI_Node()  # GUI_Node 객체 생성
        self.my_app = MyApp(node)  # MyApp 객체 생성 시 노드 객체 전달
        self.home_app = MyHome(node)  # MyHome 객체 생성 시 노드 객체 전달
        # self.move_app = MyMove(node)  # MyMove 객체 생성 시 노드 객체 전달
        self.info_app = MyInfo(node)  # MyInfo 객체 생성 시 노드 객체 전달
        self.move_app = None  # 초기에 None으로 설정 (애러서 버튼 호출 할때마다 새로운 창을 열기 위함)
        
        # StartWindow를 생성하고 스택에 추가
        self.start_window = StartWindow(parent=self)
        self.addWidget(self.start_window)

        # 나머지 페이지들도 스택에 추가
        self.addWidget(self.my_app)
        self.addWidget(self.home_app)
        # self.addWidget(self.move_app)
        self.addWidget(self.info_app)

        # 뒤로가기 버튼에서 돌아오는 길 지정
        self.my_app.goToStartScreen.connect(self.gotoStart)
        self.home_app.goToStartScreen.connect(self.gotoStart)
        # 
        self.info_app.goToStartScreen.connect(self.gotoStart)

    # 시작 페이지
    def gotoStart(self):
        self.setCurrentWidget(self.start_window)

    # 메인 페이지
    def gotoMain(self):
        self.setCurrentWidget(self.my_app)
        
    # 호밍페이지
    def gotoHome(self):
        self.setCurrentWidget(self.home_app)

    # 무빙(수동)페이지
    def gotoMove(self):
        # self.setCurrentWidget(self.move_app)
        if self.move_app is None:
            node = GUI_Node()  # 새로운 GUI_Node 객체 생성
            self.move_app = MyMove(node)  # MyMove 객체 생성 시 새로운 노드 객체 전달
            self.addWidget(self.move_app)  # 스택에 페이지 추가
    
        self.setCurrentWidget(self.move_app)
        self.move_app.goToStartScreen.connect(self.gotoStart)

    # 인포메이션 페이지
    def gotoInfo(self):
        self.setCurrentWidget(self.info_app)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rclpy.init(args=None)
    app_manager = AppManager()
    app_manager.show()
    sys.exit(app.exec_())
    rclpy.shutdown()
