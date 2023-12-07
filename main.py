import sys
import os
import rclpy
from rclpy.node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QSize, Qt
from geometry_msgs.msg import Point

# function.py 에서 class 호출
from function import xyz_button

# 현재 좌표 값 받아오기
x = 0
y = 0
z = 350

class MyApp(QWidget):
    # 현재 좌표 값 받아오기
    # btn = xyz_button(x, y, z)

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.btn = xyz_button(node, x, y, z)
        self.initUI()
        self.timer = QTimer(self)
        # self.initUI

    def initUI(self):
        self.setWindowTitle('W-DELTABOT Application')
        # 창 시작점 (center def 가져옴)
        self.center()
        # 창 타이틀 아이콘 - 윈도우에서는 가능
        self.setWindowIcon(QIcon('/workspace/pyqt_delta/img/eth.png'))
        # self.resize(400, 200)
        # 창 크기 고정
        self.setFixedSize(800,600)

        # 화면에 표시되는 xyz 좌표
        self.labelX = QLabel(f"{x}", self)
        self.labelX.setStyleSheet("Color : white")
        self.labelX.setAlignment(Qt.AlignRight)
        self.labelX.setGeometry(275, 445, 100, 30)  # Adjust position and size as needed
        self.labelY = QLabel(f"{y}", self)
        self.labelY.setStyleSheet("Color : white")
        self.labelY.setAlignment(Qt.AlignRight)
        self.labelY.setGeometry(430, 445, 100, 30)  # Adjust position and size as needed
        self.labelZ = QLabel(f"{z}", self)
        self.labelZ.setStyleSheet("Color : white")
        self.labelZ.setAlignment(Qt.AlignRight)
        self.labelZ.setGeometry(590, 445, 100, 30)  # Adjust position and size as needed

        # 배경 이미지 설정
        self.setBackgroundImage('/workspace/pyqt_delta/img/main2.png')

        # 버튼
        self.button()

        self.show()

    # 창 중앙으로 보내기
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 

    def setBackgroundImage(self, imagePath):
        pixmap = QPixmap(imagePath)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)

    # x,y,z 값 창 업데이트
    def updateLabels(self):
        # Update the labels with the current XYZ values
        self.labelX.setText(f'{self.btn.input_x}')
        self.labelY.setText(f'{self.btn.input_y}')
        self.labelZ.setText(f'{self.btn.input_z}')


    # 버튼 위치 및 사이즈 결정
    def button(self):

        # Z-Up 버튼
        self.btnZUp = QPushButton('', self)
        self.btnZUp.setGeometry(135, 100, 60, 60)
        self.btnZUp.setIcon(QIcon('/workspace/pyqt_delta/img/kbs1.png'))  # 이미지 경로 설정
        self.btnZUp.setIconSize(QSize(59, 59))  # 아이콘 크기
        self.btnZUp.pressed.connect(lambda: self.startTimer(self.zUp))
        self.btnZUp.released.connect(self.stopTimer)

        # # Z-Up 버튼
        # self.btnZUp = QPushButton('Z-Up', self)
        # self.btnZUp.setGeometry(100, 20, 90, 30)
        # self.btnZUp.pressed.connect(lambda: self.startTimer(self.zUp))
        # self.btnZUp.released.connect(self.stopTimer)

        # Z-Down 버튼
        self.btnZDown = QPushButton('Z-Dw', self)
        self.btnZDown.setGeometry(135, 280, 60, 60)
        self.btnZDown.pressed.connect(lambda: self.startTimer(self.zDown))
        self.btnZDown.released.connect(self.stopTimer)

        # X-Up 버튼
        self.btnXUp = QPushButton('X-Up', self)
        self.btnXUp.setGeometry(75, 160, 60, 60)
        self.btnXUp.pressed.connect(lambda: self.startTimer(self.xUp))
        self.btnXUp.released.connect(self.stopTimer)

        # X-Down 버튼
        self.btnXDown = QPushButton('X-Dw', self)
        self.btnXDown.setGeometry(195, 220, 60, 60)
        self.btnXDown.pressed.connect(lambda: self.startTimer(self.xDown))
        self.btnXDown.released.connect(self.stopTimer)

        # Y-Up 버튼
        self.btnYUp = QPushButton('Y-Up', self)
        self.btnYUp.setGeometry(75, 220, 60, 60)
        self.btnYUp.pressed.connect(lambda: self.startTimer(self.yUp))
        self.btnYUp.released.connect(self.stopTimer)

        # Y-Down 버튼
        self.btnYDown = QPushButton('Y-Dw', self)
        self.btnYDown.setGeometry(195, 160, 60, 60)
        self.btnYDown.pressed.connect(lambda: self.startTimer(self.yDown))
        self.btnYDown.released.connect(self.stopTimer)
        
        # Initially disable XYZ buttons
        self.btnZUp.setDisabled(True)
        self.btnZDown.setDisabled(True)
        self.btnXUp.setDisabled(True)
        self.btnXDown.setDisabled(True)
        self.btnYUp.setDisabled(True)
        self.btnYDown.setDisabled(True)

        # Start Button
        self.btnStart = QPushButton('Start', self)
        self.btnStart.setGeometry(75, 515, 80, 50)  # Adjust as needed
        self.btnStart.clicked.connect(self.startOperation)

        # Stop Button
        self.btnStop = QPushButton('Stop', self)
        self.btnStop.setGeometry(175, 515, 80, 50)  # Adjust as needed
        self.btnStop.clicked.connect(self.stopOperation)


    def startTimer(self, func):
        if self.timer.isActive():  # 타이머가 활성화되어 있다면 연결을 해제
            self.timer.timeout.disconnect()
        self.timer.timeout.connect(func)
        self.timer.start(300) # 1000 밀리초 = 1초
        
    def stopTimer(self):
        self.timer.stop()
        try:
            self.timer.timeout.disconnect()
        except TypeError:
            # 연결이 없을 경우 발생하는 TypeError를 처리
            pass

    # start 버튼 누르면 수동 번튼 활성화
    def startOperation(self):
        # Enable XYZ buttons
        self.btnZUp.setDisabled(False)
        self.btnZDown.setDisabled(False)
        self.btnXUp.setDisabled(False)
        self.btnXDown.setDisabled(False)
        self.btnYUp.setDisabled(False)
        self.btnYDown.setDisabled(False)
        print("Operation started")

    # stop 누르면 비활성화
    def stopOperation(self):
        # Disable XYZ buttons
        self.btnZUp.setDisabled(True)
        self.btnZDown.setDisabled(True)
        self.btnXUp.setDisabled(True)
        self.btnXDown.setDisabled(True)
        self.btnYUp.setDisabled(True)
        self.btnYDown.setDisabled(True)
        print("Operation stopped")

    def zUp(self):
        self.btn.z_up()
        self.updateLabels() # 화면에 보이는 좌표 업데이트
        print('Z Up', self.btn.input_z)
    
    def zDown(self):
        self.btn.z_down()
        self.updateLabels()
        print('Z Down', self.btn.input_z)

    def xUp(self):
        self.btn.x_up()
        self.updateLabels()
        print('X Up', self.btn.input_x)

    def xDown(self):
        self.btn.x_down()
        self.updateLabels()
        print('X Down', self.btn.input_x)

    def yUp(self):
        self.btn.y_up()
        self.updateLabels()
        print('Y Up', self.btn.input_y)

    def yDown(self):
        self.btn.y_down()
        self.updateLabels()
        print('Y Down', self.btn.input_y)

class GUI_Node(Node):
    def __init__(self):
        super().__init__('gui_node')
        self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)
        self.app = QApplication(sys.argv)
        self.gui = MyApp(self)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        pass


def main(args=None):
    rclpy.init(args=args)
    gui_node = GUI_Node()

    exit_code = gui_node.app.exec_()

    gui_node.destroy_node()
    rclpy.shutdown()

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
