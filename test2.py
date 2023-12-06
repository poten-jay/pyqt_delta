import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

# function.py 에서 class 호출
from function import xyz_button

# 현재 좌표 값 받아오기
btn = xyz_button(13,24,33)

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.timer.timeout.connect(self.buttonPressed)

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

        # mainLayout = QVBoxLayout()
        # hLayout = QHBoxLayout()

    # 창 중앙으로 보내기
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 버튼 
    def button(self):

        # zUp 버튼
        self.btnUp = QPushButton('Z-Up', self)
        self.btnUp.setGeometry(100, 20, 90, 30)  # 버튼 위치와 크기 설정
        self.btnUp.pressed.connect(lambda: self.startTimer(self.zUp))
        self.btnUp.released.connect(self.stopTimer)

        # xUp 버튼
        self.btnLeft = QPushButton('X-Up', self)
        self.btnLeft.setGeometry(10, 70, 90, 30)  # 버튼 위치와 크기 설정
        self.btnLeft.pressed.connect(lambda: self.startTimer('Left'))
        self.btnLeft.released.connect(self.stopTimer)

        # xDown 버튼
        self.btnRight = QPushButton('X-Down', self)
        self.btnRight.setGeometry(190, 70, 90, 30)  # 버튼 위치와 크기 설정
        self.btnRight.pressed.connect(lambda: self.startTimer('Right'))
        self.btnRight.released.connect(self.stopTimer)

        # zDown 버튼
        self.btnDown = QPushButton('Z-Down', self)
        self.btnDown.setGeometry(100, 170, 90, 30)  # 버튼 위치와 크기 설정
        self.btnDown.pressed.connect(lambda: self.startTimer('Down'))
        self.btnDown.released.connect(self.stopTimer)

        self.show()

    def startTimer(self, direction):
        self.direction = direction
        self.timer.start(100)  # 100ms마다 buttonPressed 호출

    def stopTimer(self):
        self.timer.stop()


    def buttonPressed(self):
        print(f'{self.direction} arrow pressed')

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
