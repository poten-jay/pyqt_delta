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
            file.write('0 0 0 0 0 0 0\n')

class MyMove(QWidget):
    goToStartScreen = pyqtSignal()

    def __init__(self, node):
        super().__init__()
        self.node = node
        # self.btn = xyz_button(node, x, y, z)
        self.initUI()
        self.timer = QTimer(self)
        self.initUI

    def initUI(self):
######## 이미지 넣기 #######################################################
        original_pixmap = QPixmap("img/move2.png")
        scaled_pixmap = original_pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # QLabel 생성 및 QPixmap 설정
        lbl_img = QLabel(self)
        lbl_img.setPixmap(scaled_pixmap)
        lbl_img.setGeometry(0, 0, scaled_pixmap.width(), scaled_pixmap.height())
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

        # txt 에서 읽어온 현재 상태 (now)
        # 좌표 표시 수정 => (x-5, y+4)
        self.label_spped_a1 = QLabel(f"{first_line[0]}", self)
        self.label_spped_a1.setStyleSheet("Color : white")
        self.label_spped_a1.setAlignment(Qt.AlignRight)
        self.label_spped_a1.setGeometry(325, 410, 55, 25)  # Adjust position and size as needed
        self.label_spped_a2 = QLabel(f"{first_line[1]}", self)
        self.label_spped_a2.setStyleSheet("Color : white")
        self.label_spped_a2.setAlignment(Qt.AlignRight)
        self.label_spped_a2.setGeometry(412, 258, 55, 25)  # Adjust position and size as needed
        self.label_spped_a3 = QLabel(f"{first_line[2]}", self)
        self.label_spped_a3.setStyleSheet("Color : white")
        self.label_spped_a3.setAlignment(Qt.AlignRight)
        self.label_spped_a3.setGeometry(508, 410, 55, 25)  # Adjust position and size as needed
        self.label_bending_b = QLabel(f"{first_line[3]}", self)
        self.label_bending_b.setStyleSheet("Color : white")
        self.label_bending_b.setAlignment(Qt.AlignRight)
        self.label_bending_b.setGeometry(253, 246, 55, 25)  # Adjust position and size as needed
        self.label_bending_c = QLabel(f"{first_line[4]}", self)
        self.label_bending_c.setStyleSheet("Color : white")
        self.label_bending_c.setAlignment(Qt.AlignRight)
        self.label_bending_c.setGeometry(578, 246, 55, 25)  # Adjust position and size as needed
        self.label_pick = QLabel(f"{first_line[5]}", self)
        self.label_pick.setStyleSheet("Color : white")
        self.label_pick.setAlignment(Qt.AlignRight)
        self.label_pick.setGeometry(155, 390, 55, 25)  # Adjust position and size as needed
        self.label_place = QLabel(f"{first_line[6]}", self)
        self.label_place.setStyleSheet("Color : white")
        self.label_place.setAlignment(Qt.AlignRight)
        self.label_place.setGeometry(670, 405, 55, 25)  # Adjust position and size as needed


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

        # self.label2_label = QLabel(f"{second_line[0]}", self)
        # self.label2_label.setStyleSheet("Color : white")
        # self.label2_label.setAlignment(Qt.AlignRight)
        # self.label2_label.setGeometry(313, 153, 100, 30)  # Adjust position and size as needed
        # self.label2_x = QLabel(f"{second_line[1]}", self)
        # self.label2_x.setStyleSheet("Color : white")
        # self.label2_x.setAlignment(Qt.AlignRight)
        # self.label2_x.setGeometry(412, 153, 100, 30)  # Adjust position and size as needed
        # self.label2_y = QLabel(f"{second_line[2]}", self)
        # self.label2_y.setStyleSheet("Color : white")
        # self.label2_y.setAlignment(Qt.AlignRight)
        # self.label2_y.setGeometry(531, 153, 100, 30)  # Adjust position and size as needed
        # self.label2_z = QLabel(f"{second_line[3]}", self)
        # self.label2_z.setStyleSheet("Color : white")
        # self.label2_z.setAlignment(Qt.AlignRight)
        # self.label2_z.setGeometry(649, 153, 100, 30)  # Adjust position and size as needed

        # self.label3_label = QLabel(f"{third_line[0]}", self)
        # self.label3_label.setStyleSheet("Color : white")
        # self.label3_label.setAlignment(Qt.AlignRight)
        # self.label3_label.setGeometry(313, 189, 100, 30)  # Adjust position and size as needed
        # self.label3_x = QLabel(f"{third_line[1]}", self)
        # self.label3_x.setStyleSheet("Color : white")
        # self.label3_x.setAlignment(Qt.AlignRight)
        # self.label3_x.setGeometry(412, 189, 100, 30)  # Adjust position and size as needed
        # self.label3_y = QLabel(f"{third_line[2]}", self)
        # self.label3_y.setStyleSheet("Color : white")
        # self.label3_y.setAlignment(Qt.AlignRight)
        # self.label3_y.setGeometry(531, 189, 100, 30)  # Adjust position and size as needed
        # self.label3_z = QLabel(f"{third_line[3]}", self)
        # self.label3_z.setStyleSheet("Color : white")
        # self.label3_z.setAlignment(Qt.AlignRight)
        # self.label3_z.setGeometry(649, 189, 100, 30)  # Adjust position and size as needed

        # self.label4_label = QLabel(f"{fourth_line[0]}", self)
        # self.label4_label.setStyleSheet("Color : white")
        # self.label4_label.setAlignment(Qt.AlignRight)
        # self.label4_label.setGeometry(313, 225, 100, 30)  # Adjust position and size as needed
        # self.label4_x = QLabel(f"{fourth_line[1]}", self)
        # self.label4_x.setStyleSheet("Color : white")
        # self.label4_x.setAlignment(Qt.AlignRight)
        # self.label4_x.setGeometry(412, 225, 100, 30)  # Adjust position and size as needed
        # self.label4_y = QLabel(f"{fourth_line[2]}", self)
        # self.label4_y.setStyleSheet("Color : white")
        # self.label4_y.setAlignment(Qt.AlignRight)
        # self.label4_y.setGeometry(531, 225, 100, 30)  # Adjust position and size as needed
        # self.label4_z = QLabel(f"{fourth_line[3]}", self)
        # self.label4_z.setStyleSheet("Color : white")
        # self.label4_z.setAlignment(Qt.AlignRight)
        # self.label4_z.setGeometry(649, 225, 100, 30)  # Adjust position and size as needed

        # workspace 정보
        # self.workspace_x = QLabel(f"Max : {setting.x_max}", self)
        # self.workspace_x.setStyleSheet("Color : white")
        # self.workspace_x.setAlignment(Qt.AlignRight)
        # self.workspace_x.setGeometry(5, 360, 100, 30)  # Adjust position and size as needed
        # self.workspace_xn = QLabel(f"Min : {setting.x_min}", self)
        # self.workspace_xn.setStyleSheet("Color : white")
        # self.workspace_xn.setAlignment(Qt.AlignRight)
        # self.workspace_xn.setGeometry(150, 360, 100, 30)  # Adjust position and size as needed
        
        # self.workspace_y = QLabel(f"Max : {setting.y_max}", self)
        # self.workspace_y.setStyleSheet("Color : white")
        # self.workspace_y.setAlignment(Qt.AlignRight)
        # self.workspace_y.setGeometry(70, 395, 100, 30)  # Adjust position and size as needed
        # self.workspace_yn = QLabel(f"Min : {setting.y_min}", self)
        # self.workspace_yn.setStyleSheet("Color : white")
        # self.workspace_yn.setAlignment(Qt.AlignRight)
        # self.workspace_yn.setGeometry(110, 335, 100, 30)  # Adjust position and size as needed
        
        self.workspace_z = QLabel(f"Max : {setting.z_max}", self)
        self.workspace_z.setStyleSheet("Color : white")
        self.workspace_z.setAlignment(Qt.AlignRight)
        self.workspace_z.setGeometry(126, 300, 100, 30)  # Adjust position and size as needed
        self.workspace_zn = QLabel(f"Min : {setting.z_min}", self)
        self.workspace_zn.setStyleSheet("Color : white")
        self.workspace_zn.setAlignment(Qt.AlignRight)
        self.workspace_zn.setGeometry(126, 470, 100, 30)  # Adjust position and size as needed





        # path_speed_a1
        self.path_speed_a1 = QLineEdit(self)
        self.path_speed_a1.setGeometry(330, 432, 55, 25)  # Adjust position and size as needed
        self.path_speed_a1.setText(str(1))
        self.path_speed_a1.setAlignment(Qt.AlignRight) # 우측정렬
        # path_speed_a2
        self.path_speed_a2 = QLineEdit(self)
        self.path_speed_a2.setGeometry(417, 283, 55, 25)  # Adjust position and size as needed
        self.path_speed_a2.setText(str(1))
        self.path_speed_a2.setAlignment(Qt.AlignRight)
        # path_speed_a3
        self.path_speed_a3 = QLineEdit(self)
        self.path_speed_a3.setGeometry(513, 432, 55, 25)  # Adjust position and size as needed
        self.path_speed_a3.setText(str(1))
        self.path_speed_a3.setAlignment(Qt.AlignRight)
        # bending_b
        self.bending_b = QLineEdit(self)
        self.bending_b.setGeometry(258, 270, 55, 25)  # Adjust position and size as needed
        self.bending_b.setText(str(50))
        self.bending_b.setAlignment(Qt.AlignRight)
        # bending_c
        self.bending_c = QLineEdit(self)
        self.bending_c.setGeometry(583, 270, 55, 25)  # Adjust position and size as needed
        self.bending_c.setText(str(50))
        self.bending_c.setAlignment(Qt.AlignRight)
        # pick_height
        self.pick_height = QLineEdit(self)
        self.pick_height.setGeometry(160, 414, 55, 25)  # Adjust position and size as needed
        self.pick_height.setText(str(-350))
        self.pick_height.setAlignment(Qt.AlignRight)
        # place_height
        self.place_height = QLineEdit(self)
        self.place_height.setGeometry(675, 429, 55, 25)  # Adjust position and size as needed
        self.place_height.setText(str(-350))
        self.place_height.setAlignment(Qt.AlignRight)


        # 버튼
        # Reset Button
        self.btnReset = QPushButton('Reset', self)
        self.btnReset.setGeometry(580, 500, 50, 30)  # Adjust position and size as needed
        self.btnReset.clicked.connect(self.resetFields)

        # Listup Button
        self.btnListup = QPushButton('List Up', self)
        self.btnListup.setGeometry(640, 500, 90, 30)  # Adjust position and size as needed
        self.btnListup.clicked.connect(self.listupClicked)

        self.home_t()
        # Home 1버튼
        self.home1()
        self.home2()
        self.home3()
        self.home4()

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

    # 리스트업 클릭시 보낼 정보
    def listupClicked(self):
        try:
            path_a1 = float(self.path_speed_a1.text())
            path_a2 = float(self.path_speed_a2.text())
            path_a3 = float(self.path_speed_a3.text())
            bending_b = float(self.bending_b.text())
            bending_c = float(self.bending_c.text())
            pick = float(self.pick_height.text())
            place = float(self.place_height.text())
            
            if setting.path_speed_min <= path_a1 <= setting.path_speed_max and \
               setting.path_speed_min <= path_a2 <= setting.path_speed_max and \
               setting.path_speed_min <= path_a3 <= setting.path_speed_max and \
               setting.bending_min <= bending_b <= setting.bending_max and \
               setting.bending_min <= bending_c <= setting.bending_max and \
               setting.z_min <= pick <= setting.z_max and\
               setting.z_min <= place <= setting.z_max:

                if place == setting.z_max:
                    bending_c = 0
                    path_a3 = 0

                self.updateLabels()

            # if setting.path_speed_min <= path_a1 <= setting.path_speed_max and \
            #    setting.bending_min <= bending_b <= setting.bending_max and \
            #    setting.bending_min <= bending_c <= setting.bending_max and \
            #    setting.z_min <= pick <= setting.z_max and\
            #    setting.z_min <= place <= setting.z_max:
            #     self.updateLabels()

                # move_list.txt 기존 파일 내용 읽어오기
                existing_lines = []
                if os.path.exists(file_path_move):
                    with open(file_path_move, 'r') as file:
                        existing_lines = file.readlines()

                # 파일이 없을 경우 초기값 생성
                while len(existing_lines) < 4:
                    # existing_lines.append(f'{len(existing_lines) + 1}\n')
                    existing_lines.append('0 0 0 0 0 0 0\n')


                # 0번째 줄 덮어쓰기 또는 추가하기
                existing_lines[0] = f'{path_a1} {path_a2} {path_a3} {bending_b} {bending_c} {pick} {place}\n'
                
                # # A1,2,3 통합.
                # existing_lines[0] = f'{path_a1} {path_a1} {path_a1} {bending_b} {bending_c} {pick} {place}\n'


                # 파일에 덮어쓴 내용 저장
                with open(file_path_move, 'w') as file:
                    file.writelines(existing_lines)

                self.label_spped_a1.setText(str(path_a1))
                self.label_spped_a2.setText(str(path_a2))
                self.label_spped_a3.setText(str(path_a3))
                self.label_bending_b.setText(str(bending_b))
                self.label_bending_c.setText(str(bending_c))
                self.label_pick.setText(str(pick))
                self.label_place.setText(str(place))


                # 확인 메시지 표시
                QMessageBox.information(self, "Info", "Data updated in move_list.txt")
            else:
                # Handle out of range values
                print("Values out of range")
                self.path_speed_a1.setText("Out of Range")
                self.path_speed_a1.setStyleSheet("color: red;")
                self.path_speed_a1.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.path_speed_a2.setText("Out of Range")
                self.path_speed_a2.setStyleSheet("color: red;")
                self.path_speed_a2.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.path_speed_a3.setText("Out of Range")
                self.path_speed_a3.setStyleSheet("color: red;")
                self.path_speed_a3.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.bending_b.setText("Out of Range")
                self.bending_b.setStyleSheet("color: red;")
                self.bending_b.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.bending_c.setText("Out of Range")
                self.bending_c.setStyleSheet("color: red;")
                self.bending_c.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.pick_height.setText("Out of Range")
                self.pick_height.setStyleSheet("color: red;")
                self.pick_height.setAlignment(Qt.AlignRight)
                print("Values out of range")
                self.place_height.setText("Out of Range")
                self.place_height.setStyleSheet("color: red;")
                self.place_height.setAlignment(Qt.AlignRight)


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
        if self.label_spped_a1 == setting.path_speed_max or self.label_spped_a1 == setting.path_speed_min:
            self.label_spped_a1.setStyleSheet("Color : red")
            self.label_spped_a1.setText(f'Limit {self.label_spped_a1}')
        else:
            self.label_spped_a1.setStyleSheet("Color : white")
            self.label_spped_a1.setText(f'{self.label_spped_a1}')

        if self.label_spped_a2 == setting.path_speed_max or self.label_spped_a2 == setting.path_speed_min:
            self.label_spped_a2.setStyleSheet("Color : red")
            self.label_spped_a2.setText(f'Limit {self.label_spped_a2}')
        else:
            self.label_spped_a2.setStyleSheet("Color : white")
            self.label_spped_a2.setText(f'{self.label_spped_a2}')

        if self.label_spped_a3 == setting.path_speed_max or self.label_spped_a3 == setting.path_speed_min:
            self.label_spped_a3.setStyleSheet("Color : red")
            self.label_spped_a3.setText(f'Limit {self.label_spped_a3}')
        else:
            self.label_spped_a3.setStyleSheet("Color : white")
            self.label_spped_a3.setText(f'{self.label_spped_a3}')
##############
        if self.label_bending_b == setting.bending_max or self.label_bending_b == setting.bending_min:
            self.label_bending_b.setStyleSheet("Color : red")
            self.label_bending_b.setText(f'Limit {self.label_bending_b}')
        else:
            self.label_bending_b.setStyleSheet("Color : white")
            self.label_bending_b.setText(f'{self.label_bending_b}')

        if self.label_bending_c == setting.bending_max or self.label_bending_c == setting.bending_min:
            self.label_bending_c.setStyleSheet("Color : red")
            self.label_bending_c.setText(f'Limit {self.label_bending_c}')
        else:
            self.label_bending_c.setStyleSheet("Color : white")
            self.label_bending_c.setText(f'{self.label_bending_c}')
##################
        if self.label_pick == setting.z_max or self.label_pick == setting.z_min:
            self.label_pick.setStyleSheet("Color : red")
            self.label_pick.setText(f'Limit {self.label_pick}')
        else:
            self.label_pick.setStyleSheet("Color : white")
            self.label_pick.setText(f'{self.label_pick}')

        if self.label_place == setting.z_max or self.label_place == setting.z_min:
            self.label_place.setStyleSheet("Color : red")
            self.label_place.setText(f'Limit {self.label_place}')
        else:
            self.label_place.setStyleSheet("Color : white")
            self.label_place.setText(f'{self.label_place}')


    def comboBoxIndexChanged(self, index):
        # Handle the ComboBox item selection here
        selected_item = self.comboBox.currentText()
        print(f"Selected item: {selected_item}")

    # 버튼 위치 및 사이즈 결정
    def button(self):

        # 뒤로 가기 버튼
        self.btnback = QPushButton('<<', self)
        self.btnback.clicked.connect(self.goToStartScreen.emit)
        self.btnback.setGeometry(0, 528, 50, 50)
        # self.btnback.raise_()  # Raise the button to the top of the widget stack

    def home_t(self):
        # 뒤로 가기 버튼
        self.btnhomet = QPushButton('Total', self)
        self.btnhomet.clicked.connect(self.goToStartScreen.emit)
        self.btnhomet.setGeometry(200, 86, 80, 40)
        # self.btnhomet.raise_()  # Raise the button to the top of the widget stack
    def home1(self):
        # 뒤로 가기 버튼
        self.btnhome1 = QPushButton('Home1', self)
        self.btnhome1.clicked.connect(self.goToStartScreen.emit)
        self.btnhome1.setGeometry(300, 86, 80, 40)
        # self.btnhome1.raise_()  # Raise the button to the top of the widget stack
    def home2(self):
        # 뒤로 가기 버튼
        self.btnhome2 = QPushButton('Home2', self)
        self.btnhome2.clicked.connect(self.goToStartScreen.emit)
        self.btnhome2.setGeometry(400, 86, 80, 40)
        # self.btnhome2.raise_()  # Raise the button to the top of the widget stack
    def home3(self):
        # 뒤로 가기 버튼
        self.btnhome3 = QPushButton('Home3', self)
        self.btnhome3.clicked.connect(self.goToStartScreen.emit)
        self.btnhome3.setGeometry(500, 86, 80, 40)
        # self.btnhome3.raise_()  # Raise the button to the top of the widget stack
    def home4(self):
        # 뒤로 가기 버튼
        self.btnhome4 = QPushButton('Home4', self)
        self.btnhome4.clicked.connect(self.goToStartScreen.emit)
        self.btnhome4.setGeometry(600, 86, 80, 40)
        # self.btnhome4.raise_()  # Raise the button to the top of the widget stack



    def onBackButtonClick(self):
        # Emit the signal when the button is clicked
        self.goToStartScreen.emit()


    # 직접 입력창 리셋
    def resetFields(self):

        self.path_speed_a1.setText(str(1))
        self.path_speed_a2.setText(str(1))
        self.path_speed_a3.setText(str(1))
        self.bending_b.setText(str(50))
        self.bending_c.setText(str(50))
        self.pick_height.setText(str(-350))
        self.place_height.setText(str(-350))
        # Optionally, reset the style if it's changed when values are out of range
        self.path_speed_a1.setStyleSheet("color: black;")
        self.path_speed_a2.setStyleSheet("color: black;")
        self.path_speed_a3.setStyleSheet("color: black;")
        self.bending_b.setStyleSheet("color: black;")
        self.bending_c.setStyleSheet("color: black;")
        self.pick_height.setStyleSheet("color: black;")
        self.place_height.setStyleSheet("color: black;")


########### start.py를 실행하면 아래는 필요 없음 #####################

class GUI_Node(Node):
    def __init__(self):
        super().__init__('gui_node')
        self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)
        self.app = QApplication(sys.argv)
        self.gui = MyMove(self)
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
