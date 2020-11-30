# python v_3.8.5
# pyQt5 v_5.15.1

import numpy as np
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap, QImage
from matplotlib import pyplot as plt

#<ui출력>
form_class = uic.loadUiType("form_Photo.ui")[0]

#<경로>

#<class 생성>
class MyApp(QWidget, form_class):

    #<def __init__>
    def __init__(self):  #순차적으로 실행되기 때문에 순서가 변경되면 출력값도 달라진다.
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.show()

    #<def initUI>
    def initUI(self):
        #Open,Save,Cencel 버튼연결 및 경로설정.
        self.OpenFilebtn.clicked.connect(self.Open_clicked)
        self.SaveFilebtn.clicked.connect(self.Save_clicked)
        self.Exitbtn.clicked.connect((QCoreApplication.instance().quit))

        # Groupbox 버튼연결.
        self.Blurbtn.clicked.connect(self.EditImg)
        self.Sharbtn.clicked.connect(self.EditImg)
        self.Defaultbtn.clicked.connect(self.EditImg)
        self.Invertbtn.clicked.connect(self.EditImg)
        self.Graybtn.clicked.connect(self.EditImg)
        self.setWindowTitle('PhotoEditor')

    # <def Open 이벤트> 버튼활성화시.
    def Open_clicked(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open Image files', './', options=QFileDialog.DontUseNativeDialog)
        self.label.setText('파일위치 : '+ self.fname)
        print(self.fname)
        self.showDialog()
        self.loadImage()

    def Save_clicked(self):
        self.fname, _ = QFileDialog.getSaveFileName(self, 'Save Image files', './', options=QFileDialog.DontUseNativeDialog)
        self.label_2.setText('저장위치 : ' + self.fname)
        print(self.fname)
        cv2.imwrite(self.fname, self.qimg)
        self.showDialog()
        self.loadImage()

    # <def OpenImg> 이미지읽기.
    def loadImage(self):
        self.orgImg = cv2.imread(self.fname)

    #<def Origin_img> 이미지 불러오기.
    def showDialog(self):
        self.pixmap = QPixmap(self.fname)
        self.Origin_img.setPixmap(self.pixmap)

    # <def Origin_img> 라디오박스 이미지 효과.
    def EditImg(self):
        try:
            if self.Blurbtn.isChecked() == True:
                src1 = self.orgImg
                blur = cv2.blur(src1, (3, 3))
                self.qimg = cv2.cvtColor(blur,cv2.COLOR_BGR2RGB)
                print('1')

            if self.Sharbtn.isChecked() == True:
                sharpenImg = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                src2 = self.orgImg
                shar = cv2.filter2D(src2, -1, sharpenImg)
                self.qimg = cv2.cvtColor(shar, cv2.COLOR_BGR2RGB)
                print('2')

            if self.Defaultbtn.isChecked() == True:
                src3 = self.orgImg
                self.qimg = cv2.cvtColor(src3, cv2.COLOR_BGR2RGB)
                print('3')

            self.EditImgFirst()
        except:
            print('NO IMAGE -STEP-1')

    # <def Origin_img> 역상 이미지 효과.
    def EditImgFirst(self):
        try:
            if self.Invertbtn.isChecked() == True:
                src = self.qimg
                self.qimg = cv2.bitwise_not(src)
                print('4')

            if self.Invertbtn.isChecked() == False:
                self.qimg = self.qimg

            self.EditImgSecond()
        except:
            print('NO IMAGE -STEP-2')

    # <def Origin_img> 그레이 이미지 효과.
    def EditImgSecond(self):
        try:
            if self.Graybtn.isChecked() == True:
                src = self.qimg
                gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) #그레이로 변환
                self.qimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB) # 그레이 싱클채널에서 3채널로 변환.
                self.result = QImage(self.qimg.data, self.qimg.shape[1], self.qimg.shape[0], QImage.Format_RGB888)
                print('6')

            if self.Graybtn.isChecked() == False:
                self.result = QImage(self.qimg.data, self.qimg.shape[1], self.qimg.shape[0], QImage.Format_RGB888)
                self.qimg = self.qimg
                print('7')

            self.pixmapsrc = QPixmap.fromImage(self.result)
            self.Preview_img.setPixmap(self.pixmapsrc)

        except:
            print('NO IMAGE')

#<if __name__>
if __name__ == '__main__':
    import sys
    app = QApplication([])
    ex = MyApp()
    sys.exit(app.exec_())
