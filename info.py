import sys
import os
import rclpy
from rclpy.node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QSize, Qt, pyqtSignal
from geometry_msgs.msg import Point

# function.py 에서 class 호출
from function import xyz_button

# setting.py 에서 값 호출
import setting

# 현재 좌표 값 받아오기
x = setting.x
y = setting.y
z = setting.z



class MyInfo(QWidget):
    goToStartScreen = pyqtSignal()

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.btn = xyz_button(node, x, y, z)
        self.initUI()
        self.timer = QTimer(self)
        # self.initUI

    def initUI(self):
######## 이미지 넣기 #######################################################
        original_pixmap = QPixmap("/workspace/pyqt_delta/img/test.png")
        scaled_pixmap = original_pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # QLabel 생성 및 QPixmap 설정
        lbl_img = QLabel(self)
        lbl_img.setPixmap(scaled_pixmap)
        lbl_img.setGeometry(0, 0, scaled_pixmap.width(), scaled_pixmap.height())
########################################################################
######## 이미지 추가 #######################################################
#         original_pixmap1 = QPixmap("/workspace/pyqt_delta/img/kbs1.png")
#         scaled_pixmap1 = original_pixmap1.scaled(800, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         # QLabel 생성 및 QPixmap 설정
#         lbl_img = QLabel(self)
#         lbl_img.setPixmap(scaled_pixmap1)
#         lbl_img.setGeometry(23, 20, scaled_pixmap1.width(), scaled_pixmap1.height())
# ########################################################################

        # 창 크기 고정
        self.setFixedSize(800,600)

        # lebel 정보 창

        # x,y,z 좌표 정보
        self.labelX = QLabel(f"X : {x}", self)
        self.labelX.setStyleSheet("Color : white")
        self.labelX.setGeometry(150, 120, 100, 30)
        self.labelY = QLabel(f"Y : {y}", self)
        self.labelY.setStyleSheet("Color : white")
        self.labelY.setGeometry(150, 150, 100, 30)
        self.labelZ = QLabel(f"Z : {z}", self)
        self.labelZ.setStyleSheet("Color : white")
        self.labelZ.setGeometry(150, 180, 100, 30)


        # workspace 정보
        self.workspace_x = QLabel(f"X_Max : {setting.x_max}", self)
        self.workspace_x.setStyleSheet("Color : white")
        self.workspace_x.setGeometry(150, 210, 100, 30)
        self.workspace_xn = QLabel(f"X_Min : {setting.x_min}", self)
        self.workspace_xn.setStyleSheet("Color : white")
        self.workspace_xn.setGeometry(150, 240, 100, 30)
        
        self.workspace_y = QLabel(f"Y_Max : {setting.y_max}", self)
        self.workspace_y.setStyleSheet("Color : white")
        self.workspace_y.setGeometry(150, 270, 100, 30)
        self.workspace_yn = QLabel(f"Y_Min : {setting.y_min}", self)
        self.workspace_yn.setStyleSheet("Color : white")
        self.workspace_yn.setGeometry(150, 300, 100, 30)
        
        self.workspace_z = QLabel(f"Z_Max : {setting.z_max}", self)
        self.workspace_z.setStyleSheet("Color : white")
        self.workspace_z.setGeometry(150, 330, 100, 30)
        self.workspace_zn = QLabel(f"Z_Min : {setting.z_min}", self)
        self.workspace_zn.setStyleSheet("Color : white")
        self.workspace_zn.setGeometry(150, 360, 100, 30)
        

        # ### 직접 입력 창들
        # # LineEdit for X value


        # # 버튼


        # 뒤로가기 버튼 (순서가 밀리면 안보일 수도 있음)
        self.button()
        self.show()


    # 버튼 위치 및 사이즈 결정
    def button(self):

        # 뒤로 가기 버튼
        self.btnback = QPushButton('<<', self)
        self.btnback.clicked.connect(self.goToStartScreen.emit)
        self.btnback.setGeometry(0, 528, 50, 50)
        # self.btnback.raise_()  # Raise the button to the top of the widget stack


    def onBackButtonClick(self):
        # Emit the signal when the button is clicked
        self.goToStartScreen.emit()



########### start.py를 실행하면 아래는 필요 없음 #####################

class GUI_Node(Node):
    def __init__(self):
        super().__init__('gui_node')
        self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)
        self.app = QApplication(sys.argv)
        self.gui = MyInfo(self)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        pass


def main(args=None):
    rclpy.init(args=args)
    gui_node = GUI_Node()

    exit_code = gui_node.app.exec_()

    gui_node.destroy_node()
    rclpy.shutdown()

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
