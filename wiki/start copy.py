import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QStackedWidget
import main

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Start Window')
        startButton = QPushButton('Go to Main Application', self)
        startButton.clicked.connect(self.gotoMain)

        layout = QVBoxLayout()
        layout.addWidget(startButton)
        self.setLayout(layout)

    def gotoMain(self):
        main_window = self.parent().findChild(main.MyApp)
        self.parent().setCurrentWidget(main_window)

class MainApplication(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize main application (main.py)
        self.mainApp = main.MyApp(None)  # Assuming MyApp can handle 'None' as node
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.mainApp)

def start():
    app = QApplication(sys.argv)
    stack = QStackedWidget()

    start_window = StartWindow()
    main_application = MainApplication()

    stack.addWidget(start_window)
    stack.addWidget(main_application.mainApp)

    stack.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()
