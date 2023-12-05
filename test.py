import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        hLayout = QHBoxLayout()

        # Up 버튼
        self.btnUp = QPushButton('Up', self)
        self.btnUp.clicked.connect(self.onUp)
        mainLayout.addWidget(self.btnUp)

        # Left 버튼
        self.btnLeft = QPushButton('Left', self)
        self.btnLeft.clicked.connect(self.onLeft)
        hLayout.addWidget(self.btnLeft)

        # Right 버튼
        self.btnRight = QPushButton('Right', self)
        self.btnRight.clicked.connect(self.onRight)
        hLayout.addWidget(self.btnRight)

        # Down 버튼
        self.btnDown = QPushButton('Down', self)
        self.btnDown.clicked.connect(self.onDown)
        mainLayout.addLayout(hLayout)
        mainLayout.addWidget(self.btnDown)

        self.setLayout(mainLayout)
        self.setWindowTitle('Arrow Key Buttons')
        self.setGeometry(300, 300, 200, 150)
        self.show()

    def onUp(self):
        print('Up arrow pressed')

    def onDown(self):
        print('Down arrow pressed')

    def onLeft(self):
        print('Left arrow pressed')

    def onRight(self):
        print('Right arrow pressed')

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
