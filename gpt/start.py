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



class StartWindow(QWidget):
    def __init__(self, MyApp):
        super().__init__()
        self.initUI()
        self.MyApp = MyApp
        

    def initUI(self):
        # 창 제목
        # self.setWindowTitle('Start Window')
        # 이 부분이 child로 존재하므로 parents 에 작성을 해야 적용이 됨

####### 이미지 삽입 ################################################################

        original_pixmap = QPixmap("/workspace/pyqt_delta/img/start.png")
        scaled_pixmap = original_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # QLabel 생성 및 QPixmap 설정
        lbl_img = QLabel(self)
        lbl_img.setPixmap(scaled_pixmap)
        lbl_img.setGeometry(0, 0, scaled_pixmap.width(), scaled_pixmap.height())

####### 버튼1 ######################################################################
        startButton = QPushButton('Go1', self)
        startButton.clicked.connect(self.gotoMain)
        startButton.setGeometry(10, 10, 50, 50)

####### 버튼2 ######################################################################
        homingButton = QPushButton('Go2', self)
        homingButton.clicked.connect(self.gotoHome)
        homingButton.setGeometry(10, 100, 50, 50)

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

####### main 으로 #################################################################

    def gotoHome(self):
        home_window = self.parent().findChild(MyHome)
        self.parent().setCurrentWidget(home_window)

####### 시간 #################################################################
    def update_time(self):
        # 현재 시간을 가져와서 QLabel에 표시
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(current_time)






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

        # 추가할 page 불러옴
        # ~~~~~~~~~~~~~~




        # Start page 불러옴. 여기서 Child page들이 필요함
        self.start_window = StartWindow(self.mainApp)

        # stack에 위젯을 추가함. 
        self.stack.addWidget(self.start_window)
        self.stack.addWidget(self.mainApp)
        self.stack.addWidget(self.homeApp)




        # stack의 타이틀을 설정함 (예: 첫 번째 위젯이 표시될 때) - 부모에 설정
        self.stack.setWindowTitle('W-DELTA BOT Application')
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
