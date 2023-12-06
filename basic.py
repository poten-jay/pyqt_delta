import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon

# function.py 에서 class 호출
from function import xyz_button

# 현재 좌표 값 받아오기
btn = xyz_button(13,24,33)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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

    # 버튼 
    def button(self):


        # zUp 버튼
        self.btnUp = QPushButton('Z-Up', self)
        self.btnUp.setGeometry(100, 20, 90, 30)  # 버튼 위치와 크기 설정
        self.btnUp.clicked.connect(self.zUp)

        # xUp 버튼
        self.btnLeft = QPushButton('X-Up', self)
        self.btnLeft.setGeometry(10, 70, 90, 30)  # 버튼 위치와 크기 설정
        self.btnLeft.clicked.connect(self.xUp)

        # xDown 버튼
        self.btnRight = QPushButton('X-Down', self)
        self.btnRight.setGeometry(190, 70, 90, 30)  # 버튼 위치와 크기 설정
        self.btnRight.clicked.connect(self.xDown)

        # yUp버튼
        self.btnLeft = QPushButton('Y-Up', self)
        self.btnLeft.setGeometry(10, 120, 90, 30)  # 버튼 위치와 크기 설정
        self.btnLeft.clicked.connect(self.yUp)

        # yDown 버튼
        self.btnRight = QPushButton('Y-Down', self)
        self.btnRight.setGeometry(190, 120, 90, 30)  # 버튼 위치와 크기 설정
        self.btnRight.clicked.connect(self.yDown)

        # zDown 버튼
        self.btnDown = QPushButton('Z-Down', self)
        self.btnDown.setGeometry(100, 170, 90, 30)  # 버튼 위치와 크기 설정
        self.btnDown.clicked.connect(self.zDown)

    
    def zUp(self):
        btn.z_up()
        print('Z Up', btn.input_z)
    
    def zDown(self):
        btn.z_down()
        print('Z Down', btn.input_z)

    def xUp(self):
        btn.x_up()
        print('X Up', btn.input_x)

    def xDown(self):
        btn.x_down()
        print('X Down', btn.input_x)

    def yUp(self):
        btn.y_up()
        print('Y Up', btn.input_y)

    def yDown(self):
        btn.y_down()
        print('Y Down', btn.input_y)

def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     sys.exit(app.exec_())

if __name__ == '__main__':
    main()
