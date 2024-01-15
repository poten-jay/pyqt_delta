import sys  # (1) sys 모듈을 가져옵니다.
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget  # (2) 필요한 PyQt5 위젯 및 클래스들을 가져옵니다.
from page1 import Page1  # (3) Page1 모듈을 가져옵니다.
from page2 import Page2  # (3) Page2 모듈을 가져옵니다.
from page3 import Page3

class MainWindow(QMainWindow):  # (4) QMainWindow 클래스를 상속받는 MainWindow 클래스를 정의합니다.
    def __init__(self):  # (5) 생성자 메서드를 정의합니다.
        super().__init__()  # (6) 부모 클래스인 QMainWindow의 생성자를 호출합니다.

        self.setWindowTitle("Stacked Pages Example")  # (7) 주 창의 제목을 설정합니다.
        self.setGeometry(100, 100, 400, 300)  # (8) 주 창의 초기 위치와 크기를 설정합니다.
###
        self.central_widget = QWidget(self)  # (9) 중앙 위젯을 생성합니다.
        self.setCentralWidget(self.central_widget)  # (10) 주 창의 중앙 위젯으로 central_widget을 설정합니다.

        self.stack = QStackedWidget(self.central_widget)  # (11) QStackedWidget 위젯을 생성합니다.

        self.page1 = Page1(self)  # (12) Page1 클래스의 인스턴스를 생성합니다.
        self.page2 = Page2(self)  # (13) Page2 클래스의 인스턴스를 생성합니다.
        self.page3 = Page3(self)

        self.stack.addWidget(self.page1)  # (14) 스택 위젯에 첫 번째 페이지를 추가합니다.
        self.stack.addWidget(self.page2)  # (15) 스택 위젯에 두 번째 페이지를 추가합니다.
        self.stack.addWidget(self.page3)

        layout = QVBoxLayout(self.central_widget)  # (16) 중앙 위젯에 수직 레이아웃을 설정합니다.
        layout.addWidget(self.stack)  # (17) 스택 위젯을 중앙 위젯에 추가합니다.

if __name__ == "__main__":  # (18) 스크립트가 직접 실행될 때 아래의 코드 블록을 실행합니다.
    app = QApplication(sys.argv)  # (19) PyQt5 어플리케이션 객체를 생성합니다.
    main_window = MainWindow()  # (20) MainWindow 클래스의 인스턴스를 생성합니다.
    main_window.show()  # (21) 주 창을 표시합니다.
    sys.exit(app.exec_())  # (22) 어플리케이션을 실행하고, 어플리케이션이 종료되면 시스템을 종료합니다.


















