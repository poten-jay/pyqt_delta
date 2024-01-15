from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

class Page1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # (1) Page1 클래스의 생성자를 정의하고, 부모 위젯(parent)을 인자로 받습니다.

        self.button = QPushButton("Go to Page 2")  # (2) "Go to Page 2"라는 텍스트를 가진 버튼을 생성합니다.
        self.button.clicked.connect(self.go_to_page2)  # (3) 버튼 클릭 이벤트에 go_to_page2 메서드를 연결합니다.

        layout = QVBoxLayout()  # (4) 수직 레이아웃 객체를 생성합니다.
        layout.addWidget(self.button)  # (5) 버튼을 수직 레이아웃에 추가합니다.
        self.setLayout(layout)  # (6) 위젯의 레이아웃을 위에서 생성한 수직 레이아웃으로 설정합니다.

    def go_to_page2(self):
        self.parent().setCurrentIndex(1)  # (7) go_to_page2 메서드는 호출될 때 스택의 인덱스를 변경하여 페이지 2로 이동합니다.
