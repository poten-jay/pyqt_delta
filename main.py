import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QSize

# function.py 에서 class 호출
from function import xyz_button

# 현재 좌표 값 받아오기
x = 121
y = 331
z = 431

class MyApp(QWidget):
    # 현재 좌표 값 받아오기
    btn = xyz_button(x, y, z)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        
        self.initUI

    def initUI(self):
        self.setWindowTitle('W-DELTABOT Application')
        # 창 시작점 (center def 가져옴)
        self.center()
        # 창 타이틀 아이콘 - 윈도우에서는 가능
        self.setWindowIcon(QIcon('eth.png'))
        # self.resize(400, 200)
        # 창 크기 고정
        self.setFixedSize(800,500)

        # 버튼
        self.button()

        self.show()

    # 창 중앙으로 보내기
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 버튼 위치 및 사이즈 결정
    def button(self):
        # 타이머 설정
        # self.timer = QTimer(self)
        # self.timer.setInterval(100)  # 간격을 100밀리초로 설정

        imagePath = '/eth.png'
        if os.path.exists(imagePath):
            print("이미지 파일이 존재합니다.")
        else:
            print("이미지 파일이 존재하지 않습니다:", imagePath)

        icon = QIcon(imagePath)
        if not icon.isNull():
            print("아이콘이 성공적으로 로드되었습니다.")
        else:
            print("아이콘 로드 실패")

        # Z-Up 버튼
        self.btnZUp = QPushButton('', self)
        self.btnZUp.setGeometry(100, 20, 90, 30)
        self.btnZUp.setIcon(QIcon('/media/ssd/workspace/jay/pyqt_delta/eth.png'))  # 이미지 경로 설정
        self.btnZUp.setIconSize(QSize(80, 25))  # 아이콘 크기
        self.btnZUp.pressed.connect(lambda: self.startTimer(self.zUp))
        self.btnZUp.released.connect(self.stopTimer)

        # # Z-Up 버튼
        # self.btnZUp = QPushButton('Z-Up', self)
        # self.btnZUp.setGeometry(100, 20, 90, 30)
        # self.btnZUp.pressed.connect(lambda: self.startTimer(self.zUp))
        # self.btnZUp.released.connect(self.stopTimer)

        # Z-Down 버튼
        self.btnZDown = QPushButton('Z-Down', self)
        self.btnZDown.setGeometry(100, 170, 90, 30)
        self.btnZDown.pressed.connect(lambda: self.startTimer(self.zDown))
        self.btnZDown.released.connect(self.stopTimer)

        # X-Up 버튼
        self.btnXUp = QPushButton('X-Up', self)
        self.btnXUp.setGeometry(10, 70, 90, 30)
        self.btnXUp.pressed.connect(lambda: self.startTimer(self.xUp))
        self.btnXUp.released.connect(self.stopTimer)

        # X-Down 버튼
        self.btnXDown = QPushButton('X-Down', self)
        self.btnXDown.setGeometry(190, 120, 90, 30)
        self.btnXDown.pressed.connect(lambda: self.startTimer(self.xDown))
        self.btnXDown.released.connect(self.stopTimer)

        # Y-Up 버튼
        self.btnYUp = QPushButton('Y-Up', self)
        self.btnYUp.setGeometry(10, 120, 90, 30)
        self.btnYUp.pressed.connect(lambda: self.startTimer(self.yUp))
        self.btnYUp.released.connect(self.stopTimer)

        # Y-Down 버튼
        self.btnYDown = QPushButton('Y-Down', self)
        self.btnYDown.setGeometry(190, 70, 90, 30)
        self.btnYDown.pressed.connect(lambda: self.startTimer(self.yDown))
        self.btnYDown.released.connect(self.stopTimer)

    def startTimer(self, func):
        if self.timer.isActive():  # 타이머가 활성화되어 있다면 연결을 해제
            self.timer.timeout.disconnect()
        self.timer.timeout.connect(func)
        self.timer.start(100)
        
    def stopTimer(self):
        self.timer.stop()
        try:
            self.timer.timeout.disconnect()
        except TypeError:
            # 연결이 없을 경우 발생하는 TypeError를 처리
            pass

    def zUp(self):
        self.btn.z_up()
        self.btn.z_up()
        print('Z Up', self.btn.input_z)
    
    def zDown(self):
        self.btn.z_down()
        print('Z Down', self.btn.input_z)

    def xUp(self):
        self.btn.x_up()
        print('X Up', self.btn.input_x)

    def xDown(self):
        self.btn.x_down()
        print('X Down', self.btn.input_x)

    def yUp(self):
        self.btn.y_up()
        print('Y Up', self.btn.input_y)

    def yDown(self):
        self.btn.y_down()
        print('Y Down', self.btn.input_y)

def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
