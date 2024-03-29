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

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from wimt_msg.msg import TrackerArray 

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool  # robot_on 토픽의 메시지 타입
from wimt_msg.msg import TrackerArray  # /tracked_objects 토픽의 메시지 타입

class RobotVisionStatusNode(Node):
    def __init__(self, name='robot_vision_status_node'):
        super().__init__(name)
        self.robot_on = False
        self.vision_on = False
        self.tracked_objects = None

        self.create_subscription(
            Bool,
            'robot_on',
            self.robot_on_callback,
            10)
        
        self.create_subscription(
            TrackerArray,
            'tracked_objects',
            self.tracked_objects_callback,
            10)

    def robot_on_callback(self, msg):
        self.robot_on = msg.data

    def tracked_objects_callback(self, msg):
        # self.tracked_objects = msg  # TrackerArray 메시지 객체 전체를 저장
        self.vision_on = True
        



class StartWindow(QMainWindow):
    def __init__(self, parent=None, io_data=None):
        super().__init__()
        self.parent = parent
        self.io_data = io_data  # io_data 매개변수를 추가하여 저장
        self.initUI()
        self.ros2_process_robot = None 

        if not rclpy.ok():
            rclpy.init()
        self.robot_vision_status_node = RobotVisionStatusNode()
        self.executor = rclpy.executors.SingleThreadedExecutor()
        self.executor.add_node(self.robot_vision_status_node)

        
        
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
        # self.logtimer.timeout.connect(self.update_text_browser)
        self.logtimer.timeout.connect(self.update_ros_status)
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

    def update_ros_status(self):
        try:
            # ROS 노드에서 상태 값을 받아옵니다.
            self.executor.spin_once(timeout_sec=0)  # ROS executor를 한 번 실행하여 콜백을 처리합니다.
            vision_status = self.robot_vision_status_node.vision_on  # vision_on 상태 값을 가져옵니다.
            robot_status = self.robot_vision_status_node.robot_on  # robot_on 상태 값을 가져옵니다.

            # 상태 값에 따라 표시할 텍스트를 구성합니다.
            text_content = ""
            status_dict = {"Vision": vision_status, "Robot": robot_status}
            for key, value in status_dict.items():
                icon = "◉"  # 상태 아이콘
                color = "#33FF33" if value else "red"  # 상태에 따른 색상 (True일 때 녹색, False일 때 빨강)
                text_content += f"<font color='{color}'>{icon}</font> - {key}<br>"

            # QTextBrowser에 상태 텍스트를 HTML 형식으로 설정합니다.
            self.text_browser.setHtml(text_content)

        except Exception as e:
            # 오류가 발생한 경우, 오류 메시지를 QTextBrowser에 표시합니다.
            self.text_browser.setPlainText(f"Error: {str(e)}")

        # 이제 robot_vision_status_node robot_on 및 vision_on 속성을 사용할 수 있다.
        # 예: self.robot_vision_status_node.robot_on, self.robot_vision_status_node.vision_on

        
            

    def closeEvent(self, event):
        super().closeEvent(event)
        self.executor.shutdown()
        rclpy.shutdown()
        
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

        # # yeong
        # Run the ROS2 launch file and save the subprocess reference
        current_dir = os.path.dirname(os.path.realpath(__file__))
        bringup_file = os.path.join(current_dir, "../control/bringup/launch/bringup.py")
        move_zero_file = os.path.join(current_dir, "../move/move_zero.py")

        try:
            self.ros2_process_robot = subprocess.Popen(["ros2", "launch", bringup_file], preexec_fn=os.setsid)
            print("ROS2 robot bringup started")
        except Exception as e:
            print(f"Failed to start ROS2 launch file: {e}")

        result = popup_dialog.exec_()  # Show the dialog and wait for it to close

        # try:
        #     self.ros2_process_move_zero = subprocess.Popen(["python3", move_zero_file])
        #     print("ROS2 move_zero started")
        # except Exception as e:
        #     print(f"Failed to start ROS2 python3 file: {e}")

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
        
        # yeong

        # # Terminate the ROS2 launch subprocess if it's running
        if self.ros2_process_robot and self.ros2_process_robot.poll() is None:  # Check if the process is still running
            if self.ros2_process_robot and self.ros2_process_robot.poll() is None:
                # Terminate the entire process group
                os.killpg(os.getpgid(self.ros2_process_robot.pid), signal.SIGTERM)
            # self.ros2_process_robot.terminate()  # Terminate the process
            # try:
            #     self.ros2_process_robot.wait(timeout=10)  # Wait for the process to terminate
            # except subprocess.TimeoutExpired:
            #     self.ros2_process_robot.kill()  # Force kill if it doesn't terminate within timeout
                print("ROS2 robot terminated")

        # Terminate the ROS2 launch subprocess if it's running
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

        # # yeong
        # Run the ROS2 launch file and save the subprocess reference
        current_dir = os.path.dirname(os.path.realpath(__file__))
        vision_file = os.path.join(current_dir, "../vision/launch/vision.py")
        move_file = os.path.join(current_dir, "../move/move.py")

        try:
            self.ros2_process_move = subprocess.Popen(["python3", move_file])
            print("ROS2 move started")
        except Exception as e:
            print(f"Failed to start ROS2 python3 file: {e}")

        time.sleep(6)
        
        try:
            self.ros2_process_vision = subprocess.Popen(["ros2", "launch", vision_file])
            print("ROS2 vision started")
        except Exception as e:
            print(f"Failed to start ROS2 launch file: {e}")

        print("Operation started!!")

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



class RobotStatusNode(Node):
    def __init__(self, name='robot_status_node'):
        super().__init__(name)
        self.subscription = self.create_subscription(
            Bool,
            '/robot_on',
            self.robot_status_callback,
            10)
        self.robot_on = False

    def robot_status_callback(self, msg):
        self.robot_on = msg.data




class PopupDialog_robot(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ROS 2 노드 초기화 및 구독 시작
        if not rclpy.ok():
            rclpy.init()
        self.robot_status_node = RobotStatusNode()
        self.robot_status_executor = rclpy.executors.SingleThreadedExecutor()
        self.robot_status_executor.add_node(self.robot_status_node)

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

        self.robot_status_executor.spin_once(timeout_sec=0)  # ROS 2 콜백 처리

        if self.robot_status_node.robot_on:
            self.accept()  # Close the dialog


        elapsed_time = time.time() - self.start_time
        if elapsed_time > 30:  # Timeout after 20 seconds
            self.reject()  # Close the dialog

        # try:
        #     with open('document/io.json', 'r') as file:
        #         io_data = json.load(file)
        #         if io_data.get("robot"):  # Check if robot status is True
        #             self.accept()  # Close the dialog
        # except Exception as e:
        #     print(f"Error reading io.json: {e}")
    def closeEvent(self, event):
        super().closeEvent(event)
        self.robot_status_executor.shutdown()
    #rclpy.shutdown() 호출은 프로그램의 다른 부분에서 rclpy를 사용하는 경우에는 적합하지 않을 수 있습니다.


class VisionStatusNode(Node):
    def __init__(self, name='vision_status_node'):
        super().__init__(name)
        self.vision_on = False  # Vision 상태를 저장하는 변수

        self.subscription_tracked_objects = self.create_subscription(
            TrackerArray,
            'tracked_objects',
            self.tracked_objects_callback,
            10)

    def tracked_objects_callback(self, msg):
        # 여기에서 메시지 처리 로직을 구현합니다.
        # 예를 들어, 메시지를 받으면 vision_on 상태를 True로 설정할 수 있습니다.
        self.vision_on = True

class PopupDialog_vision(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ROS 2 노드 초기화 및 구독 시작
        if not rclpy.ok():
            rclpy.init()
        self.vision_status_node = VisionStatusNode()
        self.vision_status_executor = rclpy.executors.SingleThreadedExecutor()
        self.vision_status_executor.add_node(self.vision_status_node)

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

        # ROS 2 콜백 처리
        self.vision_status_executor.spin_once(timeout_sec=0)

        if self.vision_status_node.vision_on:
            self.accept()  # Close the dialog if vision_on is True



        elapsed_time = time.time() - self.start_time
        if elapsed_time > 30:  # Timeout after 20 seconds
            self.reject()  # Close the dialog

        # try:
        #     with open('document/io.json', 'r') as file:
        #         io_data = json.load(file)
        #         if io_data.get("vision"):  # Check if robot status is True
        #             self.accept()  # Close the dialog
        # except Exception as e:
        #     print(f"Error reading io.json: {e}")

    def closeEvent(self, event):
        super().closeEvent(event)
        self.vision_status_executor.shutdown()

