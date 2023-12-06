import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

# function.py 에서 class 호출
from function import xyz_button

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.btn = xyz_button(13, 24, 33)  # 현재 좌표 값 받아오기
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('W-DELTABOT Application')
        self.center()
        self.setWindowIcon(QIcon('eth.png'))
        self.setFixedSize(800,500)
        self.button()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def button(self):
        # Z-Up 버튼
        self.btnUp = QPushButton('Z-Up', self)
        self.btnUp.setGeometry(100, 20, 90, 30)
        self.btnUp.pressed.connect(lambda: self.startTimer(self.btn.z_up))
        self.btnUp.released.connect(self.stopTimer)

        # X-Up 버튼
        self.btnLeft = QPushButton('X-Up', self)
        self.btnLeft.setGeometry(10, 70, 90, 30)
        self.btnLeft.pressed.connect(lambda: self.startTimer(self.btn.x_up))
        self.btnLeft.released.connect(self.stopTimer)

        # X-Down 버튼
        self.btnRight = QPushButton('X-Down', self)
        self.btnRight.setGeometry(190, 70, 90, 30)
        self.btnRight.pressed.connect(lambda: self.startTimer(self.btn.x_down))
        self.btnRight.released.connect(self.stopTimer)

        # Z-Down 버튼
        self.btnDown = QPushButton('Z-Down', self)
        self.btnDown.setGeometry(100, 170, 90, 30)
        self.btnDown.pressed.connect(lambda: self.startTimer(self.btn.z_down))
        self.btnDown.released.connect(self.stopTimer)

    def startTimer(self, action):
        self.timer.timeout.connect(action)
        self.timer.start(100)

    def stopTimer(self):
        self.timer.stop()
        self.timer.timeout.disconnect()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
