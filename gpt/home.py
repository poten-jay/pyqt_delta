import sys
import os
import rclpy
from rclpy.node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QSize, Qt, pyqtSignal
from geometry_msgs.msg import Point

from main import MyApp

# function.py 에서 class 호출
from function import xyz_button

# setting.py 에서 값 호출
import setting

# 현재 좌표 값 받아오기
x = setting.x
y = setting.y
z = setting.z

class MyHome(QWidget):
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
        original_pixmap = QPixmap("/workspace/pyqt_delta/img/home.png")
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

        # lebel 정보 창
        self.label1_label = QLabel(f"{x}", self)
        self.label1_label.setStyleSheet("Color : white")
        self.label1_label.setAlignment(Qt.AlignRight)
        self.label1_label.setGeometry(313, 116, 100, 30)  # Adjust position and size as needed
        self.label1_x = QLabel(f"{y}", self)
        self.label1_x.setStyleSheet("Color : white")
        self.label1_x.setAlignment(Qt.AlignRight)
        self.label1_x.setGeometry(412, 116, 100, 30)  # Adjust position and size as needed
        self.label1_y = QLabel(f"{z}", self)
        self.label1_y.setStyleSheet("Color : white")
        self.label1_y.setAlignment(Qt.AlignRight)
        self.label1_y.setGeometry(531, 116, 100, 30)  # Adjust position and size as needed
        self.label1_z = QLabel(f"{z}", self)
        self.label1_z.setStyleSheet("Color : white")
        self.label1_z.setAlignment(Qt.AlignRight)
        self.label1_z.setGeometry(649, 116, 100, 30)  # Adjust position and size as needed

        self.label2_label = QLabel(f"{x}", self)
        self.label2_label.setStyleSheet("Color : white")
        self.label2_label.setAlignment(Qt.AlignRight)
        self.label2_label.setGeometry(313, 153, 100, 30)  # Adjust position and size as needed
        self.label2_x = QLabel(f"{y}", self)
        self.label2_x.setStyleSheet("Color : white")
        self.label2_x.setAlignment(Qt.AlignRight)
        self.label2_x.setGeometry(412, 153, 100, 30)  # Adjust position and size as needed
        self.label2_y = QLabel(f"{z}", self)
        self.label2_y.setStyleSheet("Color : white")
        self.label2_y.setAlignment(Qt.AlignRight)
        self.label2_y.setGeometry(531, 153, 100, 30)  # Adjust position and size as needed
        self.label2_z = QLabel(f"{z}", self)
        self.label2_z.setStyleSheet("Color : white")
        self.label2_z.setAlignment(Qt.AlignRight)
        self.label2_z.setGeometry(649, 153, 100, 30)  # Adjust position and size as needed

        self.label3_label = QLabel(f"{x}", self)
        self.label3_label.setStyleSheet("Color : white")
        self.label3_label.setAlignment(Qt.AlignRight)
        self.label3_label.setGeometry(313, 189, 100, 30)  # Adjust position and size as needed
        self.label3_x = QLabel(f"{y}", self)
        self.label3_x.setStyleSheet("Color : white")
        self.label3_x.setAlignment(Qt.AlignRight)
        self.label3_x.setGeometry(412, 189, 100, 30)  # Adjust position and size as needed
        self.label3_y = QLabel(f"{z}", self)
        self.label3_y.setStyleSheet("Color : white")
        self.label3_y.setAlignment(Qt.AlignRight)
        self.label3_y.setGeometry(531, 189, 100, 30)  # Adjust position and size as needed
        self.label3_z = QLabel(f"{z}", self)
        self.label3_z.setStyleSheet("Color : white")
        self.label3_z.setAlignment(Qt.AlignRight)
        self.label3_z.setGeometry(649, 189, 100, 30)  # Adjust position and size as needed

        self.label4_label = QLabel(f"{x}", self)
        self.label4_label.setStyleSheet("Color : white")
        self.label4_label.setAlignment(Qt.AlignRight)
        self.label4_label.setGeometry(313, 225, 100, 30)  # Adjust position and size as needed
        self.label4_x = QLabel(f"{y}", self)
        self.label4_x.setStyleSheet("Color : white")
        self.label4_x.setAlignment(Qt.AlignRight)
        self.label4_x.setGeometry(412, 225, 100, 30)  # Adjust position and size as needed
        self.label4_y = QLabel(f"{z}", self)
        self.label4_y.setStyleSheet("Color : white")
        self.label4_y.setAlignment(Qt.AlignRight)
        self.label4_y.setGeometry(531, 225, 100, 30)  # Adjust position and size as needed
        self.label4_z = QLabel(f"{z}", self)
        self.label4_z.setStyleSheet("Color : white")
        self.label4_z.setAlignment(Qt.AlignRight)
        self.label4_z.setGeometry(649, 225, 100, 30)  # Adjust position and size as needed



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

        # Listup Button
        self.btnListup = QPushButton('List', self)
        self.btnListup.setGeometry(715, 510, 50, 25)  # Adjust position and size as needed
        self.btnListup.clicked.connect(self.listupClicked)

        # 뒤로가기 버튼 (순서가 밀리면 안보일 수도 있음)
        self.button()

        # 1,2,3,4 를 보여주는 콤보박스
        self.comboBox1 = QComboBox(self)
        self.comboBox1.setGeometry(100, 450, 120, 25)  # Adjust position and size as needed
        items = ["1", "2", "3", "4"]
        self.comboBox1.addItems(items)

        # lable 종류 txt애서 읽어와 보여주기
        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(100, 510, 120, 25)  # Adjust position and size as needed

        # Read items from the file and add them to the ComboBox
        with open('/workspace/pyqt_delta/vision/labels.txt', 'r') as file:
            items = file.read().splitlines()
            self.comboBox.addItems(items)


        # # Create a QTextEdit widget
        # self.textEdit = QTextEdit(self)
        # self.textEdit.setGeometry(100, 300, 300, 100)  # Adjust position and size as needed


    # 리스트업 클릭시 보낼 정보
    def listupClicked(self):
        selected_num = self.comboBox1.currentText()
        selected_item = self.comboBox.currentText()
        x_val = self.btn.input_x
        y_val = self.btn.input_y
        z_val = self.btn.input_z

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

        # # Append the information to the QTextEdit widget
        # info_text = f'{selected_num}. {selected_item}, X: [{x_val}], Y: [{y_val}], Z: [{z_val}]'
        # self.textEdit.append(info_text)

        # 리스트업 버튼 클릭 후 txt 로 만들기
        file_path = "/workspace/pyqt_delta/document/home_list.txt"

        # Check if the text file exists, and create it if it doesn't
        if not os.path.exists(file_path):
            with open(file_path, 'w'):
                pass

        # Write the data to the text file
        with open(file_path, 'a') as file:
            # txt 파일에 저장 시킬 형식
            info_text2 = f'{selected_num} {selected_item} {x_val} {y_val} {z_val}'
            file.write(info_text2 + '\n')


        # Optionally, display a message to confirm the write operation
        QMessageBox.information(self, "Info", "Data saved to home_list.txt")


########## 이미지 삽입 #####################################
        # Create a QLabel to display the image
        self.imageLabel = QLabel(self)
        pixmap = QPixmap('/media/ssd/workspace/jay/pyqt_delta/img/kbs1.png')
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.resize(pixmap.width(), pixmap.height())

        # Position the label where you want the image to appear
        self.imageLabel.move(100, 100)  # Adjust the position as needed
##########################################################


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
        self.btnback.setGeometry(10, 100, 50, 50)
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
