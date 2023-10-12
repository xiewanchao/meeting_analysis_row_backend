import sys
import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QVBoxLayout, QWidget, QPushButton, QFileDialog, \
    QComboBox, QHBoxLayout, QShortcut


class JSONViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.opened_file_path = None  # 存储打开的文件路径
        self.json_data = None
        self.current_element_index = 0
        self.modle = True
        self.labels = {}  # 存储每个元素的 "label" 属性

    def initUI(self):
        # 获取屏幕的宽度和高度
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        window_width = 1000
        window_height = 1000
        window_x = (screen_geometry.width() - window_width) // 2
        window_y = (screen_geometry.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowTitle('JSON Viewer')

        # 创建文本浏览器用于显示JSON内容
        self.json_browser = QTextBrowser(self)

        # 创建"Next"和"Last"按钮
        next_button = QPushButton('Next', self)
        next_button.clicked.connect(self.showNextElement)
        last_button = QPushButton('Last', self)
        last_button.clicked.connect(self.showLastElement)


        """     
        # 创建"Label"下拉框
        label_combo = QComboBox(self)
        label_combo.addItems(['1', '2', '3', '4'])
        label_combo.currentIndexChanged.connect(self.setLabel)
        """
        # 创建四个"Label"按钮
        label1_button = QPushButton('Label 1', self)
        label2_button = QPushButton('Label 2', self)
        label3_button = QPushButton('Label 3', self)
        label4_button = QPushButton('Label 4', self)
        label1_button.clicked.connect(lambda: self.setLabel('1'))
        label2_button.clicked.connect(lambda: self.setLabel('2'))
        label3_button.clicked.connect(lambda: self.setLabel('3'))
        label4_button.clicked.connect(lambda: self.setLabel('4'))

        # 创建打开文件按钮
        open_button = QPushButton('Open JSON File', self)
        open_button.clicked.connect(self.openJSONFile)

        # 创建保存按钮
        save_button = QPushButton('Save Labels', self)
        save_button.clicked.connect(self.saveLabels)

        # 创建布局
        button_layout = QHBoxLayout()  # 创建一个水平布局
        button_layout.addWidget(label1_button)
        button_layout.addWidget(label2_button)
        button_layout.addWidget(label3_button)
        button_layout.addWidget(label4_button)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(open_button)
        layout.addWidget(self.json_browser)
        layout.addLayout(button_layout)  # 将水平布局添加到垂直布局
        layout.addWidget(next_button)
        layout.addWidget(last_button)
        layout.addWidget(save_button)

        # next快捷键：⬇
        button_shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        button_shortcut.activated.connect(next_button.click)

        # last快捷键：⬆
        button_shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        button_shortcut.activated.connect(last_button.click)

        # lable1：1
        button_shortcut = QShortcut(QKeySequence(Qt.Key_1), self)
        button_shortcut.activated.connect(label1_button.click)
        # lable2：2
        button_shortcut = QShortcut(QKeySequence(Qt.Key_2), self)
        button_shortcut.activated.connect(label2_button.click)
        # lable3：3
        button_shortcut = QShortcut(QKeySequence(Qt.Key_3), self)
        button_shortcut.activated.connect(label3_button.click)
        # lable4：4
        button_shortcut = QShortcut(QKeySequence(Qt.Key_4), self)
        button_shortcut.activated.connect(label4_button.click)


        # 创建主窗口中的中心小部件
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def openJSONFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, 'Open JSON File', '', 'JSON Files (*.json);;All Files (*)',
                                                   options=options)

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.json_data = json.load(file)
                    self.current_element_index = 0
                    self.opened_file_path = file_path
                    self.showCurrentElement()
            except Exception as e:
                self.json_browser.setPlainText(f"Error: {str(e)}")

    def setLabel(self, index):
        if self.json_data is not None and 0 <= self.current_element_index < len(self.json_data):
            self.labels[self.current_element_index] = index
            self.saveLabels()

    def showCurrentElement(self):
        if self.json_data is not None and 0 <= self.current_element_index < len(self.json_data):
            element = self.json_data[self.current_element_index]
            formatted_json = json.dumps(element, indent=4)
            self.json_browser.setPlainText(formatted_json)

    def showNextElement(self):
        if self.json_data is not None:
            self.current_element_index += 1
            if self.current_element_index >= len(self.json_data):
                self.current_element_index = len(self.json_data) - 1
            self.showCurrentElement()

    def showLastElement(self):
        if self.json_data is not None:
            self.current_element_index -= 1
            if self.current_element_index < 0:
                self.current_element_index = 0
            self.showCurrentElement()

    def saveLabels(self):
        if self.opened_file_path and self.json_data:
            try:
                for index, element in enumerate(self.json_data):
                    if index in self.labels:
                        element['label'] = self.labels[index]
                self.showCurrentElement()
                with open(self.opened_file_path, 'w') as file:
                    json.dump(self.json_data, file, indent=4)
            except Exception as e:
                self.json_browser.setPlainText(f"Error: {str(e)}")


def main():
    app = QApplication(sys.argv)
    viewer = JSONViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
