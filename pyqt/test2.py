import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.timer.timeout.connect(self.buttonPressed)

        mainLayout = QVBoxLayout()
        hLayout = QHBoxLayout()

        # Up 버튼
        self.btnUp = QPushButton('Up', self)
        self.btnUp.pressed.connect(lambda: self.startTimer('Up'))
        self.btnUp.released.connect(self.stopTimer)
        mainLayout.addWidget(self.btnUp)

        # Left 버튼
        self.btnLeft = QPushButton('Left', self)
        self.btnLeft.pressed.connect(lambda: self.startTimer('Left'))
        self.btnLeft.released.connect(self.stopTimer)
        hLayout.addWidget(self.btnLeft)

        # Right 버튼
        self.btnRight = QPushButton('Right', self)
        self.btnRight.pressed.connect(lambda: self.startTimer('Right'))
        self.btnRight.released.connect(self.stopTimer)
        hLayout.addWidget(self.btnRight)

        # Down 버튼
        self.btnDown = QPushButton('Down', self)
        self.btnDown.pressed.connect(lambda: self.startTimer('Down'))
        self.btnDown.released.connect(self.stopTimer)
        mainLayout.addLayout(hLayout)
        mainLayout.addWidget(self.btnDown)

        self.setLayout(mainLayout)
        self.setWindowTitle('Arrow Key Buttons')
        self.setGeometry(300, 300, 200, 150)
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
