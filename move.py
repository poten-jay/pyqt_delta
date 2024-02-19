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

# 현재 좌표 값 받아오기
x = setting.x
y = setting.y
z = setting.z

# 리스트업 버튼 클릭 후 txt 로 만들기
file_path_move = "document/move_list.txt"
# home_list.txt 파일 만들기
if not os.path.exists(file_path_move):
    with open(file_path_move, 'w') as file:
        for _ in range(4):
            file.write('0 0 0 0 0 0 0 a\n')

class MyMove(QWidget):
    goToStartScreen = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        file_path_home = 'document/move_list.txt'
        with open(file_path_home, 'r') as file1:
            lines_home = file1.readlines()
            first_line_1 = lines_home[0].split()
            print(first_line_1)

        if first_line_1[7] == "T":
        # self.btn = xyz_button(node, x, y, z)
            self.original_pixmap = QPixmap("img/move3.png")
        else:
            self.original_pixmap = QPixmap("img/move44.png")
        self.initUI()
        self.timer = QTimer(self)
        # self.lbl_img = QLabel(self)
        
        # self.initUI

    def initUI(self):
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

        # home_list.txt 의 정보 읽어오기
        file_path_move = 'document/move_list.txt'
        with open(file_path_move, 'r') as file:
            lines = file.readlines()
        # 각 줄의 데이터를 변수에 저장합니다.
        if len(lines) <= 4 :
            # 1번째 줄 데이터 저장
            first_line = lines[0].split()
            # 2번째 줄 데이터 저장
            second_line = lines[1].split()
            # 3번째 줄 데이터 저장
            third_line = lines[2].split()
            # 4번째 줄 데이터 저장
            fourth_line = lines[3].split()

#########################################################################

        file_path_home = 'document/home_list.txt'
        with open(file_path_home, 'r') as file1:
            lines_home = file1.readlines()
        # 각 줄의 데이터를 변수에 저장합니다.
        if len(lines_home) <= 4 :
            # 1번째 줄 데이터 저장
            first_line_1 = lines_home[0].split()
            # 2번째 줄 데이터 저장
            second_line_2 = lines_home[1].split()
            # 3번째 줄 데이터 저장
            third_line_3 = lines_home[2].split()
            # 4번째 줄 데이터 저장
            fourth_line_4 = lines_home[3].split()

######################################################################
        # 0. start_point z => home 의 정보 가져오기
        self.place_z = QLabel(f"{first_line_1[3]}", self)
        self.place_z.setStyleSheet("Color : white")
        self.place_z.setAlignment(Qt.AlignRight)
        self.place_z.setGeometry(516, 464, 55, 25)  # Adjust position and size as needed

        # 1. height_1
        self.label_height_1 = QLabel(f"{first_line[0]}", self)
        self.label_height_1.setStyleSheet("Color : white")
        self.label_height_1.setAlignment(Qt.AlignRight)
        self.label_height_1.setGeometry(168, 233, 55, 25)
        self.height_1 = QLineEdit(self) # 176, 229, 55, 25)
        self.height_1.setGeometry(173, 255, 55, 25)
        self.height_1.setText(first_line[0])
        self.height_1.setAlignment(Qt.AlignRight) # 우측정렬

        # 2. decel_6 z
        self.label_pick_z_2 = QLabel(f"{first_line[1]}", self)
        self.label_pick_z_2.setStyleSheet("Color : white")
        self.label_pick_z_2.setAlignment(Qt.AlignRight)
        self.label_pick_z_2.setGeometry(193, 418, 55, 25)  # Adjust position and size as needed
        self.pick_z_2 = QLineEdit(self)
        self.pick_z_2.setGeometry(198, 440, 55, 25)  # Adjust position and size as needed
        self.pick_z_2.setText(first_line[1])
        self.pick_z_2.setAlignment(Qt.AlignRight)

        # 3. speed
        self.label_speed_3 = QLabel(f"{first_line[2]}", self)
        self.label_speed_3.setStyleSheet("Color : white")
        self.label_speed_3.setAlignment(Qt.AlignRight)
        self.label_speed_3.setGeometry(443, 284, 55, 25)  # Adjust position and size as needed
        self.speed_3 = QLineEdit(self)
        self.speed_3.setGeometry(448, 306, 55, 25)  # Adjust position and size as needed
        self.speed_3.setText(first_line[2])
        self.speed_3.setAlignment(Qt.AlignRight)

        # 4. R
        self.label_r_4 = QLabel(f"{first_line[3]}", self)
        self.label_r_4.setStyleSheet("Color : white")
        self.label_r_4.setAlignment(Qt.AlignRight)
        self.label_r_4.setGeometry(340, 179, 55, 25)  # Adjust position and size as needed
        self.r_4 = QLineEdit(self)
        self.r_4.setGeometry(345, 201, 55, 25)  # Adjust position and size as needed
        self.r_4.setText(first_line[3])
        self.r_4.setAlignment(Qt.AlignRight)

        # 5. deceleration 1
        self.label_decel_5 = QLabel(f"{first_line[4]}", self)
        self.label_decel_5.setStyleSheet("Color : white")
        self.label_decel_5.setAlignment(Qt.AlignRight)
        self.label_decel_5.setGeometry(371, 419, 55, 25)  # Adjust position and size as needed
        self.decel_5 = QLineEdit(self)
        self.decel_5.setGeometry(376, 441, 55, 25)  # Adjust position and size as needed
        self.decel_5.setText(first_line[4])
        self.decel_5.setAlignment(Qt.AlignRight)

        # 6. deceleration 2
        self.label_decel_6 = QLabel(f"{first_line[5]}", self)
        self.label_decel_6.setStyleSheet("Color : white")
        self.label_decel_6.setAlignment(Qt.AlignRight)
        self.label_decel_6.setGeometry(704, 419, 55, 25)  # Adjust position and size as needed
        self.decel_6 = QLineEdit(self)
        self.decel_6.setGeometry(709, 441, 55, 25)  # Adjust position and size as needed
        self.decel_6.setText(first_line[5])
        self.decel_6.setAlignment(Qt.AlignRight)

        # 7. start point of deceleration
        # "30" 
        self.start_point = 30
        # start_point
        # start_point

        # 8. Move L or Move U => F / T

        self.workspace_z = QLabel(f"Max : {setting.z_max}", self)
        self.workspace_z.setStyleSheet("Color : white")
        self.workspace_z.setAlignment(Qt.AlignRight)
        self.workspace_z.setGeometry(110, 150, 100, 30)  # Adjust position and size as needed
        self.workspace_zn = QLabel(f"Min : {setting.z_min}", self)
        self.workspace_zn.setStyleSheet("Color : white")
        self.workspace_zn.setAlignment(Qt.AlignRight)
        self.workspace_zn.setGeometry(110, 530, 100, 30)  # Adjust position and size as needed

#######################################################################


        # 버튼
        # Reset Button
        self.btnReset = QPushButton('Reset', self)
        self.btnReset.setGeometry(580, 500, 50, 30)  # Adjust position and size as needed
        self.btnReset.clicked.connect(self.resetFields)

        # Listup Button
        self.btnListup = QPushButton('List Up', self)
        self.btnListup.setGeometry(640, 500, 90, 30)  # Adjust position and size as needed
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

        # self.home_t()
        # # Home 1버튼
        # self.home1()
        # self.home2()
        # self.home3()
        # self.home4()

        # 뒤로가기 버튼 (순서가 밀리면 안보일 수도 있음)
        self.button()

        # Read items from the file and add them to the ComboBox
        with open('vision/labels.txt', 'r') as file:
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
        self.update_file_last_char('F')  # 파일의 마지막 글자를 'a'로 변경
        

    # ㄷ 자 무빙
    def clickmoveU(self):
        # self.speed_3.setDisabled(False)
        self.decel_6.setDisabled(False)
        # self.start_point.setDisabled(False)
        self.update_file_last_char('T')  # 파일의 마지막 글자를 'b'로 변경

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


    # 마지막 글자 바꾸기
    def update_file_last_char(self, new_char):
        with open(file_path_move, 'r') as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            updated_line = line[:-2] + new_char + '\n'  # 마지막 글자를 new_char로 변경
            updated_lines.append(updated_line)

        with open(file_path_move, 'w') as file:
            file.writelines(updated_lines)

    # 리스트업 클릭시 보낼 정보
    def listupClicked(self):
        # move_list.txt 기존 파일 내용 읽어오기
        existing_lines = []
        if os.path.exists(file_path_move):
            with open(file_path_move, 'r') as file:
                existing_lines = file.readlines()

        # 파일이 없을 경우 초기값 생성
        while len(existing_lines) < 4:
            # existing_lines.append(f'{len(existing_lines) + 1}\n')
            existing_lines.append('0 0 0 0 0 0 0 a\n')

        if existing_lines[0][-2] == 'F':
            self.listupClicked_a()
        else :
            self.listupClicked_b()


        # print(existing_lines[0][-2])


    def listupClicked_a(self):
        try:
            height_1 = float(self.height_1.text())
            pick_z_2 = float(self.pick_z_2.text())
            speed_3 = float(self.speed_3.text())
            r_4 = float(self.r_4.text())
            decel_5 = float(self.decel_5.text())
            decel_6 = float(self.decel_6.text())
            start_point = float(self.start_point)
            
            if setting.z_min <= height_1 <= setting.z_max and \
               setting.z_min <= pick_z_2 <= (height_1 - setting.round) and \
               setting.path_speed_min <= speed_3 <= setting.path_speed_max and \
               setting.bending_min <= r_4 <= setting.bending_max and \
               setting.Deceleration_min <= decel_5 <= setting.Deceleration_max and \
               setting.Deceleration_min <= decel_6 <= setting.Deceleration_max:

                # if start_point == setting.z_max:
                #     decel_5 = 0
                #     speed_3 = 0

                self.updateLabels()

            # if setting.path_speed_min <= height_1 <= setting.path_speed_max and \
            #    setting.bending_min <= r_4 <= setting.bending_max and \
            #    setting.bending_min <= decel_5 <= setting.bending_max and \
            #    setting.z_min <= decel_6 <= setting.z_max and\
            #    setting.z_min <= start_point <= setting.z_max:
            #     self.updateLabels()

                # move_list.txt 기존 파일 내용 읽어오기
                existing_lines = []
                if os.path.exists(file_path_move):
                    with open(file_path_move, 'r') as file:
                        existing_lines = file.readlines()

                # 파일이 없을 경우 초기값 생성
                while len(existing_lines) < 4:
                    # existing_lines.append(f'{len(existing_lines) + 1}\n')
                    existing_lines.append('0 0 0 0 0 0 0 F\n')


                # 0번째 줄 덮어쓰기 또는 추가하기
                existing_lines[0] = f'{height_1} {pick_z_2} {speed_3} {r_4} {decel_5} {decel_6} {start_point} F\n'
                
                # # A1,2,3 통합.
                # existing_lines[0] = f'{height_1} {height_1} {height_1} {r_4} {decel_5} {decel_6} {start_point}\n'


                # 파일에 덮어쓴 내용 저장
                with open(file_path_move, 'w') as file:
                    file.writelines(existing_lines)

                self.label_height_1.setText(str(height_1))
                self.label_pick_z_2.setText(str(pick_z_2))
                self.label_speed_3.setText(str(speed_3))
                self.label_r_4.setText(str(r_4))
                self.label_decel_5.setText(str(decel_5))
                self.label_decel_6.setText(str(decel_6))
                # self.start_point.setText(str(start_point))


                # 확인 메시지 표시
                QMessageBox.information(self, "Info", "Data updated in move_list.txt")
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
            start_point = float(self.start_point)
            
            if setting.z_min <= height_1 <= setting.z_max and \
               setting.z_min <= pick_z_2 <= (height_1 - setting.round) and \
               setting.path_speed_min <= speed_3 <= setting.path_speed_max and \
               setting.bending_min <= r_4 <= setting.bending_max and \
               setting.Deceleration_min <= decel_5 <= setting.Deceleration_max and \
               setting.Deceleration_min <= decel_6 <= setting.Deceleration_max:


            # if setting.Deceleration_min <= height_1 <= setting.Deceleration_max and \
            #    setting.path_speed_min <= pick_z_2 <= setting.path_speed_max and \
            #    setting.Deceleration_min <= speed_3 <= setting.Deceleration_max and \
            #    setting.bending_min <= r_4 <= setting.bending_max and \
            #    setting.bending_min <= decel_5 <= setting.bending_max and \
            #    setting.z_min <= decel_6 <= setting.z_max and\
            #    setting.z_min <= start_point <= setting.z_max:

            #     if start_point == setting.z_max:
            #         decel_5 = 0
            #         speed_3 = 0

                self.updateLabels()

            # if setting.path_speed_min <= height_1 <= setting.path_speed_max and \
            #    setting.bending_min <= r_4 <= setting.bending_max and \
            #    setting.bending_min <= decel_5 <= setting.bending_max and \
            #    setting.z_min <= decel_6 <= setting.z_max and\
            #    setting.z_min <= start_point <= setting.z_max:
            #     self.updateLabels()

                # move_list.txt 기존 파일 내용 읽어오기
                existing_lines = []
                if os.path.exists(file_path_move):
                    with open(file_path_move, 'r') as file:
                        existing_lines = file.readlines()

                # 파일이 없을 경우 초기값 생성
                while len(existing_lines) < 4:
                    # existing_lines.append(f'{len(existing_lines) + 1}\n')
                    existing_lines.append('0 0 0 0 0 0 0 F\n')


                # 0번째 줄 덮어쓰기 또는 추가하기
                existing_lines[0] = f'{height_1} {pick_z_2} {speed_3} {r_4} {decel_5} {decel_6} {start_point} T\n'
                
                # # A1,2,3 통합.
                # existing_lines[0] = f'{height_1} {height_1} {height_1} {r_4} {decel_5} {decel_6} {start_point}\n'


                # 파일에 덮어쓴 내용 저장
                with open(file_path_move, 'w') as file:
                    file.writelines(existing_lines)

                self.label_height_1.setText(str(height_1))
                self.label_pick_z_2.setText(str(pick_z_2))
                self.label_speed_3.setText(str(speed_3))
                self.label_r_4.setText(str(r_4))
                self.label_decel_5.setText(str(decel_5))
                self.label_decel_6.setText(str(decel_6))
                # self.start_point.setText(str(start_point))

                # 확인 메시지 표시
                QMessageBox.information(self, "Info", "Data updated in move_list.txt")
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

        self.btnback.clicked.connect(self.close)
        self.btnback.clicked.connect(self.goToStartScreen.emit)

    # def home_t(self):
    #     # 뒤로 가기 버튼
    #     self.btnhomet = QPushButton('Total', self)
    #     self.btnhomet.clicked.connect(self.goToStartScreen.emit)
    #     self.btnhomet.setGeometry(200, 86, 80, 40)
    #     # self.btnhomet.raise_()  # Raise the button to the top of the widget stack
    # def home1(self):
    #     # 뒤로 가기 버튼
    #     self.btnhome1 = QPushButton('Home1', self)
    #     self.btnhome1.clicked.connect(self.goToStartScreen.emit)
    #     self.btnhome1.setGeometry(300, 86, 80, 40)
    #     # self.btnhome1.raise_()  # Raise the button to the top of the widget stack
    #     self.btnhome1.setDisabled(True)

    # def home2(self):
    #     # 뒤로 가기 버튼
    #     self.btnhome2 = QPushButton('Home2', self)
    #     self.btnhome2.clicked.connect(self.goToStartScreen.emit)
    #     self.btnhome2.setGeometry(400, 86, 80, 40)
    #     # self.btnhome2.raise_()  # Raise the button to the top of the widget stack
    #     self.btnhome2.setDisabled(True)

    # def home3(self):
    #     # 뒤로 가기 버튼
    #     self.btnhome3 = QPushButton('Home3', self)
    #     self.btnhome3.clicked.connect(self.goToStartScreen.emit)
    #     self.btnhome3.setGeometry(500, 86, 80, 40)
    #     # self.btnhome3.raise_()  # Raise the button to the top of the widget stack
    #     self.btnhome3.setDisabled(True)

    # def home4(self):
    #     # 뒤로 가기 버튼
    #     self.btnhome4 = QPushButton('Home4', self)
    #     self.btnhome4.clicked.connect(self.goToStartScreen.emit)
    #     self.btnhome4.setGeometry(600, 86, 80, 40)
    #     # self.btnhome4.raise_()  # Raise the button to the top of the widget stack
    #     self.btnhome4.setDisabled(True)


    def onBackButtonClick(self):
        # Emit the signal when the button is clicked
        self.goToStartScreen.emit()


    # 직접 입력창 리셋
    def resetFields(self):

        self.height_1.setText(str(-900))
        self.pick_z_2.setText(str(-950))
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
        file_path_home = 'document/home_list.txt'
        with open(file_path_home, 'r') as file1:
            lines_home = file1.readlines()
        # 각 줄의 데이터를 변수에 저장합니다.
        if len(lines_home) <= 4 :
            # 1번째 줄 데이터 저장
            first_line_1 = lines_home[0].split()
            # 2번째 줄 데이터 저장
            second_line_2 = lines_home[1].split()
            # 3번째 줄 데이터 저장
            third_line_3 = lines_home[2].split()
            # 4번째 줄 데이터 저장
            fourth_line_4 = lines_home[3].split()

        # lebel 정보 창
        self.label1_label = QLabel(f"{first_line_1[0]}", self)
        self.label1_label.setStyleSheet("Color : white")
        self.label1_label.setAlignment(Qt.AlignRight)
        self.label1_label.setGeometry(313, 153, 100, 30)  # Adjust position and size as needed
        self.label1_x = QLabel(f"{first_line_1[1]}", self)
        self.label1_x.setStyleSheet("Color : white")
        self.label1_x.setAlignment(Qt.AlignRight)
        self.label1_x.setGeometry(412, 153, 100, 30)  # Adjust position and size as needed
        self.label1_y = QLabel(f"{first_line_1[2]}", self)
        self.label1_y.setStyleSheet("Color : white")
        self.label1_y.setAlignment(Qt.AlignRight)
        self.label1_y.setGeometry(531, 153, 100, 30)  # Adjust position and size as needed
        self.label1_z = QLabel(f"{first_line_1[3]}", self)
        self.label1_z.setStyleSheet("Color : white")
        self.label1_z.setAlignment(Qt.AlignRight)
        self.label1_z.setGeometry(649, 153, 100, 30)  # Adjust position and size as needed


########### start.py를 실행하면 아래는 필요 없음 #####################

# class GUI_Node(Node):
#     def __init__(self):
#         super().__init__('gui_node')
#         self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)
#         self.app = QApplication(sys.argv)
#         self.gui = MyMove(self)
#         self.timer = self.create_timer(0.1, self.timer_callback)

#     def timer_callback(self):
#         pass


# def main(args=None):
#     rclpy.init(args=args)
#     gui_node = GUI_Node()

#     exit_code = gui_node.app.exec_()

#     gui_node.destroy_node()
#     rclpy.shutdown()

#     sys.exit(exit_code)

# if __name__ == '__main__':
#     main()
