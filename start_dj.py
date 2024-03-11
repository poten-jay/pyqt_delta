import sys
import rclpy
import json
from PyQt5.QtWidgets import QApplication, QTextBrowser, QPushButton, QMainWindow, QStackedWidget, QLabel, QRadioButton, QDialog, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import  Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from datetime import datetime

from example import MyEx
from publisher import GUI_Node
from manual import MyApp
from home import MyHome
from move import MyMove
from info import MyInfo
from calibration import MyCal
import receive

# yeong
import subprocess
import os
import time
import signal


class StartWindow(QMainWindow):
    def __init__(self, parent=None, io_data=None):
        super().__init__()
        self.parent = parent
        self.io_data = io_data  # io_data 매개변수를 추가하여 저장
        self.initUI()
        
        
    def initUI(self):
        # UI 초기화 코드


####### start ######################################################################
        self.startButton = QPushButton('START', self)
        self.startButton.clicked.connect(self.startOperation)
        self.startButton.setGeometry(200, 300, 100, 100)

####### stop ######################################################################
        self.stopButton = QPushButton('STOP', self)
        self.stopButton.clicked.connect(self.stopOperation)
        self.stopButton.setGeometry(400, 300, 100, 100)

####### ON ######################################################################
        self.onButton = QPushButton('ON', self)
        self.onButton.clicked.connect(self.onOperation)
        self.onButton.setGeometry(200, 450, 100, 100)

####### OFF ######################################################################
        self.offButton = QPushButton('OFF', self)
        self.offButton.clicked.connect(self.offOperation)
        self.offButton.setGeometry(400, 450, 100, 100)

####### connect ######################################################################
        self.connectButton = QPushButton('Connect', self)
        self.connectButton.clicked.connect(self.connectToReceiver)
        self.connectButton.setGeometry(600, 300, 100, 50)

####### go main ######################################################################
        self.mainButton = QPushButton('Manual', self)
        self.mainButton.clicked.connect(self.parent.gotoMain)
        self.mainButton.setGeometry(10, 100, 100, 50)

####### go home ######################################################################
        self.homingButton = QPushButton('Home', self)
        self.homingButton.clicked.connect(self.parent.gotoHome)
        self.homingButton.setGeometry(10, 150, 100, 50)

####### go move ######################################################################
        self.movingButton = QPushButton('Move', self)
        self.movingButton.clicked.connect(self.parent.gotoMove)
        self.movingButton.setGeometry(10, 200, 100, 50)

####### go Info ######################################################################
        self.infoButton = QPushButton('Information', self)
        self.infoButton.clicked.connect(self.parent.gotoInfo)
        self.infoButton.setGeometry(10, 250, 100, 50)

# ####### go calibration ######################################################################
#         self.infoButton = QPushButton('calibration', self)
#         self.infoButton.clicked.connect(self.parent.gotoCalibration)
#         self.infoButton.setGeometry(10, 300, 100, 50)

####### go calibration need password ######################################################################
        self.calButton = QPushButton('Calibration', self)
        self.calButton.clicked.connect(self.showCalibrationDialog)
        self.calButton.setGeometry(10, 500, 100, 50)     

####### go log ######################################################################
        self.logButton = QPushButton('Log', self)
        self.logButton.clicked.connect(self.parent.gotoLog)
        self.logButton.setGeometry(10, 300, 100, 50)

####### go example ######################################################################
        self.examButton = QPushButton('exmaple', self)
        self.examButton.clicked.connect(self.parent.gotoLog)
        self.examButton.setGeometry(10, 400, 100, 50)

####### # Initially disable XYZ buttons ######################################
        self.startButton.setDisabled(True)
        self.stopButton.setDisabled(True)
        self.mainButton.setDisabled(True)
        self.homingButton.setDisabled(True)
        self.movingButton.setDisabled(True)
        self.infoButton.setDisabled(True)
        self.connectButton.setDisabled(True)
        self.calButton.setDisabled(True)
        self.logButton.setDisabled(True)

        
        # Robot text label
        msg_robot = "- Robot"
        self.signal_robot = QLabel(f"{msg_robot}", self)
        self.signal_robot.setStyleSheet("Color : white; font-size: 15pt; background-color: black;")
        self.signal_robot.setAlignment(Qt.AlignLeft)
        self.signal_robot.setGeometry(300, 100, 150, 25)

        # Conveyor text label
        msg_conveyor = "- Conveyor"
        self.signal_conveyor = QLabel(f"{msg_conveyor}", self)
        self.signal_conveyor.setStyleSheet("Color : white; font-size: 15pt; background-color: black;")
        self.signal_conveyor.setAlignment(Qt.AlignLeft)
        self.signal_conveyor.setGeometry(300, 130, 150, 25)

        # Vision text label
        msg_vision = "- Vision"
        self.signal_vision = QLabel(f"{msg_vision}", self)
        self.signal_vision.setStyleSheet("Color : white; font-size: 15pt; background-color: black;")
        self.signal_vision.setAlignment(Qt.AlignLeft)
        self.signal_vision.setGeometry(300, 160, 150, 25)

        # Encoder text label
        msg_encoder = "- Encoder"
        self.signal_encoder = QLabel(f"{msg_encoder}", self)
        self.signal_encoder.setStyleSheet("Color : white; font-size: 15pt; background-color: black;")
        self.signal_encoder.setAlignment(Qt.AlignLeft)
        self.signal_encoder.setGeometry(300, 190, 150, 25)




####### QTextBrowser 위젯 추가 ###############################################
        self.text_browser = QTextBrowser(self)
        self.text_browser.setGeometry(500, 100, 200, 200)
        
        self.text_browser.setStyleSheet("color: white; font-size: 15pt; background-color: transparent;")

        self.update_text_browser()
        self.connectButton.clicked.connect(self.update_text_browser)
        
        
        # QTimer 설정
        self.logtimer = QTimer(self)
        self.logtimer.timeout.connect(self.update_text_browser)
        self.logtimer.start(500)  # 0.5 seconds interval

        # # 텍스트 파일 내용을 읽어와서 QTextBrowser에 표시
        # try:
        #     file_path = 'document/io.json'  # 실제 파일 경로로 변경
        #     with open(file_path, 'r', encoding='utf-8') as file:
        #         io_data = json.load(file)
        #         text_content = ""
        #         for key, value in io_data.items():
        #             text_content += f"{key} : {value}\n"
        #         self.text_browser.setPlainText(text_content)
        # except Exception as e:
        #     self.text_browser.setPlainText(f"Error: {str(e)}")

####### 시간 ######################################################################
        # 시간 표시 라벨 설정
        self.time_label = QLabel(self)
        self.time_label.setGeometry(660, 585, 200, 10)
        self.time_label.setStyleSheet("font-size: 14px;")
        self.time_label.setStyleSheet("Color : white")

        # QTimer 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

####### I/O 신호 관련 텍스트 ###################################################
        # self.sig_robot = QLabel(f"Robot", self)
        # self.sig_robot.setStyleSheet("Color : white")
        # self.sig_robot.setAlignment(Qt.AlignRight)
        # self.sig_robot.setGeometry(300, 100, 60, 30)

        # self.sig_conveyor = QLabel(f"conveyor", self)
        # self.sig_conveyor.setStyleSheet("Color : white")
        # self.sig_conveyor.setAlignment(Qt.AlignRight)
        # self.sig_conveyor.setGeometry(300, 130, 60, 30)

        # self.sig_vision = QLabel(f"vision", self)
        # self.sig_vision.setStyleSheet("Color : white")
        # self.sig_vision.setAlignment(Qt.AlignRight)
        # self.sig_vision.setGeometry(300, 160, 60, 30)

        # self.sig_encoder = QLabel(f"encoder", self)
        # self.sig_encoder.setStyleSheet("Color : white")
        # self.sig_encoder.setAlignment(Qt.AlignRight)
        # self.sig_encoder.setGeometry(300, 190, 60, 30)

        # # io update 설정 - 시간 설정은 이미 위에서 했음
        # # self.timer = QTimer(self)
        # # self.timer.timeout.connect(self.update_io)  ### 살리면 1초당 업뎃
        # # self.timer.timeout.connect(self.connectToReceiver)
        # # self.timer.start(1000)  # 1초마다 업데이트

        # with open("document/io.json", "r") as io_file:
        #     self.io_data = json.load(io_file)

        # # self.ioPoint()

        # self.loadIoImages()

        # self.radiobuttons()



###
### def###
###
        
####### io.json 읽어오기 ######################################################
    def update_text_browser(self):
                # 텍스트 파일 내용을 읽어와서 QTextBrowser에 표시
        try:
            file_path = 'document/io.json'  # 실제 파일 경로로 변경
            with open(file_path, 'r', encoding='utf-8') as file:
                io_data = json.load(file)
                text_content = ""
                for key, value in io_data.items():
                    icon = "◉" if value else "◉"
                    color = "#33FF33" if value else "red"
                    text_content += f"<font color='{color}'>{icon}</font> - {key}<br>"
                self.text_browser.setHtml(text_content)
        except Exception as e:
            self.text_browser.setPlainText(f"Error: {str(e)}")


####### connect ##########################################################
    def connectToReceiver(self):
        # io.json 파일 읽기
        with open("document/io.json", "r") as io_file:
            self.io_data = json.load(io_file)

            # I/O 신호 이미지 업데이트
            self.loadIoImages()

            # 점찍기
            self.ioPoint()

            # 라디오 버튼 업데이트
            self.radiobuttons()

            # new_start_window = StartWindow(parent=self.parent, io_data=self.io_data)
            # new_start_window.show()
            # UI 업데이트
            # self.update()

            # pyqtSignal()
            print("Connected to receiver")


####### 이미지 삽입 ################################################################
        
    def input_image(self, x, y, w, h, img_path):
        pixmap = QPixmap(img_path)
        scaled_pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # QLabel 생성 및 QPixmap 설정
        lbl_img = QLabel(self)
        lbl_img.setPixmap(scaled_pixmap)
        lbl_img.setGeometry(x, y, scaled_pixmap.width(), scaled_pixmap.height())

####### 시간 #################################################################
    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(current_time)

####### On connect popup ##################################################

####### on / off ##########################################################
    def onOperation(self):
        # Create and display the popup dialog
        popup_dialog = PopupDialog_robot(self)
        result = popup_dialog.exec_()  # Show the dialog and wait for it to close

        if result == QDialog.Accepted:
            # The robot is activated, enable the buttons
            self.startButton.setDisabled(False)
            self.stopButton.setDisabled(False)
            self.mainButton.setDisabled(False)
            self.homingButton.setDisabled(False)
            self.movingButton.setDisabled(False)
            self.infoButton.setDisabled(False)
            self.connectButton.setDisabled(False)
            self.calButton.setDisabled(False)
            self.logButton.setDisabled(False)
        else:
            # The dialog was closed due to timeout
            QMessageBox.warning(self, "Timeout", "Failed to activate the robot within the time limit.")

        # # # yeong
        # # Run the ROS2 launch file and save the subprocess reference
        # current_dir = os.path.dirname(os.path.realpath(__file__))
        # bringup_file = os.path.join(current_dir, "../control/bringup/launch/bringup.py")
        # move_zero_file = os.path.join(current_dir, "../move/move_zero.py")

        # try:
        #     self.ros2_process_robot = subprocess.Popen(["ros2", "launch", bringup_file], preexec_fn=os.setsid)
        #     print("ROS2 robot bringup started")
        # except Exception as e:
        #     print(f"Failed to start ROS2 launch file: {e}")

        # time.sleep(20)

        # try:
        #     self.ros2_process_move_zero = subprocess.Popen(["python3", move_zero_file])
        #     print("ROS2 move_zero started")
        # except Exception as e:
        #     print(f"Failed to start ROS2 python3 file: {e}")

        
        print("Robot ON!!")

    # stop 누르면 비활성화
    def offOperation(self):
        self.startButton.setDisabled(True)
        self.stopButton.setDisabled(True)
        self.mainButton.setDisabled(True)
        self.homingButton.setDisabled(True)
        self.movingButton.setDisabled(True)
        self.infoButton.setDisabled(True)
        self.connectButton.setDisabled(True)
        self.calButton.setDisabled(True)
        self.logButton.setDisabled(True)
        
        # # yeong

        # # # Terminate the ROS2 launch subprocess if it's running
        # if self.ros2_process_robot and self.ros2_process_robot.poll() is None:  # Check if the process is still running
        #     if self.ros2_process_robot and self.ros2_process_robot.poll() is None:
        #         # Terminate the entire process group
        #         os.killpg(os.getpgid(self.ros2_process_robot.pid), signal.SIGTERM)
        #     # self.ros2_process_robot.terminate()  # Terminate the process
        #     # try:
        #     #     self.ros2_process_robot.wait(timeout=10)  # Wait for the process to terminate
        #     # except subprocess.TimeoutExpired:
        #     #     self.ros2_process_robot.kill()  # Force kill if it doesn't terminate within timeout
        #         print("ROS2 robot terminated")

        # # Terminate the ROS2 launch subprocess if it's running
        # if self.ros2_process_move_zero and self.ros2_process_move_zero.poll() is None:  # Check if the process is still running
        #     self.ros2_process_move_zero.terminate()  # Terminate the process
        #     try:
        #         self.ros2_process_move_zero.wait(timeout=5)  # Wait for the process to terminate
        #     except subprocess.TimeoutExpired:
        #         self.ros2_process_move_zero.kill()  # Force kill if it doesn't terminate within timeout
        #     print("ROS2 vision terminated")

        print("Good Bye...")

####### start/stop ##########################################################
    def startOperation(self):


            # Create and display the popup dialog
        popup_dialog = PopupDialog_vision(self)
        result = popup_dialog.exec_()  # Show the dialog and wait for it to close

        if result == QDialog.Accepted:
            # # # yeong
            self.startButton.setDisabled(True)
            # self.stopButton.setDisabled(True)
            self.mainButton.setDisabled(True)
            self.homingButton.setDisabled(True)
            self.movingButton.setDisabled(True)
            # self.infoButton.setDisabled(True)
            self.connectButton.setDisabled(True)
            self.onButton.setDisabled(True)
            self.offButton.setDisabled(True)
            self.calButton.setDisabled(True)
            self.logButton.setDisabled(True)
        else:
            # The dialog was closed due to timeout
            QMessageBox.warning(self, "Timeout", "Failed to activate the robot within the time limit.")


        
        # # # yeong
        # # Run the ROS2 launch file and save the subprocess reference
        # current_dir = os.path.dirname(os.path.realpath(__file__))
        # vision_file = os.path.join(current_dir, "../vision/launch/vision.py")
        # move_file = os.path.join(current_dir, "../move/move.py")

        # try:
        #     self.ros2_process_vision = subprocess.Popen(["ros2", "launch", vision_file])
        #     print("ROS2 vision started")
        # except Exception as e:
        #     print(f"Failed to start ROS2 launch file: {e}")

        
        # time.sleep(4)
        
        # try:
        #     self.ros2_process_move = subprocess.Popen(["python3", move_file])
        #     print("ROS2 move started")
        # except Exception as e:
        #     print(f"Failed to start ROS2 python3 file: {e}")

        print("Operation started!!")

    # stop 누르면 비활성화
    def stopOperation(self):
        self.startButton.setDisabled(False)
        self.stopButton.setDisabled(False)
        self.mainButton.setDisabled(False)
        self.homingButton.setDisabled(False)
        self.movingButton.setDisabled(False)
        self.infoButton.setDisabled(False)
        self.connectButton.setDisabled(False)
        self.onButton.setDisabled(False)
        self.stopButton.setDisabled(False)
        self.offButton.setDisabled(False)
        self.calButton.setDisabled(False)
        self.logButton.setDisabled(False)
        
        # # Terminate the ROS2 launch subprocess if it's running
        if self.ros2_process_move and self.ros2_process_move.poll() is None:  # Check if the process is still running
            self.ros2_process_move.terminate()  # Terminate the process
            try:
                self.ros2_process_move.wait(timeout=5)  # Wait for the process to terminate
            except subprocess.TimeoutExpired:
                self.ros2_process_move.kill()  # Force kill if it doesn't terminate within timeout
            print("ROS2 move terminated")
        time.sleep(2)

        # Terminate the ROS2 launch subprocess if it's running
        if self.ros2_process_vision and self.ros2_process_vision.poll() is None:  # Check if the process is still running
            self.ros2_process_vision.terminate()  # Terminate the process
            try:
                self.ros2_process_vision.wait(timeout=5)  # Wait for the process to terminate
            except subprocess.TimeoutExpired:
                self.ros2_process_vision.kill()  # Force kill if it doesn't terminate within timeout
            print("ROS2 vision terminated")

        print("Operation stopped...")


    def showCalibrationDialog(self):
        # 비밀번호 입력 다이얼로그 생성
        dialog = PasswordDialog(self)
        result = dialog.exec_()  # 다이얼로그를 모달로 표시하고 결과를 받음

        # 다이얼로그 결과 확인
        if result == QDialog.Accepted:
            self.parent.gotoCalibration()  # 올바른 비밀번호가 입력되면 calibration 페이지로 이동
            print("password")
            # self.mycal.run_move_forward()
    
    

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Password')
        self.setFixedSize(300, 150)

        self.label = QLabel('Please Enter password', self)
        self.label.setGeometry(20, 20, 260, 30)

        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(20, 60, 260, 30)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_button = QPushButton('OK', self)
        self.confirm_button.setGeometry(20, 100, 120, 30)
        self.confirm_button.clicked.connect(self.checkPassword)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.setGeometry(160, 100, 120, 30)
        self.cancel_button.clicked.connect(self.reject)

    def checkPassword(self):
        # 입력된 비밀번호 확인
        if self.password_input.text() == '1234':
            self.accept()  # 올바른 비밀번호인 경우 다이얼로그를 종료하고 Accepted 반환
        else:
            QMessageBox.warning(self, 'Erorr', 'Invalied password!.')
            self.password_input.clear()



# class AppManager(QStackedWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('W-ECOBOT Application')
#         self.setWindowIcon(QIcon('img/eth.png'))
#         self.setFixedSize(800, 600)
#         self.setStyleSheet("QStackedWidget {background-image: url('img/start.png');}")
#         self.node = GUI_Node()  # GUI_Node 객체 생성
#         self.initUI()
        
#     def initUI(self):
#         # MyApp, MyHome, MyMove, MyInfo 등 모든 페이지를 생성
        
#         self.my_app = MyApp(self.node)  # MyApp 객체 생성 시 노드 객체 전달
#         self.home_app = MyHome(self.node)  # MyHome 객체 생성 시 노드 객체 전달
#         # self.move_app = MyMove(self.node)  # MyMove 객체 생성 시 노드 객체 전달
#         self.info_app = MyInfo(self.node)  # MyInfo 객체 생성 시 노드 객체 전달
#         self.move_app = None  # 초기에 None으로 설정 (애러서 버튼 호출 할때마다 새로운 창을 열기 위함)
        
#         # StartWindow를 생성하고 스택에 추가
#         self.start_window = StartWindow(parent=self)
#         self.addWidget(self.start_window)

#         # 나머지 페이지들도 스택에 추가
#         self.addWidget(self.my_app)
#         self.addWidget(self.home_app)
#         # self.addWidget(self.move_app)
#         self.addWidget(self.info_app)

#         # 뒤로가기 버튼에서 돌아오는 길 지정
#         self.my_app.goToStartScreen.connect(self.gotoStart)
#         self.home_app.goToStartScreen.connect(self.gotoStart)
#         # 
#         self.info_app.goToStartScreen.connect(self.gotoStart)

#     # 시작 페이지
#     def gotoStart(self):
#         self.setCurrentWidget(self.start_window)

#     # 메인 페이지
#     def gotoMain(self):
#         self.setCurrentWidget(self.my_app)
        
#     # 호밍페이지
#     def gotoHome(self):
#         self.setCurrentWidget(self.home_app)

#     # 무빙(수동)페이지
#     def gotoMove(self):
#         # self.setCurrentWidget(self.move_app)
#         if self.move_app is None:
#             # node = GUI_Node()  # 새로운 GUI_Node 객체 생성
#             self.move_app = MyMove()  # MyMove 객체 생성 시 새로운 노드 객체 전달
#             self.addWidget(self.move_app)  # 스택에 페이지 추가
    
#         self.setCurrentWidget(self.move_app)
#         self.move_app.goToStartScreen.connect(self.gotoStart)

#     # 인포메이션 페이지
#     def gotoInfo(self):
#         self.setCurrentWidget(self.info_app)

# if __name__ == '__main__':
#     app = QApplication(sys.argv) # QApplication : 프로그램을 실행시켜주는 클래스
#     rclpy.init(args=None)
#     app_manager = AppManager()
#     app_manager.show()
#     sys.exit(app.exec_())
#     rclpy.shutdown()
            
class PopupDialog_robot(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Waiting for Robot Activation')
        self.setFixedSize(300, 150)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 300 , 150)
        self.image_paths = [f'img/wait{i}.png' for i in range(1, 7)]  # List of image paths
        self.current_image_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateImage)
        self.timer.start(500)  # Update image every 0.5 seconds
        self.check_robot_status_timer = QTimer(self)
        self.check_robot_status_timer.timeout.connect(self.checkRobotStatus)
        self.check_robot_status_timer.start(500)  # Check robot status every 0.5 seconds
        self.start_time = time.time()

    def updateImage(self):
        pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.label.setPixmap(pixmap)
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)

    def checkRobotStatus(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 30:  # Timeout after 20 seconds
            self.reject()  # Close the dialog

        try:
            with open('document/io.json', 'r') as file:
                io_data = json.load(file)
                if io_data.get("robot"):  # Check if robot status is True
                    self.accept()  # Close the dialog
        except Exception as e:
            print(f"Error reading io.json: {e}")

class PopupDialog_vision(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Waiting for Vision Activation')
        self.setFixedSize(300, 150)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 300 , 150)
        self.image_paths = [f'img/wait{i}.png' for i in range(1, 7)]  # List of image paths
        self.current_image_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateImage)
        self.timer.start(500)  # Update image every 0.5 seconds
        self.check_robot_status_timer = QTimer(self)
        self.check_robot_status_timer.timeout.connect(self.checkRobotStatus)
        self.check_robot_status_timer.start(500)  # Check robot status every 0.5 seconds
        self.start_time = time.time()

    def updateImage(self):
        pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.label.setPixmap(pixmap)
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)

    def checkRobotStatus(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 30:  # Timeout after 20 seconds
            self.reject()  # Close the dialog

        try:
            with open('document/io.json', 'r') as file:
                io_data = json.load(file)
                if io_data.get("vision"):  # Check if robot status is True
                    self.accept()  # Close the dialog
        except Exception as e:
            print(f"Error reading io.json: {e}")