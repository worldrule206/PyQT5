# python v_3.8.5
# pyQt5 v_5.15.1

import cv2
import os
import numpy as np
from PIL import ImageGrab
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import *
from matplotlib import pyplot as plt
import time


#<ui출력>
form_class = uic.loadUiType("mainwindow.ui")[0]

#<경로>

#<class 생성>
class MyApp(QMainWindow, form_class):
    #<def __init__>
    def __init__(self):  #순차적으로 실행되기 때문에 순서가 변경되면 출력도 달라진다.
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.show()

    #<def initUI>
    def initUI(self):

        # toolbar Activate.
        self.actionOpenFile.triggered.connect(self.Open_clicked)                # 파일열기
        self.actionSaveFile.triggered.connect(self.Save_clicked)                # 저장
        self.actionExit.triggered.connect((QCoreApplication.instance().quit))   # 종료
        self.actionCrop.triggered.connect(self.Crop_clicked)                    # 이미지 자르기
        self.actionReset.triggered.connect(self.loadImage)                      # 초기화
        self.actionCapture.triggered.connect(self.Capture_clicked)              # 화면캡쳐

        # Slider Activate.
        self.BlurSlider.valueChanged.connect(self.EditImg)
        self.SharSlider.valueChanged.connect(self.EditImg)
        self.Rotatedial.valueChanged.connect(self.EditImg)

        # Line Edit.
        self.Wid_edit.textChanged.connect(self.EditImg)
        self.Hei_edit.textChanged.connect(self.EditImg)

        # btn Activate.
        self.Resizebtn.clicked.connect(self.EditImg)
        self.Blurbtn.clicked.connect(self.EditImg)
        self.Sharbtn.clicked.connect(self.EditImg)
        self.Defaultbtn.clicked.connect(self.EditImg)
        self.Invertbtn.clicked.connect(self.EditImg)
        self.Graybtn.clicked.connect(self.EditImg)
        self.Rotatebtn.clicked.connect(self.EditImg)
        self.setWindowTitle('Photo Editor')

    def Open_clicked(self):
        try:
            a = QFileDialog.getOpenFileName; b = QFileDialog.DontUseNativeDialog
            self.fname, _ = a(self, 'Open Image files', './', options=b)
            self.label.setText('파일위치 : '+ self.fname)
            self.showDialog(); self.loadImage()
        except:
            return 0
    def Save_clicked(self):
        try:
            a = QFileDialog.getOpenFileName; b = QFileDialog.DontUseNativeDialog
            self.fname, _ = a(self, 'Save Image files', './', options=b)
            self.label_2.setText('저장위치 : ' + self.fname)
            cv2.imwrite(self.fname, self.qimg)
            self.showDialog(); self.loadImage()
        except:
            return 0
    # <def OpenImg> 이미지읽기.
    def loadImage(self):
        src = cv2.imread(self.fname)
        dst = src.copy()
        self.orgImg = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB) #채널변경.
        # self.orgImg : 이미지편집을 위한 변수, self.origin : 초기화이미지를 위한 변수.

        # 이미지정보 읽어오고 라벨에 표시.
        height, width, channel = self.orgImg.shape
        self.Wid_edit.setText(str(height))
        self.Hei_edit.setText(str(width))

        self.origin = self.orgImg.copy(); a = self.origin
        self.result = QImage(a.data, a.shape[1], a.shape[0], QImage.Format_RGB888)
        self.pixmapsrc = QPixmap.fromImage(self.result)
        self.Preview_img.setPixmap(self.pixmapsrc)
        # 처음 이미지를 불러왔을때 초기화면(라벨2)에 띄우기 위해 문장을 추가.

    # <def Origin_img> 이미지 불러오기.
    def showDialog(self):
        self.pixmap = QPixmap(self.fname)
        self.Origin_img.setPixmap(self.pixmap)

    # <def Origin_img> 라디오박스 이미지 효과.
    def EditImg(self):
        try:
            self.qimg = self.orgImg.copy()

            if self.Blurbtn.isChecked() == True:
                i = self.BlurSlider.value()
                blur = cv2.blur(self.qimg, (i, i))
                self.qimg = blur
                print('1')

            if self.Sharbtn.isChecked() == True:
                j = self.SharSlider.value()
                sharpenImg = np.array([[-1, -1, -1], [-1, j, -1], [-1, -1, -1]])
                shar = cv2.filter2D(self.qimg, -1, sharpenImg)
                self.qimg = shar
                print('2')

            if self.Defaultbtn.isChecked() == True:
                pass
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
                pass
                print('5')

            self.EditImgSecond()
        except:
            print('NO IMAGE -STEP-2')

    # <def Origin_img> 그레이 이미지 효과.
    def EditImgSecond(self):
        try:
            if self.Graybtn.isChecked() == True:
                src = self.qimg
                gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) #3채널에서 단채널로 변환된다.
                dst = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB) #이미지포멧을 위해 3채널로 변경.
                self.qimg = dst
                print('6')
            if self.Graybtn.isChecked() == False:
                pass
                print('7')

            self.EditSize()
        except:
            print('NO IMAGE -STEP-3')

    # <def History> 기록남기기 추후 기능 추가.
    # def History(self):

    # 이미지 리사이즈
    def EditSize(self):
        try:
            self.w = int(self.Wid_edit.displayText())
            self.h = int(self.Hei_edit.displayText())

            if self.Resizebtn.isChecked() == True:
                self.qimg = cv2.resize(self.qimg, dsize=(self.w, self.h), interpolation=cv2.INTER_AREA)
                print('8')
            else:
                pass
                print('9')

            self.EditRotate()
        except:
            print('NO IMAGE -STEP-4')

        # 이미지 리사이즈
    def EditRotate(self):
        try:
            if self.Rotatebtn.isChecked() == True:
                r = self.Rotatedial.value()
                matrix = cv2.getRotationMatrix2D((self.w/2, self.h/2), r, 1)
                self.qimg = cv2.warpAffine(self.qimg, matrix, (self.w, self.h))
                print('10')
            else:
                pass
                print('11')

            self.Result()
        except:
            print('NO IMAGE -STEP-5')

    def Result(self):
        a = self.qimg
        self.result = QImage(a.data, a.shape[1], a.shape[0], QImage.Format_RGB888)
        self.pixmapsrc = QPixmap.fromImage(self.result)
        self.Preview_img.setPixmap(self.pixmapsrc)

#================================================================================================스냅관련.
    # <def OpenImg> 이미지 Crop.
    def Crop_clicked(self):
        try:
            src = self.orgImg; dst = src.copy()
            roi = cv2.selectROI('Screen Crop', dst, False, False) #roi 설정.
            img = dst[roi[0]:roi[0] + roi[2], roi[1]:roi[1] + roi[3]] #roi (x좌표, y좌표, 넓이, 높이)
            self.orgImg = img
            self.EditImg()
            cv2.imshow('Image Crop', img); cv2.waitKey(); cv2.destroyAllWindows()
        except:
            return 0

    def Capture_clicked(self):
        try:
            path = './img' ; file = 'screenshot.jpg'; file1 = 'screencrop.jpg'
            screensave = os.path.join(path, file); cropsave = os.path.join(path, file1)

            if os.path.isfile(screensave):
                os.remove(screensave)
                imgCapture = ImageGrab.grab()
                imgCapture.save(screensave)  # 저장 위치
                time.sleep(1) # 이미지가 저장되는 시간을 고려해 대기.
                print("삭제 후 저장 완료")
            else:
                imgCapture = ImageGrab.grab()
                imgCapture.save(screensave)  # 저장 위치
                time.sleep(1) # 이미지가 저장되는 시간을 고려해 대기.
                print("새로운 이미지 파일 생성")

            src = cv2.imread(screensave); dst = src.copy()
            dst1 = cv2.resize(dst, dsize=(1000, 563), interpolation=cv2.INTER_AREA) #이미지 리사이즈.
            roi = cv2.selectROI('Screen shot', dst1, False, False)
            capimg = dst1[roi[0]:roi[0] + roi[2],roi[1]:roi[1] + roi[3]] # roi (x좌표, y좌표, 넓이, 높이)
            cv2.imshow('Image Crop', capimg); cv2.imwrite(cropsave, capimg); cv2.waitKey(); cv2.destroyAllWindows()
            print("사진 자르기 완료")
        except:
            return 0

if __name__ == '__main__':
    import sys
    app = QApplication([]) # GUI의 어플리케이션의 흐름을 관리.
    ex = MyApp() # 생성자의 self는 ex를 전달받게 된다.
    sys.exit(app.exec_()) # 이벤트가 활성되면 종료신호가 호출될 때까지 대기함.


