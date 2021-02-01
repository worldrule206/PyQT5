# 1. **Pyqt5를 이용한 사진편집기 제작(PHOTOWORKS)**
- 1.1. [실행환경](#11-실행환경)  
- 1.2. [구성요소](#12-구성요소)  

&nbsp;
##  1.1. 실행환경
---
- Linux
- Ubuntu 18.04  
- Python v_3.8.5      
- PyQt5 v_5.15.1

&nbsp;
## 1.2. 구성요소
---
+ 1.2.1.  [Resize 크기조절](#121-resize)
+ 1.2.2.  [Blur 흐리게](#122-blur)
+ 1.2.3.  [Sharpen 강조](#123-sharpen)
+ 1.2.4.  [GrayScale 회색조](#124-grayscale)
+ 1.2.5.  [Invert 역상](#125-invert)
+ 1.2.6.  [Rotate 회전](#126-rotate)
+ 1.2.7.  [Screenshot 화면저장 및 잘라내기](#127-screenshot)  
+ 1.2.8.  [저장 및 불러오기](#128-open--save)

&nbsp;   
### 1.2.1 Resize
```python
    height, width, channel = self.orgImg.shape # 이미지 높이,넓이 채널로 분리
    self.Wid_edit.setText(str(height)) #높이깂 표시
    self.Hei_edit.setText(str(width))  #넓이값 표시

 def EditSize(self):
       
    self.w = int(self.Wid_edit.displayText()) #높이 입력값 저장
    self.h = int(self.Hei_edit.displayText()) #넓이 입력값 저장

    if self.Resizebtn.isChecked() == True:     
        self.qimg = cv2.resize(self.qimg, dsize=(self.w, self.h), interpolation=cv2.INTER_AREA)
        # 입력된 높이값과 넓이값을 읽어와 변환 및 self.qimg 반환.

```

![Pyqt5_Main_Img](./Readme_img/pqyqt5_main.png)


&nbsp;
### 1.2.2 Blur 
```python
    def EditImg(self):
    
        self.qimg = self.orgImg.copy()  #원본이미지 데이터보호를 위해 복사 후 복사본으로 작업.

        if self.Blurbtn.isChecked() == True:    # 블러버튼 활성 시 이미지블러
            i = self.BlurSlider.value()         # 슬라이더를 이용하여 i값 변경.
            blur = cv2.blur(self.qimg, (i, i))  # 이미지를 i만큼 블러처리
            self.qimg = blur                    # 이후 편집기능 활성 시 블러처리 된 이미지를 반환.
```
![Pyqt5_Blur_Img](./Readme_img/pqyqt5_Blur.png)

&nbsp;
### 1.2.3 Sharpen
```python
    if self.Sharbtn.isChecked() == True:
        j = self.SharSlider.value()                                      # 슬라이더 값을 j값으로 입력
        sharpenImg = np.array([[-1, -1, -1], [-1, j, -1], [-1, -1, -1]]) # j값 만큼 변경 필터생성.
        shar = cv2.filter2D(self.qimg, -1, sharpenImg)                   # 이미지 넘피배열만큼 필터처리
        self.qimg = shar                                                 # 가공된 이미지 다음편집단계를 위해 저장.                                 
```
![Pyqt5_Sharpen_Img](./Readme_img/pqyqt5_Sharpen.png)

&nbsp;
### 1.2.4 GrayScale
```python
def EditImgSecond(self):
       
    if self.Graybtn.isChecked() == True:
        src = self.qimg
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) #3채널에서 단채널로 변환된다.
        dst = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB) #Qt에서 이미지포멧을 위해 3채널로 다시 변환.
        #입력된이미지(3채널) -> 그레이스케일변환(1채널) -> Qt포멧을위한변환(3채널)
        self.qimg = dst
```
![Pyqt5_GrayScale_Img](./Readme_img/pqyqt5_GrayScale.png)

&nbsp;
### 1.2.5 Invert
```python
def EditImgFirst(self):

    if self.Invertbtn.isChecked() == True:
        src = self.qimg
        self.qimg = cv2.bitwise_not(src) #입력된 이미지 역상처리 후 self.qimg 반환
        
```
![Pyqt5_Invert_Img](./Readme_img/pqyqt5_Invert.png)

&nbsp;
### 1.2.6 Rotate
```python
  def EditRotate(self):
    
    if self.Rotatebtn.isChecked() == True:
        r = self.Rotatedial.value()                                     #볼륨값
        matrix = cv2.getRotationMatrix2D((self.w/2, self.h/2), r, 1)    #중간값, 볼륨값, 1채널 의 매트릭스 생성
        self.qimg = cv2.warpAffine(self.qimg, matrix, (self.w, self.h)) #생성된 매트릭스를 적용, 이미지 위치변경.
```
![Pyqt5_Rotate_Img](./Readme_img/pqyqt5_Rotate.png)


&nbsp;
### 1.2.7 Screenshot
```python
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
```
![Pyqt5_Screenshot_Img](./Readme_img/pqyqt5_Screenshot.png)

&nbsp;
### 1.2.8 Open & Save
```python

def Open_clicked(self):
    try:
        a = QFileDialog.getOpenFileName; b = QFileDialog.DontUseNativeDialog
        #DontUseNativeDialog 사용자경로를 위해 네이티브다이얼로그 해제.
        #DontUseNativeDialog 가 있고 없고 차이를 보면 알 수 있다.
        self.fname, _ = a(self, 'Open Image files', './', options=b)
        self.label.setText('파일위치 : '+ self.fname)
        self.showDialog(); self.loadImage()
    except:
        return 0
def Save_clicked(self):
    try:
        a = QFileDialog.getSaveFileName; b = QFileDialog.DontUseNativeDialog
        self.fname, _ = a(self, 'Save Image files', './', options=b)
        self.label_2.setText('저장위치 : ' + self.fname)
        cv2.imwrite(self.fname, self.qimg)
    except:
        return 0
```
![Pyqt5_OS_Img](./Readme_img/pqyqt5_OS.png)

