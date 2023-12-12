import sys
import os
import rclpy
from rclpy.node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QSize, Qt
from geometry_msgs.msg import Point
from main import GUI_Node



# main.py 연결
from main import MyApp 
from main import GUI_Node


class Start(QWidget):
    # 현재 좌표 값 받아오기
    # btn = xyz_button(x, y, z)

    def __init__(self):
        super().__init__()
        # rclpy.init(args=None)  # rclpy 환경 초기화
        self.initUI()

    def initUI(self):
        self.setWindowTitle('W-DELTABOT Application')
        # 창 시작점 (center def 가져옴)
        self.center()
        # 창 타이틀 아이콘 - 윈도우에서는 가능
        self.setWindowIcon(QIcon('/workspace/pyqt_delta/img/eth.png'))
        # self.resize(400, 200)
        # 창 크기 고정
        self.setFixedSize(800,600)

        # 배경 이미지 설정
        self.setBackgroundImage('/workspace/pyqt_delta/img/none.png')

        # 버튼
        self.button()

        self.show()

    # 창 중앙으로 보내기
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 

    # 배경 이미지
    def setBackgroundImage(self, imagePath):
        pixmap = QPixmap(imagePath)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)

    # 버튼 위치 및 사이즈 결정
    def button(self):
        # main 버튼
        self.btnmain = QPushButton('main', self)
        self.btnmain.setGeometry(0, 100, 90, 30)
        # self.btnmain.pressed.connect(lambda: self.startTimer(self.zUp))
        # main.py로 연결
        self.btnmain.clicked.connect(self.openMain)

    # # main.py 로 연결
    # def openMain(self):
    #     self.mainWindow = MyApp(QWidget)  # GUI_Node 객체 없이 MyApp 인스턴스를 생성합니다.
    #     self.mainWindow.show()  # MyApp 윈도우를 보여줍니다.

    # # main.py 로 연결
    # def openMain(self):
    #     node = GUI_Node()  # GUI_Node 객체를 생성합니다.
    #     self.mainWindow = MyApp(node)  # 생성한 GUI_Node 객체를 MyApp 인스턴스에 전달합니다.
    #     self.mainWindow.show()  # MyApp 윈도우를 보여줍니다.

    def openMain(self):
        if hasattr(self, 'mainWindow') and self.mainWindow.isVisible():
            # 이미 창이 열려있으면 추가로 열지 않음
            self.mainWindow.raise_()  # 창을 맨 앞으로 가져옴
            self.mainWindow.activateWindow()  # 창을 활성화
            return
        GUI_Node()
        # self.mainWindow = MyApp(node)
        # self.mainWindow.show()



def main():
    rclpy.init(args=None)  # rclpy 환경 초기화
    app = QApplication(sys.argv)
    ex = Start()
    ex.show()  # Make sure to call show() to display the window
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()