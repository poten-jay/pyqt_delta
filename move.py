import sys
import os
import rclpy
from datetime import datetime
from rclpy.node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QSize, Qt, pyqtSignal
from geometry_msgs.msg import Point

# function.py 에서 class 호출
# from function import xyz_button
from home import MyHome


# setting.py 에서 값 호출
import setting
import yaml
import ruamel.yaml


# 현재 좌표 값 받아오기
x = setting.x
y = setting.y
z = setting.z


yaml_file_path = '../move/config.yaml'  

with open(yaml_file_path, 'r') as file:
    # YAML 파일을 읽고 파싱하여 Python 딕셔너리로 변환
    config = yaml.safe_load(file)


    up = config['trajectory']['up']
    pick_z = config['trajectory']['pick_z']
    speed = config['trajectory']['speed']
    curve_r = config['trajectory']['curve_r']
    pick_decel = config['trajectory']['pick_decel']
    place_decel = config['trajectory']['place_decel']
    decel_start = config['trajectory']['decel_start']
    place_down_mode = config['trajectory']['place_down_mode']
    pick_sync = config['trajectory']['pick_sync']
    place_sync = config['trajectory']['place_sync']

class MyMove(QWidget):
    goToStartScreen = pyqtSignal()

    def __init__(self):
        super().__init__()
    
        with open(yaml_file_path, 'r') as file:
            # YAML 파일을 읽고 파싱하여 Python 딕셔너리로 변환
            config = yaml.safe_load(file)
            
        if config['trajectory']['place_down_mode'] == 1:
        # self.btn = xyz_button(node, x, y, z)
            self.original_pixmap = QPixmap("img/move3.png")
        else:
            self.original_pixmap = QPixmap("img/move44.png")
        self.initUI()
        self.timer = QTimer(self)
        # self.lbl_img = QLabel(self)
        
        # self.initUI
        if config['trajectory']['sync'] == 0:
            # Sync 값이 0이면 이 부분의 설정을 따름
            self.decel_5.setEnabled(True)
            self.decel_6.setEnabled(True)
            self.sync1.setDisabled(True)
            self.sync2.setDisabled(True)
            self.synconoff.setText("Sync On")  # 버튼 텍스트를 Sync On으로 설정
        else:
            # Sync 값이 1이면 이 부분의 설정을 따름
            self.decel_5.setDisabled(True)
            self.decel_6.setDisabled(True)
            self.sync1.setEnabled(True)
            self.sync2.setEnabled(True)
            self.synconoff.setText("Sync Off")  # 버튼 텍스트를 Sync Off으로 설정

        

    def initUI(self):
        with open(yaml_file_path, 'r') as file:
        # YAML 파일을 읽고 파싱하여 Python 딕셔너리로 변환
            config = yaml.safe_load(file)


            up = config['trajectory']['up']
            pick_z = config['trajectory']['pick_z']
            speed = config['trajectory']['speed']
            curve_r = config['trajectory']['curve_r']
            pick_decel = config['trajectory']['pick_decel']
            place_decel = config['trajectory']['place_decel']
            decel_start = config['trajectory']['decel_start']
            place_down_mode = config['trajectory']['place_down_mode']
            pick_sync = config['trajectory']['pick_sync']
            place_sync = config['trajectory']['place_sync']
######## 이미지 넣기 #######################################################
        # original_pixmap = QPixmap("img/move2.png")
        scaled_pixmap = self.original_pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # QLabel 생성 및 QPixmap 설정
        self.lbl_img = QLabel(self)
        self.lbl_img.setPixmap(scaled_pixmap)
        self.lbl_img.setGeometry(0, 0, scaled_pixmap.width(), scaled_pixmap.height())
########################################################################
######## 이미지 추가 #######################################################
#         original_pixmap1 = QPixmap("img/kbs1.png")
#         scaled_pixmap1 = original_pixmap1.scaled(800, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         # QLabel 생성 및 QPixmap 설정
#         lbl_img = QLabel(self)
#         lbl_img.setPixmap(scaled_pixmap1)
#         lbl_img.setGeometry(23, 20, scaled_pixmap1.width(), scaled_pixmap1.height())
# ########################################################################

        # 창 크기 고정
        self.setFixedSize(800,600)

######################################################################
        # 0. start_point z => home 의 정보 가져오기
        self.place_z = QLabel(f"{config['move']['home1']['z']}", self)
        self.place_z.setStyleSheet("Color : white")
        self.place_z.setAlignment(Qt.AlignRight)
        self.place_z.setGeometry(516, 473, 55, 25)  # Adjust position and size as needed

        # 1. height_1
        self.label_height_1 = QLabel(f"{up}", self)
        self.label_height_1.setStyleSheet("Color : white")
        self.label_height_1.setAlignment(Qt.AlignRight)
        self.label_height_1.setGeometry(189, 274, 55, 25)
        self.height_1 = QLineEdit(self) # 176, 229, 55, 25)
        self.height_1.setGeometry(194, 296, 55, 25)
        self.height_1.setText(str(up))
        self.height_1.setAlignment(Qt.AlignRight) # 우측정렬

        # 2. decel_6 z
        self.label_pick_z_2 = QLabel(f"{pick_z}", self)
        self.label_pick_z_2.setStyleSheet("Color : white")
        self.label_pick_z_2.setAlignment(Qt.AlignRight)
        self.label_pick_z_2.setGeometry(159, 489, 55, 25)  # Adjust position and size as needed
        self.pick_z_2 = QLineEdit(self)
        self.pick_z_2.setGeometry(164, 511, 55, 25)  # Adjust position and size as needed
        self.pick_z_2.setText(str(pick_z))
        self.pick_z_2.setAlignment(Qt.AlignRight)

        # 3. speed
        self.label_speed_3 = QLabel(f"{speed}", self)
        self.label_speed_3.setStyleSheet("Color : white")
        self.label_speed_3.setAlignment(Qt.AlignRight)
        self.label_speed_3.setGeometry(453, 280, 55, 25)  # Adjust position and size as needed
        self.speed_3 = QLineEdit(self)
        self.speed_3.setGeometry(458, 302, 55, 25)  # Adjust position and size as needed
        self.speed_3.setText(str(speed))
        self.speed_3.setAlignment(Qt.AlignRight)

        # 4. R
        self.label_r_4 = QLabel(f"{curve_r}", self)
        self.label_r_4.setStyleSheet("Color : white")
        self.label_r_4.setAlignment(Qt.AlignRight)
        self.label_r_4.setGeometry(346, 178, 55, 25)  # Adjust position and size as needed
        self.r_4 = QLineEdit(self)
        self.r_4.setGeometry(351, 201, 54, 25)  # Adjust position and size as needed
        self.r_4.setText(str(curve_r))
        self.r_4.setAlignment(Qt.AlignRight)

        # 5. deceleration 1
        self.label_decel_5 = QLabel(f"{pick_decel}", self)
        self.label_decel_5.setStyleSheet("Color : white")
        self.label_decel_5.setAlignment(Qt.AlignRight)
        self.label_decel_5.setGeometry(378, 419, 55, 25)  # Adjust position and size as needed
        self.decel_5 = QLineEdit(self)
        self.decel_5.setGeometry(383, 441, 55, 25)  # Adjust position and size as needed
        self.decel_5.setText(str(pick_decel))
        self.decel_5.setAlignment(Qt.AlignRight)

        # 6. deceleration 2
        self.label_decel_6 = QLabel(f"{place_decel}", self)
        self.label_decel_6.setStyleSheet("Color : white")
        self.label_decel_6.setAlignment(Qt.AlignRight)
        self.label_decel_6.setGeometry(704, 419, 55, 25)  # Adjust position and size as needed
        self.decel_6 = QLineEdit(self)
        self.decel_6.setGeometry(709, 441, 55, 25)  # Adjust position and size as needed
        self.decel_6.setText(str(place_decel))
        self.decel_6.setAlignment(Qt.AlignRight)

        # 7. start point of deceleration
        # "30" 

        # self.start_point = 30
        self.start_point = decel_start
                 
        # 8. Move L or Move U => F / T

        self.workspace_z = QLabel(f"Max : {setting.z_max}", self)
        self.workspace_z.setStyleSheet("Color : white")
        self.workspace_z.setAlignment(Qt.AlignRight)
        self.workspace_z.setGeometry(110, 150, 100, 30)  # Adjust position and size as needed
        self.workspace_zn = QLabel(f"Min : {setting.z_min}", self)
        self.workspace_zn.setStyleSheet("Color : white")
        self.workspace_zn.setAlignment(Qt.AlignRight)
        self.workspace_zn.setGeometry(110, 550, 100, 30)  # Adjust position and size as needed

        # 9. Sync
        self.pick_sync_8 = QLabel(f"{pick_sync}", self)
        self.pick_sync_8.setStyleSheet("Color : white")
        self.pick_sync_8.setAlignment(Qt.AlignRight)
        self.pick_sync_8.setGeometry(159, 400, 55, 25)  # Adjust position and size as needed
        self.place_sync_9 = QLabel(f"{place_sync}", self)
        self.place_sync_9.setStyleSheet("Color : white")
        self.place_sync_9.setAlignment(Qt.AlignRight)
        self.place_sync_9.setGeometry(600, 400, 55, 25)  # Adjust position and size as needed
#######################################################################


        # 버튼
        # Reset Button
        self.btnReset = QPushButton('Reset', self)
        self.btnReset.setGeometry(580, 520, 50, 40)  # Adjust position and size as needed
        self.btnReset.clicked.connect(self.resetFields)

        # Listup Button
        self.btnListup = QPushButton('List Up', self)
        self.btnListup.setGeometry(640, 520, 90, 40)  # Adjust position and size as needed
        self.btnListup.clicked.connect(self.listupClicked)

        # a Button - ㄱ 자 움직임
        self.btna = QPushButton('Move L', self)
        self.btna.setGeometry(10, 200, 70, 50)  # Adjust position and size as needed
        self.btna.clicked.connect(self.clickmoveL)
        self.btna.clicked.connect(self.addimage)

        # b Button - ㄷ자 움직임
        self.btnb = QPushButton('Move U', self)
        self.btnb.setGeometry(10, 300, 70, 50)  # Adjust position and size as needed
        self.btnb.clicked.connect(self.clickmoveU)
        self.btnb.clicked.connect(self.addimage2)

        # sync on/off
        self.synconoff = QPushButton('Sync On', self)
        self.synconoff.setGeometry(10, 400, 70, 50)
        if config['trajectory']['sync'] == 1:
            self.synconoff.setStyleSheet("background-color: green;")
        else:
            self.synconoff.setStyleSheet("")
        self.synconoff.clicked.connect(self.toggleSync)
        self.synconoff.clicked.connect(self.synconclick)

        # pick Sync Button
        self.sync1 = QPushButton('Sync', self)
        self.sync1.setGeometry(310, 510, 35, 25)  # Adjust position and size as needed
        if config['trajectory']['sync'] == 1:
            self.sync1.setStyleSheet("background-color: green;")
        else:
            self.sync1.setStyleSheet("")
        self.sync1.clicked.connect(self.syncDialog_pick)
        self.sync1.setDisabled(True)
            
        # Place Sync Button
        self.sync2 = QPushButton('Sync', self)
        self.sync2.setGeometry(610, 480, 35, 25)  # Adjust position and size as needed
        if config['trajectory']['sync'] == 1:
            self.sync2.setStyleSheet("background-color: green;")
        else:
            self.sync2.setStyleSheet("")
        self.sync2.clicked.connect(self.syncDialog_place)
        self.sync2.setDisabled(True)

        # 뒤로가기 버튼 (순서가 밀리면 안보일 수도 있음)
        self.button()

        # Read items from the file and add them to the ComboBox
        with open('../vision/labels.txt', 'r') as file:
            items = file.read().splitlines()
            # self.comboBox.addItems(items)

####### 시간 ######################################################################
        # 시간을 표시할 QLabel 생성
        self.time_label = QLabel(self)
        self.time_label.setGeometry(660, 585, 200, 10)  # 위치와 크기 설정
        self.time_label.setStyleSheet("font-size: 14px;")  # 폰트 크기 설정
        self.time_label.setStyleSheet("Color : white")

        # QTimer 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1초마다 update_time 함수 호출
        
    def update_time(self):
        # 현재 시간을 가져와서 QLabel에 표시
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(current_time)

####### 시간 #################################################################


    # ㄱ 자 무빙
    def clickmoveL(self):
        # self.speed_3.setDisabled(True)
        self.decel_6.setDisabled(True)
        # self.start_point.setDisabled(True)
        self.update_place_down_mode(0)  # 파일의 마지막 글자를 'a'로 변경
        

    # ㄷ 자 무빙
    def clickmoveU(self):
        # self.speed_3.setDisabled(False)
        if config['trajectory']['sync'] == 1:
            self.decel_6.setDisabled(True)
        # self.start_point.setDisabled(False)
        self.update_place_down_mode(1)  # 파일의 마지막 글자를 'b'로 변경

####### 이미지 추가 #######################################################
    def addimage(self):
        new_pixmap = QPixmap("img/move44.png")
        self.lbl_img.setPixmap(new_pixmap)

    def addimage2(self):
        new2_pixmap = QPixmap("img/move3.png")
        # new2_pixmap = self.original_pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lbl_img.setPixmap(new2_pixmap)
        # original_pixmap1 = QPixmap("img/main.png")
        # scaled_pixmap1 = original_pixmap1.scaled(800, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # # QLabel 생성 및 QPixmap 설정
        # add_img = QLabel(self)
        # add_img.setPixmap(scaled_pixmap1)
        # add_img.setGeometry(100, 100, scaled_pixmap1.width(), scaled_pixmap1.height())
########################################################################

###### sync on/off버튼
    def toggleSync(self):
        current_text = self.synconoff.text()
        new_text = "Sync" if current_text == "Sync On" else "Sync On"
        self.synconoff.setText(new_text)
    
    def synconclick(self):
        current_text = self.synconoff.text()
        if current_text == "Sync On":
            self.decel_5.setEnabled(True)
            self.decel_6.setEnabled(True)
            self.sync1.setDisabled(True)
            self.sync2.setDisabled(True)
            self.updateSyncValue(0)  # Sync Off 상태에서 Sync 값을 0으로 설정
            self.synconoff.setStyleSheet("")
            self.sync1.setStyleSheet("") 
            self.sync2.setStyleSheet("") 
            
        else:
            self.decel_5.setDisabled(True)
            self.decel_6.setDisabled(True)
            self.sync1.setEnabled(True)
            self.sync2.setEnabled(True)
            self.updateSyncValue(1)  # Sync On 상태에서 Sync 값을 1로 설정
            self.synconoff.setStyleSheet("background-color: green;") 
            self.sync1.setStyleSheet("background-color: green;") 
            self.sync2.setStyleSheet("background-color: green;") 
        
    def updateSyncValue(self, value):
        # config['trajectory']['sync'] 값을 업데이트하는 함수
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=4, sequence=4, offset=2)
        with open(yaml_file_path, 'r') as file:
            config = yaml.load(file)
            config['trajectory']['sync'] = value  # sync 값을 업데이트

        with open(yaml_file_path, 'w') as file:
            yaml.dump(config, file)  # 변경된 설정을 파일에 다시 쓰기

###### 마지막 글자 바꾸기
    def update_place_down_mode(self, tf):
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=4, sequence=4, offset=2)
        with open(yaml_file_path, 'r') as file:
            # YAML 파일을 읽고 파싱하여 Python 딕셔너리로 변환
            config = yaml.load(file)

            # tf = tf.rstrip('')
            config['trajectory']['place_down_mode'] = tf

        with open(yaml_file_path, 'w') as file:
            yaml.dump(config, file)



###### 리스트업 클릭시 보낼 정보
    def listupClicked(self):

        if place_down_mode == 0:
            self.listupClicked_a()
        else :
            self.listupClicked_b()



    def listupClicked_a(self):
        

        try:
            height_1 = float(self.height_1.text())
            pick_z_2 = float(self.pick_z_2.text())
            speed_3 = float(self.speed_3.text())
            r_4 = float(self.r_4.text())
            decel_5 = float(self.decel_5.text())
            decel_6 = float(self.decel_6.text())
            start_point = float(decel_start)
            pick_sync_8 = float(self.pick_sync_8.text())
            place_sync_9 = float(self.place_sync_9.text())
            
            if setting.z_min <= height_1 <= setting.z_max and \
               setting.z_min <= pick_z_2 <= (height_1 - setting.round) and \
               setting.path_speed_min <= speed_3 <= setting.path_speed_max and \
               setting.bending_min <= r_4 <= setting.bending_max and \
               setting.Deceleration_min <= decel_5 <= setting.Deceleration_max and \
               setting.Deceleration_min <= decel_6 <= setting.Deceleration_max and \
               setting.sync_min <= pick_sync_8 <= setting.sync_max and \
               setting.sync_min <= place_sync_9 <= setting.sync_max:
               

                self.updateLabels()

                yaml = ruamel.yaml.YAML()
                yaml.indent(mapping=4, sequence=4, offset=2)
                with open(yaml_file_path, 'r') as file:
                    # YAML 파일을 읽고 파싱하여 Python 딕셔너리로 변환
                    config = yaml.load(file)

                # # 0번째 줄 덮어쓰기 또는 추가하기
                # existing_lines[0] = f'{height_1} {pick_z_2} {speed_3} {r_4} {decel_5} {decel_6} {start_point} F\n'
                
                config['trajectory']['up'] = height_1
                config['trajectory']['pick_z'] = pick_z_2
                config['trajectory']['speed'] = speed_3
                config['trajectory']['curve_r'] = r_4
                config['trajectory']['pick_decel'] = decel_5
                config['trajectory']['place_decel'] = decel_6
                config['trajectory']['decel_start'] = start_point
                config['trajectory']['pick_sync'] =  pick_sync_8
                config['trajectory']['place_sync'] = place_sync_9
                # place_down_mode = config['trajectory']['place_down_mode']
                    
                with open(yaml_file_path, 'w') as file:
                    yaml.dump(config, file)

                self.label_height_1.setText(str(height_1))
                self.label_pick_z_2.setText(str(pick_z_2))
                self.label_speed_3.setText(str(speed_3))
                self.label_r_4.setText(str(r_4))
                self.label_decel_5.setText(str(decel_5))
                self.label_decel_6.setText(str(decel_6))
                self.pick_sync_8.setText(str(pick_sync_8))
                self.place_sync_9.setText(str(place_sync_9))
                # self.start_point.setText(str(start_point))
                # place_down_mode = config['trajectory']['place_down_mode']

                # 확인 메시지 표시
                QMessageBox.information(self, "Info", "Data updated in config")
            else:
                # Handle out of range values
                print("Values out of range")
                self.height_1.setText("Out of Range")
                self.height_1.setStyleSheet("color: red;")
                self.height_1.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.pick_z_2.setText("Out of Range")
                self.pick_z_2.setStyleSheet("color: red;")
                self.pick_z_2.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.speed_3.setText("Out of Range")
                self.speed_3.setStyleSheet("color: red;")
                self.speed_3.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.r_4.setText("Out of Range")
                self.r_4.setStyleSheet("color: red;")
                self.r_4.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.decel_5.setText("Out of Range")
                self.decel_5.setStyleSheet("color: red;")
                self.decel_5.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.decel_6.setText("Out of Range")
                self.decel_6.setStyleSheet("color: red;")
                self.decel_6.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.pick_sync_8.setText("Out of Range")
                self.pick_sync_8.setStyleSheet("color: red;")
                self.pick_sync_8.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.place_sync_9.setText("Out of Range")
                self.place_sync_9.setStyleSheet("color: red;")
                self.place_sync_9.setAlignment(Qt.AlignRight)
                # print("Values out of range")
                # self.start_point.setText("Out of Range")
                # self.start_point.setStyleSheet("color: red;")
                # self.start_point.setAlignment(Qt.AlignRight)


        except ValueError:
            print("Error")

    # 리스트업 클릭시 보낼 정보
    def listupClicked_b(self):

        try:
            height_1 = float(self.height_1.text())
            pick_z_2 = float(self.pick_z_2.text())
            speed_3 = float(self.speed_3.text())
            r_4 = float(self.r_4.text())
            decel_5 = float(self.decel_5.text())
            decel_6 = float(self.decel_6.text())
            start_point = float(decel_start)
            pick_sync_8 = float(self.pick_sync_8.text())
            place_sync_9 = float(self.place_sync_9.text())
            
            if setting.z_min <= height_1 <= setting.z_max and \
               setting.z_min <= pick_z_2 <= (height_1 - setting.round) and \
               setting.path_speed_min <= speed_3 <= setting.path_speed_max and \
               setting.bending_min <= r_4 <= setting.bending_max and \
               setting.Deceleration_min <= decel_5 <= setting.Deceleration_max and \
               setting.Deceleration_min <= decel_6 <= setting.Deceleration_max and \
               setting.sync_min <= pick_sync_8 <= setting.sync_max and \
               setting.sync_min <= place_sync_9 <= setting.sync_max:
               

                self.updateLabels()

                yaml = ruamel.yaml.YAML()
                yaml.indent(mapping=4, sequence=4, offset=2)
                with open(yaml_file_path, 'r') as file:
                    # YAML 파일을 읽고 파싱하여 Python 딕셔너리로 변환
                    config = yaml.load(file)

                # # 0번째 줄 덮어쓰기 또는 추가하기
                # existing_lines[0] = f'{height_1} {pick_z_2} {speed_3} {r_4} {decel_5} {decel_6} {start_point} F\n'
                
                config['trajectory']['up'] = height_1
                config['trajectory']['pick_z'] = pick_z_2
                config['trajectory']['speed'] = speed_3
                config['trajectory']['curve_r'] = r_4
                config['trajectory']['pick_decel'] = decel_5
                config['trajectory']['place_decel'] = decel_6
                config['trajectory']['decel_start'] = start_point
                config['trajectory']['pick_sync'] =  pick_sync_8
                config['trajectory']['place_sync'] = place_sync_9
                # place_down_mode = config['trajectory']['place_down_mode']
                    
                with open(yaml_file_path, 'w') as file:
                    yaml.dump(config, file)

                self.label_height_1.setText(str(height_1))
                self.label_pick_z_2.setText(str(pick_z_2))
                self.label_speed_3.setText(str(speed_3))
                self.label_r_4.setText(str(r_4))
                self.label_decel_5.setText(str(decel_5))
                self.label_decel_6.setText(str(decel_6))
                self.pick_sync_8.setText(str(pick_sync_8))
                self.place_sync_9.setText(str(place_sync_9))
                # self.start_point.setText(str(start_point))

                # 확인 메시지 표시
                QMessageBox.information(self, "Info", "Data updated in config")
            else:
                # Handle out of range values
                print("Values out of range")
                self.height_1.setText("Out of Range")
                self.height_1.setStyleSheet("color: red;")
                self.height_1.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.pick_z_2.setText("Out of Range")
                self.pick_z_2.setStyleSheet("color: red;")
                self.pick_z_2.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.speed_3.setText("Out of Range")
                self.speed_3.setStyleSheet("color: red;")
                self.speed_3.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.r_4.setText("Out of Range")
                self.r_4.setStyleSheet("color: red;")
                self.r_4.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.decel_5.setText("Out of Range")
                self.decel_5.setStyleSheet("color: red;")
                self.decel_5.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.decel_6.setText("Out of Range")
                self.decel_6.setStyleSheet("color: red;")
                self.decel_6.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.pick_sync_8.setText("Out of Range")
                self.pick_sync_8.setStyleSheet("color: red;")
                self.pick_sync_8.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.place_sync_9.setText("Out of Range")
                self.place_sync_9.setStyleSheet("color: red;")
                self.place_sync_9.setAlignment(Qt.AlignRight)
                # print("Values out of range")
                # self.start_point.setText("Out of Range")
                # self.start_point.setStyleSheet("color: red;")
                # self.start_point.setAlignment(Qt.AlignRight)


        except ValueError:
            print("Error")

        self.show()

    # 창 중앙으로 보내기
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 

    # def setBackgroundImage(self, imagePath):
    #     pixmap = QPixmap(imagePath)
    #     palette = QPalette()
    #     palette.setBrush(QPalette.Background, QBrush(pixmap))
    #     self.setPalette(palette)

    # x,y,z 값 창 업데이트
    def updateLabels(self):
        # xzy 값 한도에서 붉게 변경
        if self.label_height_1 == setting.z_min or self.label_height_1 == setting.z_max:
            self.label_height_1.setStyleSheet("Color : red")
            self.label_height_1.setText(f'Limit {self.label_height_1}')
        else:
            self.label_height_1.setStyleSheet("Color : white")
            self.label_height_1.setText(f'{self.label_height_1}')

        if self.label_pick_z_2 == setting.z_min or self.label_pick_z_2 == setting.z_max:
            self.label_pick_z_2.setStyleSheet("Color : red")
            self.label_pick_z_2.setText(f'Limit {self.label_pick_z_2}')
        else:
            self.label_pick_z_2.setStyleSheet("Color : white")
            self.label_pick_z_2.setText(f'{self.label_pick_z_2}')

        if self.label_speed_3 == setting.path_speed_min or self.label_speed_3 == setting.path_speed_max:
            self.label_speed_3.setStyleSheet("Color : red")
            self.label_speed_3.setText(f'Limit {self.label_speed_3}')
        else:
            self.label_speed_3.setStyleSheet("Color : white")
            self.label_speed_3.setText(f'{self.label_speed_3}')
##############
        if self.label_r_4 == setting.bending_min or self.label_r_4 == setting.bending_max:
            self.label_r_4.setStyleSheet("Color : red")
            self.label_r_4.setText(f'Limit {self.label_r_4}')
        else:
            self.label_r_4.setStyleSheet("Color : white")
            self.label_r_4.setText(f'{self.label_r_4}')
##################
        if self.label_decel_5 == setting.Deceleration_min or self.label_decel_5 == setting.Deceleration_max:
            self.label_decel_5.setStyleSheet("Color : red")
            self.label_decel_5.setText(f'Limit {self.label_decel_5}')
        else:
            self.label_decel_5.setStyleSheet("Color : white")
            self.label_decel_5.setText(f'{self.label_decel_5}')

        if self.label_decel_6 == setting.Deceleration_min or self.label_decel_6 == setting.Deceleration_max:
            self.label_decel_6.setStyleSheet("Color : red")
            self.label_decel_6.setText(f'Limit {self.label_decel_6}')
        else:
            self.label_decel_6.setStyleSheet("Color : white")
            self.label_decel_6.setText(f'{self.label_decel_6}')

        # if self.start_point == setting.z_max or self.start_point == setting.z_min:
        #     self.start_point.setStyleSheet("Color : red")
        #     self.start_point.setText(f'Limit {self.start_point}')
        # else:
        #     self.start_point.setStyleSheet("Color : white")
        #     self.start_point.setText(f'{self.start_point}')


    def comboBoxIndexChanged(self, index):
        # Handle the ComboBox item selection here
        selected_item = self.comboBox.currentText()
        print(f"Selected item: {selected_item}")

    # 버튼 위치 및 사이즈 결정
    def button(self):

        # 뒤로 가기 버튼
        self.btnback = QPushButton('<<', self)
        # self.btnback.clicked.connect(self.goToStartScreen.emit)
        self.btnback.setGeometry(0, 528, 50, 50)
        # self.btnback.raise_()  # Raise the button to the top of the widget stack

        # self.btnback.clicked.connect(self.close)
        # self.btnback.clicked.connect(self.goToStartScreen.emit)
        self.btnback.clicked.connect(self.onBackButtonClick)


    def onBackButtonClick(self):
        # Emit the signal when the button is clicked
        self.close() 
        self.goToStartScreen.emit()


    # 직접 입력창 리셋
    def resetFields(self):

        self.height_1.setText(str(-900))
        self.pick_z_2.setText(str(-970))
        self.speed_3.setText(str(1000))
        self.r_4.setText(str(50))
        self.decel_5.setText(str(0.95))
        self.decel_6.setText(str(0.95))
        # self.start_point.setText(str(-900))
        # Optionally, reset the style if it's changed when values are out of range
        self.height_1.setStyleSheet("color: black;")
        self.pick_z_2.setStyleSheet("color: black;")
        self.speed_3.setStyleSheet("color: black;")
        self.r_4.setStyleSheet("color: black;")
        self.decel_5.setStyleSheet("color: black;")
        self.decel_6.setStyleSheet("color: black;")
        # self.start_point.setStyleSheet("color: black;")

    def refreshPage(self):

        with open(yaml_file_path, 'r') as file:
            # YAML 파일을 읽고 파싱하여 Python 딕셔너리로 변환
            config = yaml.safe_load(file)

            # config['move']['home1']['label']
            # config['move']['home1']['x']
            # config['move']['home1']['y']
            # config['move']['home1']['z']

        # lebel 정보 창
        self.label1_label = QLabel(f"{config['move']['home1']['label']}", self)
        self.label1_label.setStyleSheet("Color : white")
        self.label1_label.setAlignment(Qt.AlignRight)
        self.label1_label.setGeometry(313, 153, 100, 30)  # Adjust position and size as needed
        self.label1_x = QLabel(f"{config['move']['home1']['x']}", self)
        self.label1_x.setStyleSheet("Color : white")
        self.label1_x.setAlignment(Qt.AlignRight)
        self.label1_x.setGeometry(412, 153, 100, 30)  # Adjust position and size as needed
        self.label1_y = QLabel(f"{config['move']['home1']['y']}", self)
        self.label1_y.setStyleSheet("Color : white")
        self.label1_y.setAlignment(Qt.AlignRight)
        self.label1_y.setGeometry(531, 153, 100, 30)  # Adjust position and size as needed
        self.label1_z = QLabel(f"{config['move']['home1']['z']}", self)
        self.label1_z.setStyleSheet("Color : white")
        self.label1_z.setAlignment(Qt.AlignRight)
        self.label1_z.setGeometry(649, 153, 100, 30)  # Adjust position and size as needed

###### pop pick synk ###########
    def syncDialog_pick(self):
        QMessageBox.information(self, "Notice", "If you use Sncy, you will not be able to use Decceleration.")
        # config.yaml 파일에서 pick_z 값을 읽어오는 부분
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file)
            current_pick = config['trajectory']['pick_sync']  # 현재 pick_z 값을 얻음

        # syncDialog에 현재 pick_z 값을 전달하면서 인스턴스 생성
        dialog = syncDialog_pick(current_pick, self)  
        dialog.saveClicked.connect(self.updatePick1)  # 시그널 연결
        dialog.exec_()  # 대화상자 실행

    # 슬롯 정의: 새 pick_z_2 값으로 self.pick_z_2 업데이트
    def updatePick1(self, new_pick):
        self.pick_sync_8.setText(str(new_pick))  # QLineEdit의 텍스트 업데이트
        # 필요한 경우 추가적인 업데이트 로직 구현

###### pop place synk ###########
    def syncDialog_place(self):
        QMessageBox.information(self, "Notice", "If you use Sncy, you will not be able to use Decceleration.")
        # config.yaml 파일에서 pick_z 값을 읽어오는 부분
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file)
            current_place = config['trajectory']['place_sync']  # 현재 pick_z 값을 얻음

        # syncDialog에 현재 pick_z 값을 전달하면서 인스턴스 생성
        dialog = syncDialog_place(current_place, self)  
        dialog.saveClicked.connect(self.updatePick2)  # 시그널 연결
        dialog.exec_()  # 대화상자 실행

    # 슬롯 정의: 새 pick_z_2 값으로 self.pick_z_2 업데이트
    def updatePick2(self, new_place):
        self.place_sync_9.setText(str(new_place))  # QLineEdit의 텍스트 업데이트
        # 필요한 경우 추가적인 업데이트 로직 구현
        
###### pop pick synk ###########
class syncDialog_pick(QDialog):
    saveClicked = pyqtSignal(float)  # float 타입의 시그널 정의

    def __init__(self,pick_sync, parent=None):
        super(syncDialog_pick, self).__init__(parent)
        self.setWindowTitle('Moving Sync & Deceleration')
        self.setFixedSize(500, 300)
        self.setBackgroundImage("img/move_pop2.png")

        # QLineEdit 위젯 생성 및 초기화
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setText(str(pick_sync))  # 기존 pick_z 값으로 초기화
        self.lineEdit.setAlignment(Qt.AlignRight)
        self.lineEdit.setFixedSize(55,25) # QLineEdit의 크기를 조절
        self.lineEdit.move(302, 233)  # QLineEdit의 위치를 지정

        # QDialog에 확인(Ok) 버튼 추가
        self.okButton = QPushButton('Save', self)
        self.okButton.setFixedSize(70,50) # QLineEdit의 크기를 조절
        self.okButton.move(400, 220)  # QLisave_clickedneEdit의 위치를 지정
        self.okButton.clicked.connect(self.save_clicked)  # 클릭 시 대화상자 닫기

    def setBackgroundImage(self, imagePath):
        # 배경 이미지 설정을 위한 QPixmap 객체 생성
        background = QPixmap(imagePath)
        # QPalette 객체 생성
        palette = QPalette()
        # QPalette의 Background에 QPixmap을 QBrush 객체로 설정
        palette.setBrush(QPalette.Window, QBrush(background))
        # QDialog의 팔레트 설정
        self.setPalette(palette)

     # "Save" 버튼 클릭 이벤트 처리기
    def save_clicked(self):
        QMessageBox.information(self, "Notice", "You must click List Up to enable Sync.")
        new_pick = float(self.lineEdit.text())  # QLineEdit에서 새 값을 읽음
        self.saveClicked.emit(new_pick)  # 시그널 발생, new_place 값 전달
        self.close()  # 대화상자 닫기


    
###### pop place synk ###########
class syncDialog_place(QDialog):
    saveClicked = pyqtSignal(float)  # float 타입의 시그널 정의

    def __init__(self,place_sync, parent=None):
        super(syncDialog_place, self).__init__(parent)
        self.setWindowTitle('Moving Sync & Deceleration')
        self.setFixedSize(500, 300)
        self.setBackgroundImage("img/move_pop3.png")

        # QLineEdit 위젯 생성 및 초기화
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setText(str(place_sync))  # 기존 pick_z 값으로 초기화
        self.lineEdit.setAlignment(Qt.AlignRight)
        self.lineEdit.setFixedSize(55,25) # QLineEdit의 크기를 조절
        self.lineEdit.move(302, 233)  # QLineEdit의 위치를 지정

        # QDialog에 확인(Ok) 버튼 추가
        self.okButton = QPushButton('Save', self)
        self.okButton.setFixedSize(70,50) # QLineEdit의 크기를 조절
        self.okButton.move(400, 220)  # QLisave_clickedneEdit의 위치를 지정
        self.okButton.clicked.connect(self.save_clicked)  # 클릭 시 대화상자 닫기

    def setBackgroundImage(self, imagePath):
        # 배경 이미지 설정을 위한 QPixmap 객체 생성
        background = QPixmap(imagePath)
        # QPalette 객체 생성
        palette = QPalette()
        # QPalette의 Background에 QPixmap을 QBrush 객체로 설정
        palette.setBrush(QPalette.Window, QBrush(background))
        # QDialog의 팔레트 설정
        self.setPalette(palette)

     # "Save" 버튼 클릭 이벤트 처리기
    def save_clicked(self):
        QMessageBox.information(self, "Notice", "You must click List Up to enable Sync.")
        new_place = float(self.lineEdit.text())  # QLineEdit에서 새 값을 읽음
        self.saveClicked.emit(new_place)  # 시그널 발생, 새 pick_z_2 값 전달
        self.close()  # 대화상자 닫기