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

# 리스트업 버튼 클릭 후 txt 로 만들기
file_path = "/workspace/pyqt_delta/document/home_list.txt"
# home_list.txt 파일 만들기
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        for _ in range(4):
            file.write('0 0 0 0\n')

class MyHome(QWidget):
    goToStartScreen = pyqtSignal()

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.btn = xyz_button(node, x, y, z)
        self.initUI()
        self.timer = QTimer(self)
        self.initUI

    def initUI(self):
######## 이미지 넣기 #######################################################
        original_pixmap = QPixmap("/workspace/pyqt_delta/img/home2.png")
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

        # 화면에 표시되는 xyz 좌표
        self.labelX = QLabel(f"{x}", self)
        self.labelX.setStyleSheet("Color : white")
        self.labelX.setAlignment(Qt.AlignRight)
        self.labelX.setGeometry(275, 410, 100, 30)  # Adjust position and size as needed
        self.labelY = QLabel(f"{y}", self)
        self.labelY.setStyleSheet("Color : white")
        self.labelY.setAlignment(Qt.AlignRight)
        self.labelY.setGeometry(430, 410, 100, 30)  # Adjust position and size as needed
        self.labelZ = QLabel(f"{z}", self)
        self.labelZ.setStyleSheet("Color : white")
        self.labelZ.setAlignment(Qt.AlignRight)
        self.labelZ.setGeometry(590, 410, 100, 30)  # Adjust position and size as needed

        # home_list.txt 의 정보 읽어오기
        with open(file_path, 'r') as file:
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

        # lebel 정보 창
        self.label1_label = QLabel(f"{first_line[0]}", self)
        self.label1_label.setStyleSheet("Color : white")
        self.label1_label.setAlignment(Qt.AlignRight)
        self.label1_label.setGeometry(313, 116, 100, 30)  # Adjust position and size as needed
        self.label1_x = QLabel(f"{first_line[1]}", self)
        self.label1_x.setStyleSheet("Color : white")
        self.label1_x.setAlignment(Qt.AlignRight)
        self.label1_x.setGeometry(412, 116, 100, 30)  # Adjust position and size as needed
        self.label1_y = QLabel(f"{first_line[2]}", self)
        self.label1_y.setStyleSheet("Color : white")
        self.label1_y.setAlignment(Qt.AlignRight)
        self.label1_y.setGeometry(531, 116, 100, 30)  # Adjust position and size as needed
        self.label1_z = QLabel(f"{first_line[3]}", self)
        self.label1_z.setStyleSheet("Color : white")
        self.label1_z.setAlignment(Qt.AlignRight)
        self.label1_z.setGeometry(649, 116, 100, 30)  # Adjust position and size as needed

        self.label2_label = QLabel(f"{second_line[0]}", self)
        self.label2_label.setStyleSheet("Color : white")
        self.label2_label.setAlignment(Qt.AlignRight)
        self.label2_label.setGeometry(313, 153, 100, 30)  # Adjust position and size as needed
        self.label2_x = QLabel(f"{second_line[1]}", self)
        self.label2_x.setStyleSheet("Color : white")
        self.label2_x.setAlignment(Qt.AlignRight)
        self.label2_x.setGeometry(412, 153, 100, 30)  # Adjust position and size as needed
        self.label2_y = QLabel(f"{second_line[2]}", self)
        self.label2_y.setStyleSheet("Color : white")
        self.label2_y.setAlignment(Qt.AlignRight)
        self.label2_y.setGeometry(531, 153, 100, 30)  # Adjust position and size as needed
        self.label2_z = QLabel(f"{second_line[3]}", self)
        self.label2_z.setStyleSheet("Color : white")
        self.label2_z.setAlignment(Qt.AlignRight)
        self.label2_z.setGeometry(649, 153, 100, 30)  # Adjust position and size as needed

        self.label3_label = QLabel(f"{third_line[0]}", self)
        self.label3_label.setStyleSheet("Color : white")
        self.label3_label.setAlignment(Qt.AlignRight)
        self.label3_label.setGeometry(313, 189, 100, 30)  # Adjust position and size as needed
        self.label3_x = QLabel(f"{third_line[1]}", self)
        self.label3_x.setStyleSheet("Color : white")
        self.label3_x.setAlignment(Qt.AlignRight)
        self.label3_x.setGeometry(412, 189, 100, 30)  # Adjust position and size as needed
        self.label3_y = QLabel(f"{third_line[2]}", self)
        self.label3_y.setStyleSheet("Color : white")
        self.label3_y.setAlignment(Qt.AlignRight)
        self.label3_y.setGeometry(531, 189, 100, 30)  # Adjust position and size as needed
        self.label3_z = QLabel(f"{third_line[3]}", self)
        self.label3_z.setStyleSheet("Color : white")
        self.label3_z.setAlignment(Qt.AlignRight)
        self.label3_z.setGeometry(649, 189, 100, 30)  # Adjust position and size as needed

        self.label4_label = QLabel(f"{fourth_line[0]}", self)
        self.label4_label.setStyleSheet("Color : white")
        self.label4_label.setAlignment(Qt.AlignRight)
        self.label4_label.setGeometry(313, 225, 100, 30)  # Adjust position and size as needed
        self.label4_x = QLabel(f"{fourth_line[1]}", self)
        self.label4_x.setStyleSheet("Color : white")
        self.label4_x.setAlignment(Qt.AlignRight)
        self.label4_x.setGeometry(412, 225, 100, 30)  # Adjust position and size as needed
        self.label4_y = QLabel(f"{fourth_line[2]}", self)
        self.label4_y.setStyleSheet("Color : white")
        self.label4_y.setAlignment(Qt.AlignRight)
        self.label4_y.setGeometry(531, 225, 100, 30)  # Adjust position and size as needed
        self.label4_z = QLabel(f"{fourth_line[3]}", self)
        self.label4_z.setStyleSheet("Color : white")
        self.label4_z.setAlignment(Qt.AlignRight)
        self.label4_z.setGeometry(649, 225, 100, 30)  # Adjust position and size as needed

        # workspace 정보
        self.workspace_x = QLabel(f"Max : {setting.x_max}", self)
        self.workspace_x.setStyleSheet("Color : white")
        self.workspace_x.setAlignment(Qt.AlignRight)
        self.workspace_x.setGeometry(5, 360, 100, 30)  # Adjust position and size as needed
        self.workspace_xn = QLabel(f"Min : {setting.x_min}", self)
        self.workspace_xn.setStyleSheet("Color : white")
        self.workspace_xn.setAlignment(Qt.AlignRight)
        self.workspace_xn.setGeometry(150, 360, 100, 30)  # Adjust position and size as needed
        
        self.workspace_y = QLabel(f"Max : {setting.y_max}", self)
        self.workspace_y.setStyleSheet("Color : white")
        self.workspace_y.setAlignment(Qt.AlignRight)
        self.workspace_y.setGeometry(70, 395, 100, 30)  # Adjust position and size as needed
        self.workspace_yn = QLabel(f"Min : {setting.y_min}", self)
        self.workspace_yn.setStyleSheet("Color : white")
        self.workspace_yn.setAlignment(Qt.AlignRight)
        self.workspace_yn.setGeometry(110, 335, 100, 30)  # Adjust position and size as needed
        
        self.workspace_z = QLabel(f"Max : {setting.z_max}", self)
        self.workspace_z.setStyleSheet("Color : white")
        self.workspace_z.setAlignment(Qt.AlignRight)
        self.workspace_z.setGeometry(5, 415, 100, 30)  # Adjust position and size as needed
        self.workspace_zn = QLabel(f"Min : {setting.z_min}", self)
        self.workspace_zn.setStyleSheet("Color : white")
        self.workspace_zn.setAlignment(Qt.AlignRight)
        self.workspace_zn.setGeometry(5, 470, 100, 30)  # Adjust position and size as needed
        

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

        # 버튼
        # Reset Button
        self.btnReset = QPushButton('Reset', self)
        self.btnReset.setGeometry(615, 540, 50, 30)  # Adjust position and size as needed
        self.btnReset.clicked.connect(self.resetFields)
        # Update Button
        self.btnUpdate = QPushButton('Run', self)
        self.btnUpdate.setGeometry(680, 540, 50, 30)  # Adjust as needed
        self.btnUpdate.clicked.connect(self.updateXYZ)
        # Listup Button
        self.btnListup = QPushButton('List Up', self)
        self.btnListup.setGeometry(640, 480, 90, 25)  # Adjust position and size as needed
        self.btnListup.clicked.connect(self.listupClicked)

        # 뒤로가기 버튼 (순서가 밀리면 안보일 수도 있음)
        self.button()

        # 1,2,3,4 를 보여주는 콤보박스
        self.comboBox1 = QComboBox(self)
        self.comboBox1.setGeometry(305, 480, 90, 25)  # Adjust position and size as needed
        items = ["1", "2", "3", "4"]
        self.comboBox1.addItems(items)

        # lable 종류 txt애서 읽어와 보여주기
        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(460, 480, 90, 25)  # Adjust position and size as needed

        # Read items from the file and add them to the ComboBox
        with open('/workspace/pyqt_delta/vision/labels.txt', 'r') as file:
            items = file.read().splitlines()
            self.comboBox.addItems(items)


        # # Create a QTextEdit widget
        # self.textEdit = QTextEdit(self)
        # self.textEdit.setGeometry(100, 300, 300, 100)  # Adjust position and size as needed


    # 리스트업 클릭시 보낼 정보
    def listupClicked(self):
        try:
            selected_num = self.comboBox1.currentText()
            selected_item = self.comboBox.currentText()
            x_val = float(self.lineEditX.text())
            y_val = float(self.lineEditY.text())
            z_val = float(self.lineEditZ.text())
            
            if setting.x_min <= x_val <= setting.x_max and \
               setting.y_min <= y_val <= setting.y_max and \
               setting.z_min <= z_val <= setting.z_max:
                self.btn.input_x = x_val
                self.btn.input_y = y_val
                self.btn.input_z = z_val
                self.updateLabels()

                if selected_num == "1":
                    self.label1_label.setText(selected_item)
                    self.label1_x.setText(str(x_val))
                    self.label1_y.setText(str(y_val))
                    self.label1_z.setText(str(z_val))
                elif selected_num == "2":
                    self.label2_label.setText(selected_item)
                    self.label2_x.setText(str(x_val))
                    self.label2_y.setText(str(y_val))
                    self.label2_z.setText(str(z_val))
                elif selected_num == "3":
                    self.label3_label.setText(selected_item)
                    self.label3_x.setText(str(x_val))
                    self.label3_y.setText(str(y_val))
                    self.label3_z.setText(str(z_val))
                elif selected_num == "4":
                    self.label4_label.setText(selected_item)
                    self.label4_x.setText(str(x_val))
                    self.label4_y.setText(str(y_val))
                    self.label4_z.setText(str(z_val))

                # home_list.txt 기존 파일 내용 읽어오기
                existing_lines = []
                if os.path.exists(file_path):
                    with open(file_path, 'r') as file:
                        existing_lines = file.readlines()

                # 파일이 없을 경우 초기값 생성
                while len(existing_lines) < 4:
                    # existing_lines.append(f'{len(existing_lines) + 1}\n')
                    existing_lines.append('0 0 0 0\n')


                # 선택된 번호에 해당하는 줄 덮어쓰기 또는 추가하기
                if selected_num == "1":
                    existing_lines[0] = f'{selected_item} {x_val} {y_val} {z_val}\n'
                elif selected_num == "2":
                    existing_lines[1] = f'{selected_item} {x_val} {y_val} {z_val}\n'
                elif selected_num == "3":
                    existing_lines[2] = f'{selected_item} {x_val} {y_val} {z_val}\n'
                elif selected_num == "4":
                    existing_lines[3] = f'{selected_item} {x_val} {y_val} {z_val}\n'

                # 파일에 덮어쓴 내용 저장
                with open(file_path, 'w') as file:
                    file.writelines(existing_lines)

                # 확인 메시지 표시
                QMessageBox.information(self, "Info", "Data updated in home_list.txt")
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
            print("D")

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


########### start.py를 실행하면 아래는 필요 없음 #####################

class GUI_Node(Node):
    def __init__(self):
        super().__init__('gui_node')
        self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)
        self.app = QApplication(sys.argv)
        self.gui = MyHome(self)
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
