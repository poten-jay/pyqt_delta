import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QTextEdit, QStackedWidget
import receive
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QPixmap

class MyWindow(QMainWindow):
    def __init__(self, info_lines):
        super().__init__()
        self.info_lines = info_lines
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Info Display Example")
        self.setGeometry(100, 100, 400, 400)

        # 메인 위젯
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 버튼을 포함한 레이아웃
        self.layout = QVBoxLayout(self.central_widget)

        # 새로고침 버튼
        self.reload_button = QPushButton("reee", self)
        self.reload_button.clicked.connect(self.reloadWidget)
        self.layout.addWidget(self.reload_button)

        # QStackedWidget
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # 페이지 1: 정보 표시
        self.page_info = QWidget(self)
        self.layout_info = QVBoxLayout(self.page_info)

        # QLabel로 정보 표시
        self.info_label = QLabel(self.page_info)
        self.layout_info.addWidget(self.info_label)

        # 페이지 2: 텍스트 파일 내용 보기
        self.page_text = QWidget(self)
        self.layout_text = QVBoxLayout(self.page_text)

        # QTextEdit로 텍스트 파일 내용 표시
        self.text_edit = QTextEdit(self.page_text)
        self.text_edit.setReadOnly(True)
        self.layout_text.addWidget(self.text_edit)

        # QStackedWidget에 페이지 추가
        self.stacked_widget.addWidget(self.page_info)
        self.stacked_widget.addWidget(self.page_text)

        # 전환 버튼
        self.switch_button = QPushButton("swich", self)
        self.switch_button.clicked.connect(self.switchPage)
        self.layout.addWidget(self.switch_button)

        # 초기 정보 표시
        self.displayInfo()
        print('main_display')

        self.loadIoImages()  # (1) loadIoImages 메서드를 초기화 단계에서 호출합니다.

    def loadIoImages(self):
        if receive.robot == True:
            self.input_image(40, 40, 17, 17, "img/on.png")
            print("OK")
        else:
            self.input_image(40, 40, 17, 17, "img/off.png")
            print("No")

    def input_image(self, x, y, w, h, img_path):
        pixmap = QPixmap(img_path)
        scaled_pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # QLabel 생성 및 QPixmap 설정
        lbl_img = QLabel(self)
        lbl_img.setPixmap(scaled_pixmap)
        lbl_img.setGeometry(x, y, scaled_pixmap.width(), scaled_pixmap.height())

    def displayInfo(self):
        print('display Info')
        info_str = "<br>".join(self.info_lines)
        self.info_label.setText(info_str)

        # QTextEdit에도 정보 표시
        self.text_edit.setPlainText("\n".join(self.info_lines))

    def reloadWidget(self):
        print('reload widget')
        # 파일 다시 읽어오고 정보 표시
        with open("document/test.txt", "r") as file:
            print('reload read text')
            self.info_lines = file.read().splitlines()
        self.displayInfo()
        print('reload _ diaplay')
        print('=============================')

    def switchPage(self):
        print('switch page')
        # 현재 페이지의 인덱스를 확인하고 다음 페이지로 전환
        current_page_index = self.stacked_widget.currentIndex()
        next_page_index = (current_page_index + 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(next_page_index)

        # 전환된 페이지에서도 새로고침 실행
        self.reloadWidget()
        print('========================')

def main():
    app = QApplication(sys.argv)
    
    # home_list.txt 파일에서 정보 읽기
    with open("document/test.txt", "r") as file:
        print('main_read text')
        info_data = file.read().splitlines()

    print('pre window --------')
    window = MyWindow(info_data)
    print('window -> my window (info_data)')
    window.show()
    print('window show()')
    print('============================================')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
