import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
# 더 추가할 필요가 있다면 추가하시면 됩니다. 예: (from PyQt5.QtGui import QIcon)

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))    
    print(base_path)
    return os.path.join(base_path, relative_path)

form = resource_path('main.ui')
form_class = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)

        # 여기에 시그널, 설정 
    #여기에 함수 설정

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )
