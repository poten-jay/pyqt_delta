import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('W-DELTABOT Application')
        # 창 시작점 (center def 가져옴)
        self.center()
        # 창 타이틀 아이콘
        self.setWindowIcon(QIcon('eth.png'))
        # self.resize(400, 200)
        # 창 크기 고정
        self.setFixedSize(800,500)
        self.show()

    # 창 중앙으로 보내기
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

