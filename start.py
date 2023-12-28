import sys
import main
import rclpy
from rclpy.node import Node
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer
from geometry_msgs.msg import Point
from datetime import datetime


from main import MyApp
from home import MyHome
from move import MyMove
from info import MyInfo
import receive
import setting


class StartWindow(QWidget):
    def __init__(self, MyApp):
        super().__init__()
        self.initUI()
        self.MyApp = MyApp
        

    def initUI(self):
        # 창 제목
        # self.setWindowTitle('Start Window')
        # 이 부분이 child로 존재하므로 parents 에 작성을 해야 적용이 됨

####### 이미지 추가 삽입 ################################################################

        # original_pixmap = QPixmap("/workspace/pyqt_delta/img/start.png")
        # scaled_pixmap = original_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # # QLabel 생성 및 QPixmap 설정
        # lbl_img = QLabel(self)
        # lbl_img.setPixmap(scaled_pixmap)
        # lbl_img.setGeometry(0, 0, scaled_pixmap.width(), scaled_pixmap.height())

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

    def loadIoImages(self):
        import receive
####### I/O 신호 관련 이미지 #######################################################
        if receive.robot == True:
            self.input_image(370, 100, 17, 17, "/workspace/pyqt_delta/img/on.png")
            print("OK")
        else:
            self.input_image(370, 100, 17, 17, "/workspace/pyqt_delta/img/off.png")
            print("No")

        if receive.conveyor == True:
            self.input_image(370, 130, 17, 17, "/workspace/pyqt_delta/img/on.png")
            print("OK")
        else:
            self.input_image(370, 130, 17, 17, "/workspace/pyqt_delta/img/off.png")
            print("No")

        if receive.vision == True:
            self.input_image(370, 160, 17, 17, "/workspace/pyqt_delta/img/on.png")
            print("OK")
        else:
            self.input_image(370, 160, 17, 17, "/workspace/pyqt_delta/img/off.png")
            print("No")

        if receive.encoder == True:
            self.input_image(370, 190, 17, 17, "/workspace/pyqt_delta/img/on.png")
            print("OK")
        else:
            self.input_image(370, 190, 17, 17, "/workspace/pyqt_delta/img/off.png")
            print("No")

####### 이미지 삽입 ################################################################
        
    def input_image(self, x, y, w, h, img_path):
        pixmap = QPixmap(img_path)
        scaled_pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # QLabel 생성 및 QPixmap 설정
        lbl_img = QLabel(self)
        lbl_img.setPixmap(scaled_pixmap)
        lbl_img.setGeometry(x, y, scaled_pixmap.width(), scaled_pixmap.height())

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
        self.mainButton.clicked.connect(self.gotoMain)
        self.mainButton.setGeometry(10, 100, 100, 50)

####### go home ######################################################################
        self.homingButton = QPushButton('homing', self)
        self.homingButton.clicked.connect(self.gotoHome)
        self.homingButton.setGeometry(10, 150, 100, 50)

####### go move ######################################################################
        self.movingButton = QPushButton('moving', self)
        self.movingButton.clicked.connect(self.gotoMove)
        self.movingButton.setGeometry(10, 200, 100, 50)

####### go Info ######################################################################
        self.infoButton = QPushButton('Infomation', self)
        self.infoButton.clicked.connect(self.gotoInfo)
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
        # 시간을 표시할 QLabel 생성
        self.time_label = QLabel(self)
        self.time_label.setGeometry(660, 585, 200, 10)  # 위치와 크기 설정
        self.time_label.setStyleSheet("font-size: 14px;")  # 폰트 크기 설정
        self.time_label.setStyleSheet("Color : white")

        # QTimer 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1초마다 update_time 함수 호출

####### main 으로 #################################################################

    def gotoMain(self):
        main_window = self.parent().findChild(MyApp)
        self.parent().setCurrentWidget(main_window)

####### home 으로 #################################################################

    def gotoHome(self):
        home_window = self.parent().findChild(MyHome)
        self.parent().setCurrentWidget(home_window)

####### move 로 #################################################################

    def gotoMove(self):
        move_window = self.parent().findChild(MyMove)
        self.parent().setCurrentWidget(move_window)

####### info 로 #################################################################

    def gotoInfo(self):
        info_window = self.parent().findChild(MyInfo)
        self.parent().setCurrentWidget(info_window)


####### 시간 #################################################################
    def update_time(self):
        # 현재 시간을 가져와서 QLabel에 표시
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
        # 특정 내용을 넣어햐함....
        # importlib.reload(receive)
        # self.loadIoImages()
        print("Connected to receiver")





class GUI_Node(Node):
    def __init__(self):
        super().__init__('gui_node')
        # Publisher 생성
        self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)

        # PyQT 생성을 위함
        self.app = QApplication(sys.argv)
        self.stack = QStackedWidget() # Stack을 통한 Widget 띄우기에 필요한 것. 

        # Main page 불러옴
        self.mainApp = MyApp(self)
        self.mainApp.goToStartScreen.connect(self.showStartWindow)

        # Homing page 불러옴
        self.homeApp = MyHome(self)
        self.homeApp.goToStartScreen.connect(self.showStartWindow)

        # Move page 불러옴
        self.moveApp = MyMove(self)
        self.moveApp.goToStartScreen.connect(self.showStartWindow)

        # Info page 불러옴
        self.infoApp = MyInfo(self)
        self.infoApp.goToStartScreen.connect(self.showStartWindow)

        # 추가할 page 불러옴
        # ~~~~~~~~~~~~~~




        # Start page 불러옴. 여기서 Child page들이 필요함
        self.start_window = StartWindow(self.mainApp)

        # stack에 위젯을 추가함. 
        self.stack.addWidget(self.start_window)
        self.stack.addWidget(self.mainApp)
        self.stack.addWidget(self.homeApp)
        self.stack.addWidget(self.moveApp)
        self.stack.addWidget(self.infoApp)


        # stack의 타이틀을 설정함 (예: 첫 번째 위젯이 표시될 때) - 부모에 설정
        self.stack.setWindowTitle('W-ECOBOT Application')
        # 창 타이틀 아이콘 - 윈도우에서는 가능
        self.stack.setWindowIcon(QIcon('/workspace/pyqt_delta/img/eth.png'))
        # self.resize(400, 200)
        # 창 크기 고정
        self.stack.setFixedSize(800,600)

        self.stack.setObjectName("mainStack")
        # self.stack.setStyleSheet("#mainStack {background-image: url('/workspace/pyqt_delta/img/main2.png');}")
        # # QStackedWidget 은 전체 배경 / QWidget 배경 버튼 전부
        self.stack.setStyleSheet("QStackedWidget {background-image: url('/workspace/pyqt_delta/img/start.png');}")
    
        # stack을 보여줌. 
        self.stack.show()

    def showStartWindow(self):
        # Switch to the StartWindow widget
        self.stack.setCurrentWidget(self.start_window)


def main(args=None):
    rclpy.init(args=args)
    gui_node = GUI_Node()
    exit_code = gui_node.app.exec_()
    gui_node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
