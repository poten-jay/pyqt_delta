import sys
import os
import rclpy
from rclpy.node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QSize, Qt, pyqtSignal
from geometry_msgs.msg import Point
from shared_updates import global_update_xyz


from home import MyHome
# function.py 에서 class 호출
from function import xyz_button

# setting.py 에서 값 호출
import setting

# 현재 좌표 값 받아오기
x = setting.x
y = setting.y
z = setting.z

class MyApp(QWidget):
    # 현재 좌표 값 받아오기
    # btn = xyz_button(x, y, z)
    goToStartScreen = pyqtSignal()

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.btn = xyz_button(node, x, y, z)
        self.initUI()
        self.timer = QTimer(self)
        self.initUI

    def initUI(self):
        # # 배경 이미지 설정
        # self.setStyleSheet("QWidget {background-image: url('/workspace/pyqt_delta/img/main2.png');}")


        # 이미지 넣기
        original_pixmap = QPixmap("/workspace/pyqt_delta/img/main2.png")
        scaled_pixmap = original_pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # QLabel 생성 및 QPixmap 설정
        lbl_img = QLabel(self)
        lbl_img.setPixmap(scaled_pixmap)
        lbl_img.setGeometry(0, 0, scaled_pixmap.width(), scaled_pixmap.height())

        # 창 크기 고정
        self.setFixedSize(800,600)

        # 화면에 표시되는 xyz 좌표
        self.labelX = QLabel(f"{x}", self)
        self.labelX.setStyleSheet("Color : white")
        self.labelX.setAlignment(Qt.AlignRight)
        self.labelX.setGeometry(275, 445, 100, 30)  # Adjust position and size as needed
        self.labelY = QLabel(f"{y}", self)
        self.labelY.setStyleSheet("Color : white")
        self.labelY.setAlignment(Qt.AlignRight)
        self.labelY.setGeometry(430, 445, 100, 30)  # Adjust position and size as needed
        self.labelZ = QLabel(f"{z}", self)
        self.labelZ.setStyleSheet("Color : white")
        self.labelZ.setAlignment(Qt.AlignRight)
        self.labelZ.setGeometry(590, 445, 100, 30)  # Adjust position and size as needed


        ### 직접 입력 창들
        # LineEdit for X value
        self.lineEditX = QLineEdit(self)
        self.lineEditX.setGeometry(305, 510, 90, 25)  # Adjust position and size as needed
        self.lineEditX.setText(str(x))
        self.lineEditX.setAlignment(Qt.AlignRight) # 우측정렬
        # LineEdit for Y value
        self.lineEditY = QLineEdit(self)
        self.lineEditY.setGeometry(460, 510, 90, 25)  # Adjust position and size as needed
        self.lineEditY.setText(str(y))
        self.lineEditY.setAlignment(Qt.AlignRight)
        # LineEdit for Z value
        self.lineEditZ = QLineEdit(self)
        self.lineEditZ.setGeometry(615, 510, 90, 25)  # Adjust position and size as needed
        self.lineEditZ.setText(str(z))
        self.lineEditZ.setAlignment(Qt.AlignRight)
        # Update Button
        self.btnUpdate = QPushButton('Run', self)
        self.btnUpdate.setGeometry(680, 540, 50, 30)  # Adjust as needed
        self.btnUpdate.clicked.connect(self.updateXYZ)
        # Reset Button
        self.btnReset = QPushButton('Reset', self)
        self.btnReset.setGeometry(615, 540, 50, 30)  # Adjust position and size as needed
        self.btnReset.clicked.connect(self.resetFields)

        # Create a QLabel to display the image
        self.imageLabel = QLabel(self)
        pixmap = QPixmap('/media/ssd/workspace/jay/pyqt_delta/img/kbs1.png')
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.resize(pixmap.width(), pixmap.height())

        # Position the label where you want the image to appear
        self.imageLabel.move(100, 100)  # Adjust the position as needed


        # 버튼
        self.button()

        self.show()

    # 창 중앙으로 보내기
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 

    def setBackgroundImage(self, imagePath):
        pixmap = QPixmap(imagePath)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)

    # x,y,z 값 창 업데이트
    def updateLabels(self):
        # xzy 값 한도에서 붉게 변경
        if self.btn.input_x == setting.x_max or self.btn.input_x == setting.x_min:
            self.labelX.setStyleSheet("Color : red")
            self.labelX.setText(f'Limit {self.btn.input_x}')
            # MyHome.initUI.labelX.setText(f'Limit {self.btn.input_x}')
        else:
            self.labelX.setStyleSheet("Color : white")
            self.labelX.setText(f'{self.btn.input_x}')
        
        if self.btn.input_y == setting.y_max or self.btn.input_y == setting.y_min:
            self.labelY.setStyleSheet("Color : red")
            self.labelY.setText(f'Limit {self.btn.input_y}')
        else:
            self.labelY.setStyleSheet("Color : white")
            self.labelY.setText(f'{self.btn.input_y}')

        if self.btn.input_z == setting.z_max or self.btn.input_z == setting.z_min:
            self.labelZ.setStyleSheet("Color : red")
            self.labelZ.setText(f'Limit {self.btn.input_z}')
        else:
            self.labelZ.setStyleSheet("Color : white")
            self.labelZ.setText(f'{self.btn.input_z}')

        # Update the labels with the current XYZ values
        # self.labelX.setText(f'{self.btn.input_x}')
        # self.labelY.setText(f'{self.btn.input_y}')
        # self.labelZ.setText(f'{self.btn.input_z}')


    # 버튼 위치 및 사이즈 결정
    def button(self):

        self.btnback = QPushButton('<<', self)
        self.btnback.clicked.connect(self.goToStartScreen.emit)
        self.btnback.setGeometry(10, 10, 50, 50)
        # self.btnback.clicked.connect(self.onBackButtonClick)
        # self.btnback.clicked.connect(self.goBack.emit)

        # Z-Up 버튼
        self.btnZUp = QPushButton('', self)
        self.btnZUp.setGeometry(135, 100, 60, 60)
        self.btnZUp.setIcon(QIcon('/workspace/pyqt_delta/img/zu.png'))  # 이미지 경로 설정
        self.btnZUp.setIconSize(QSize(60, 60))  # 아이콘 크기
        self.btnZUp.pressed.connect(lambda: self.startTimer(self.zUp))
        self.btnZUp.released.connect(self.stopTimer)

        # # Z-Up 버튼
        # self.btnZUp = QPushButton('Z-Up', self)
        # self.btnZUp.setGeometry(100, 20, 90, 30)
        # self.btnZUp.pressed.connect(lambda: self.startTimer(self.zUp))
        # self.btnZUp.released.connect(self.stopTimer)

        # Z-Down 버튼
        self.btnZDown = QPushButton('', self)
        self.btnZDown.setGeometry(135, 280, 60, 60)
        self.btnZDown.setIcon(QIcon('/workspace/pyqt_delta/img/zd.png'))  # 이미지 경로 설정
        self.btnZDown.setIconSize(QSize(60, 60))  # 아이콘 크기
        self.btnZDown.pressed.connect(lambda: self.startTimer(self.zDown))
        self.btnZDown.released.connect(self.stopTimer)

        # X-Up 버튼
        self.btnXUp = QPushButton('', self)
        self.btnXUp.setGeometry(75, 160, 60, 60)
        self.btnXUp.setIcon(QIcon('/workspace/pyqt_delta/img/xu.png'))  # 이미지 경로 설정
        self.btnXUp.setIconSize(QSize(60, 60))  # 아이콘 크기
        self.btnXUp.pressed.connect(lambda: self.startTimer(self.xUp))
        self.btnXUp.released.connect(self.stopTimer)

        # X-Down 버튼
        self.btnXDown = QPushButton('', self)
        self.btnXDown.setGeometry(195, 220, 60, 60)
        self.btnXDown.setIcon(QIcon('/workspace/pyqt_delta/img/xd.png'))  # 이미지 경로 설정
        self.btnXDown.setIconSize(QSize(60, 60))  # 아이콘 크기
        self.btnXDown.pressed.connect(lambda: self.startTimer(self.xDown))
        self.btnXDown.released.connect(self.stopTimer)

        # Y-Up 버튼
        self.btnYUp = QPushButton('', self)
        self.btnYUp.setGeometry(75, 220, 60, 60)
        self.btnYUp.setIcon(QIcon('/workspace/pyqt_delta/img/yu.png'))  # 이미지 경로 설정
        self.btnYUp.setIconSize(QSize(60, 60))  # 아이콘 크기
        self.btnYUp.pressed.connect(lambda: self.startTimer(self.yUp))
        self.btnYUp.released.connect(self.stopTimer)

        # Y-Down 버튼
        self.btnYDown = QPushButton('', self)
        self.btnYDown.setGeometry(195, 160, 60, 60)
        self.btnYDown.setIcon(QIcon('/workspace/pyqt_delta/img/yd.png'))  # 이미지 경로 설정
        self.btnYDown.setIconSize(QSize(60, 60))  # 아이콘 크기
        self.btnYDown.pressed.connect(lambda: self.startTimer(self.yDown))
        self.btnYDown.released.connect(self.stopTimer)
        
        # Initially disable XYZ buttons
        self.btnZUp.setDisabled(True)
        self.btnZDown.setDisabled(True)
        self.btnXUp.setDisabled(True)
        self.btnXDown.setDisabled(True)
        self.btnYUp.setDisabled(True)
        self.btnYDown.setDisabled(True)
        self.btnUpdate.setDisabled(True)
        self.btnReset.setDisabled(True)
        

        # Start Button
        self.btnStart = QPushButton('Start', self)
        self.btnStart.setGeometry(75, 515, 80, 50)  # Adjust as needed
        self.btnStart.clicked.connect(self.startOperation)

        # Stop Button
        self.btnStop = QPushButton('Stop', self)
        self.btnStop.setGeometry(175, 515, 80, 50)  # Adjust as needed
        self.btnStop.clicked.connect(self.stopOperation)

    def onBackButtonClick(self):
        # Emit the signal when the button is clicked
        self.goToStartScreen.emit()

    def updateXYZ(self):
        # Read values from LineEdits and update XYZ
        try:
            x_val = float(self.lineEditX.text())
            y_val = float(self.lineEditY.text())
            z_val = float(self.lineEditZ.text())
            
            # Add any necessary validation for range
            if setting.x_min <= x_val <= setting.x_max and \
               setting.y_min <= y_val <= setting.y_max and \
               setting.z_min <= z_val <= setting.z_max:
                self.btn.input_x = x_val
                self.btn.input_y = y_val
                self.btn.input_z = z_val
                self.updateLabels()
                MyApp.updateLabels()
                MyHome.updateLabels()
                self.btn.publish_xyz()
                
                # Add any other necessary updates or method calls
            else:
                # Handle out of range values
                print("Values out of range")
                self.lineEditX.setText("Out of Rnage")
                self.lineEditX.setStyleSheet("color: red;")
                self.lineEditX.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.lineEditY.setText("Out of Rnage")
                self.lineEditY.setStyleSheet("color: red;")
                self.lineEditY.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.lineEditZ.setText("Out of Rnage")
                self.lineEditZ.setStyleSheet("color: red;")
                self.lineEditZ.setAlignment(Qt.AlignRight)
        except ValueError:
            # Handle invalid input
            print("Invalid input")

    # 직접 입력창 리셋
    def resetFields(self):
        # Reset the QLineEdit fields to initial settings
        self.lineEditX.setText(str(setting.x))
        self.lineEditY.setText(str(setting.y))
        self.lineEditZ.setText(str(setting.z))
        # Optionally, reset the style if it's changed when values are out of range
        self.lineEditX.setStyleSheet("color: black;")
        self.lineEditY.setStyleSheet("color: black;")
        self.lineEditZ.setStyleSheet("color: black;")


    def startTimer(self, func):
        if self.timer.isActive():  # 타이머가 활성화되어 있다면 연결을 해제
            self.timer.timeout.disconnect()
        self.timer.timeout.connect(func)
        self.timer.start(setting.ms) # 1000 밀리초 = 1초
        
    def stopTimer(self):
        self.timer.stop()
        try:
            self.timer.timeout.disconnect()
        except TypeError:
            # 연결이 없을 경우 발생하는 TypeError를 처리
            pass

    # start 버튼 누르면 수동 번튼 활성화
    def startOperation(self):
        # Increment initial XYZ values by 10
        self.btn.input_x = x
        self.btn.input_y = y
        self.btn.input_z = z

        self.btn.publish_xyz()

        # Update labels with new values
        self.updateLabels()

        # Enable XYZ buttons
        self.btnZUp.setDisabled(False)
        self.btnZDown.setDisabled(False)
        self.btnXUp.setDisabled(False)
        self.btnXDown.setDisabled(False)
        self.btnYUp.setDisabled(False)
        self.btnYDown.setDisabled(False)
        self.btnUpdate.setDisabled(False)
        self.btnReset.setDisabled(False)
        print("Operation started")

#  # Update Button
#         self.btnUpdate = QPushButton('>', self)
#         self.btnUpdate.setGeometry(750, 510, 25, 25)  # Adjust as needed
#         self.btnUpdate.clicked.connect(self.updateXYZ)

    # stop 누르면 비활성화
    def stopOperation(self):
        # Disable XYZ buttons
        self.btnZUp.setDisabled(True)
        self.btnZDown.setDisabled(True)
        self.btnXUp.setDisabled(True)
        self.btnXDown.setDisabled(True)
        self.btnYUp.setDisabled(True)
        self.btnYDown.setDisabled(True)
        self.btnUpdate.setDisabled(True)
        self.btnReset.setDisabled(True)
        print("Operation stopped")

    def zUp(self):
        self.btn.z_up()
        self.updateLabels() # 화면에 보이는 좌표 업데이트
        print('Z Up', self.btn.input_z)
    
    def zDown(self):
        self.btn.z_down()
        self.updateLabels()
        print('Z Down', self.btn.input_z)

    def xUp(self):
        self.btn.x_up()
        self.updateLabels()
        print('X Up', self.btn.input_x)

    def xDown(self):
        self.btn.x_down()
        self.updateLabels()
        print('X Down', self.btn.input_x)

    def yUp(self):
        self.btn.y_up()
        self.updateLabels()
        print('Y Up', self.btn.input_y)

    def yDown(self):
        self.btn.y_down()
        self.updateLabels()
        print('Y Down', self.btn.input_y)

########### start.py를 실행하면 아래는 필요 없음 #####################

class GUI_Node(Node):
    def __init__(self):
        super().__init__('gui_node')
        self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)
        self.app = QApplication(sys.argv)
        self.gui = MyApp(self)
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
