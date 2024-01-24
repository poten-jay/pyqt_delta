import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextBrowser, QPushButton
import openpyxl

class ExcelPopup(QDialog):
    def __init__(self, excel_file):
        super().__init__()

        self.excel_file = excel_file
        self.setup_ui()
        self.load_excel_data()

    def setup_ui(self):
        self.setWindowTitle("Excel Popup")
        self.setGeometry(100, 100, 400, 200)

        self.text_browser = QTextBrowser(self)
        self.load_button = QPushButton("Load Excel", self)
        self.load_button.clicked.connect(self.load_excel_data)

        layout = QVBoxLayout()
        layout.addWidget(self.text_browser)
        layout.addWidget(self.load_button)

        self.setLayout(layout)

    def load_excel_data(self):
        try:
            wb = openpyxl.load_workbook(self.excel_file)
            sheet = wb["angles"]
            values = [str(cell.value) for cell in sheet[1]]
            self.text_browser.setPlainText("\t".join(values))
        except Exception as e:
            self.text_browser.setPlainText("Error: " + str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    excel_file = "cal.xlsx"  # 엑셀 파일 경로를 지정하세요
    window = ExcelPopup(excel_file)
    window.show()
    sys.exit(app.exec_())
