import sys
import rclpy
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QIcon

from example import MyEx

from publisher import GUI_Node
from manual import MyApp
from home import MyHome
from move import MyMove
from info import MyInfo
from start import StartWindow
from calibration import MyCal


class AppManager(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('W-ECOBOT Application')
        self.setWindowIcon(QIcon('img/eth.png'))
        self.setFixedSize(800, 600)
        self.setStyleSheet("QStackedWidget {background-image: url('img/start.png');}")
        self.node = GUI_Node()  # GUI_Node 객체 생성
        self.initUI()
        
    def initUI(self):
        self.ex_app = MyEx(self.node)

        # MyApp, MyHome, MyMove, MyInfo 등 모든 페이지를 생성
        
        self.my_app = MyApp(self.node)  # MyApp 객체 생성 시 노드 객체 전달
        self.home_app = MyHome(self.node)  # MyHome 객체 생성 시 노드 객체 전달
        # self.move_app = MyMove(self.node)  # MyMove 객체 생성 시 노드 객체 전달
        self.info_app = MyInfo(self.node)  # MyInfo 객체 생성 시 노드 객체 전달
        self.move_app = None  # 초기에 None으로 설정 (애러서 버튼 호출 할때마다 새로운 창을 열기 위함)
        self.cal_app = MyCal(self.node)
        
        # StartWindow를 생성하고 스택에 추가
        self.start_window = StartWindow(parent=self)
        self.addWidget(self.start_window)

        # 나머지 페이지들도 스택에 추가
        self.addWidget(self.ex_app)
        self.addWidget(self.my_app)
        self.addWidget(self.home_app)
        # self.addWidget(self.move_app)
        self.addWidget(self.info_app)
        self.addWidget(self.cal_app)

        # 뒤로가기 버튼에서 돌아오는 길 지정
        self.ex_app.goToStartScreen.connect(self.gotoStart)
        self.my_app.goToStartScreen.connect(self.gotoStart)
        self.home_app.goToStartScreen.connect(self.gotoStart)
        # 
        self.info_app.goToStartScreen.connect(self.gotoStart)
        self.cal_app.goToStartScreen.connect(self.gotoStart)

    # 예제 페이지
    def gotoCalibration(self):
        self.setCurrentWidget(self.ex_app)

    # 시작 페이지
    def gotoStart(self):
        self.setCurrentWidget(self.start_window)

    # 메인 페이지
    def gotoMain(self):
        self.setCurrentWidget(self.my_app)
        
    # 호밍페이지
    def gotoHome(self):
        self.setCurrentWidget(self.home_app)

    # 무빙(수동)페이지
    def gotoMove(self):
        # self.setCurrentWidget(self.move_app)
        if self.move_app is None:
            # node = GUI_Node()  # 새로운 GUI_Node 객체 생성
            self.move_app = MyMove()  # MyMove 객체 생성 시 새로운 노드 객체 전달
            self.addWidget(self.move_app)  # 스택에 페이지 추가
    
        self.setCurrentWidget(self.move_app)
        self.move_app.goToStartScreen.connect(self.gotoStart)

    # 인포메이션 페이지
    def gotoInfo(self):
        self.setCurrentWidget(self.info_app)

    # 칼리브레이션 페이지
    def gotoCalibration(self):
        self.setCurrentWidget(self.cal_app)
        
        




    # 예제 폼
    def gotoExample(self):
        self.setCurrentWidget(self.ex_app)

if __name__ == '__main__':
    app = QApplication(sys.argv) # QApplication : 프로그램을 실행시켜주는 클래스
    rclpy.init(args=None)
    app_manager = AppManager()
    app_manager.show()
    sys.exit(app.exec_())
    rclpy.shutdown()
