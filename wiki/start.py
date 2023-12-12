import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QStackedWidget
import main
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point

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
        # self.mainApp = main.GUI_Node()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.mainApp)


class GUI_Node(Node):
    def __init__(self):
        super().__init__('gui_node')
        self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        pass


def start(args=None):
    rclpy.init(args=args)
    gui_node = GUI_Node()
    exit_code = gui_node.app.exec_()
    
    app = QApplication(sys.argv)
    stack = QStackedWidget()

    start_window = StartWindow()
    main_application = MainApplication()

    stack.addWidget(start_window)
    stack.addWidget(main_application.mainApp)

    stack.show()

    gui_node.destroy_node()
    rclpy.shutdown()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()
