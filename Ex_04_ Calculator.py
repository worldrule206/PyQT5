import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton, QToolButton, QSizePolicy

from PyQt5.QtCore import Qt


print()

class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setStyleSheet('color : black; background : #808080')
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height()+ 50)
        size.setWidth(max(size.width(), size.height()))
        return size


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # 결과모니터 생성
        self.display = QLineEdit('0')   # 초기값 0
        self.display.setReadOnly(True)  # 읽기전용
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        font = self.display.font()
        font.setPointSize(font.pointSize() + 12)
        self.display.setFont(font)

        # 출력 모니터
        self.grid.addWidget(self.display, 0, 0, 1, 4)
        # 입력버튼 생성
        self.divisionButton = self.createButton(u"AC")
        self.grid.addWidget(self.divisionButton, 1, 0)
        self.divisionButton = self.createButton(u"+/-")
        self.grid.addWidget(self.divisionButton, 1, 1)
        self.divisionButton = self.createButton(u"%")
        self.grid.addWidget(self.divisionButton, 1, 2)

        self.divisionButton = self.createButton(u"÷")
        self.grid.addWidget(self.divisionButton, 1, 3)
        self.divisionButton.setStyleSheet('color : white; background : #A0522D')

        self.divisionButton = self.createButton(u"7")
        self.grid.addWidget(self.divisionButton, 2, 0)
        self.divisionButton = self.createButton(u"8")
        self.grid.addWidget(self.divisionButton, 2, 1)
        self.divisionButton = self.createButton(u"9")
        self.grid.addWidget(self.divisionButton, 2, 2)

        self.divisionButton = self.createButton(u"×")
        self.grid.addWidget(self.divisionButton, 2, 3)
        self.divisionButton.setStyleSheet('color : white; background : #A0522D')

        self.divisionButton = self.createButton(u"6")
        self.grid.addWidget(self.divisionButton, 3, 0)
        self.divisionButton = self.createButton(u"5")
        self.grid.addWidget(self.divisionButton, 3, 1)
        self.divisionButton = self.createButton(u"4")
        self.grid.addWidget(self.divisionButton, 3, 2)

        self.divisionButton = self.createButton(u"－")
        self.grid.addWidget(self.divisionButton, 3, 3)
        self.divisionButton.setStyleSheet('color : white; background : #A0522D')

        self.divisionButton = self.createButton(u"3")
        self.grid.addWidget(self.divisionButton, 4, 0)
        self.divisionButton = self.createButton(u"2")
        self.grid.addWidget(self.divisionButton, 4, 1)
        self.divisionButton = self.createButton(u"1")
        self.grid.addWidget(self.divisionButton, 4, 2)

        self.divisionButton = self.createButton(u"＋")
        self.grid.addWidget(self.divisionButton, 4, 3)
        self.divisionButton.setStyleSheet('color : white; background : #A0522D')

        self.divisionButton = self.createButton(u"0")
        self.grid.addWidget(self.divisionButton, 5, 0, 1, 2)
        self.divisionButton = self.createButton(u".")
        self.grid.addWidget(self.divisionButton, 5, 2)

        self.divisionButton = self.createButton(u"=")
        self.grid.addWidget(self.divisionButton, 5, 3)
        self.divisionButton.setStyleSheet('color : white; background : #A0522D')


        #self.grid.addWidget(self.timesButton, 3, 4)
        #self.grid.addWidget(self.plusButton, 5, 4)

        self.setWindowTitle('계 산 기')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def createButton(self, text):
        button = Button(text)
        return button


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())