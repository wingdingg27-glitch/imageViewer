import sys
import os

from calculations import Calculations
from viewer import Ui_MainWindow
from PyQt6.QtWidgets import QApplication,QMainWindow,QFileDialog,QMessageBox,QRubberBand,QPushButton
from PyQt6.QtGui import QPixmap,QPalette
from PyQt6.QtCore import Qt,QRect,QPoint

class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.appCalculations=Calculations()
        self.setupUi(self)
        self.setWindowTitle("Image Viewer")
        self.saveButton=QPushButton("Сохранить",self.label)
        self.saveButton.hide()
        self.saveButton.clicked.connect(self.saveImage)
        self.cropButton=QPushButton("Обрезать",self.label)
        self.cropButton.hide()
        self.cropButton.clicked.connect(self.cropImage)
        self.pushButton.clicked.connect(self.next)
        self.pushButton_2.clicked.connect(self.prev)
        self.actionopen_folder.triggered.connect(self.openFolder)
        self.actionopen_image()
        #для выделения области
        self.label.setMouseTracking(True)
        self.label.installEventFilter(self)
        self.startPos=None
        self.startPosSave=None
        self.finPos=None
        self.rubberBand=None
        self.rectSelection=None
        #для работы с масштабом
        self.originalImage=None
        self.currentImage=None #отмасштабированная картинка
        self.offsetImage=None
        self.scaleFactor=None
        #red=f"background-color:rgb({255},{0},{0});"
        #green=f"background-color:rgb({0},{255},{0});"
        #blue=f"background-color:rgb({0},{0},{255});"
        #self.colors=[red,green,blue]
        #self.length=len(self.colors)

    def eventFilter(self,obj,event):
        if obj==self.label:
            if event.type()==event.Type.MouseButtonPress and event.button()==Qt.MouseButton.LeftButton:
                if not self.appCalculations.isEmpty():
                    self.startPos=event.position().toPoint()
                    self.startPosSave=self.startPos
                    print(self.rubberBand)
                    if not self.rubberBand:
                        self.rubberBand=QRubberBand(QRubberBand.Shape.Rectangle,self.label)
                        palette=QPalette()
                        palette.setColor(QPalette.ColorRole.Highlight,Qt.GlobalColor.green)
                        self.rubberBand.setPalette(palette)
                    else:
                        self.rubberBand.hide()
                    self.rubberBand.setGeometry(self.startPos.x(),self.startPos.y(),0,0)
                    self.rubberBand.show()
                return True
            elif event.type()==event.Type.MouseMove:
                if self.rubberBand and self.startPos:
                    rect=QRect(self.startPos,event.position().toPoint()).normalized()
                    self.rubberBand.setGeometry(rect)
                return True
            elif event.type()==event.Type.MouseButtonRelease and event.button()==Qt.MouseButton.LeftButton:
                if not self.appCalculations.isEmpty():
                    self.finPos=event.position().toPoint()
                    if self.rubberBand:
                        rect=self.rubberBand.geometry()
                        if rect.width()>5 and rect.height()>5:
                            origRect = self.calculateOriginalSelectionArea(rect)
                            self.rectSelection=origRect
                            self.cropButton.show()
                            self.saveButton.hide()
                            x,y,w,h=origRect.x(),origRect.y(),origRect.width(),origRect.height()
                            print(f"height={h},width={w}")
                        else:
                            print("Выделение слишком маленькое!")
                            self.rubberBand.hide()
                            self.rubberBand=None
                            self.cropButton.hide()

                        self.startPos=0
                return True
        return super().eventFilter(obj,event)

    def actionopen_image(self):
        #открытие картинки через приложение
        if len(sys.argv)==2:
            imagePath=sys.argv[1]
            if os.path.isfile(imagePath):
                self.openImage(imagePath)
        else:
            self.showPlaceholder()

    def next(self):
        #(0+1)%3
        self.appCalculations.next()
        #self.label.setText(self.images[self.i])
        if self.rubberBand:
            self.rubberBand.hide()
        self.cropButton.hide()
        self.saveButton.hide()
        self.originalImage=None
        self.showImage()

    def prev(self):
        self.appCalculations.prev()
        #self.label.setText(self.images[self.i])
        if self.rubberBand:
            self.rubberBand.hide()
        self.cropButton.hide()
        self.saveButton.hide()
        self.originalImage=None
        self.showImage()

    # def searchImage(self, folder):
    #     """Поиск всех изображений в папке"""
    #     for i in os.listdir(folder):
    #         ext = os.path.splitext(i)[1].lower()
    #         if ext in include_ext:
    #             path_image = os.path.join(folder, i)
    #             self.images.append(path_image)
    #     if not self.images:
    #         QMessageBox.information(self, "Ошибка!", "Загрузка не удалась!")
    #         return

    def saveImage(self):
        self.saveButton.hide()
        fullName=os.path.basename(self.appCalculations.currentImage())
        name=os.path.splitext(fullName)[0]
        ext=os.path.splitext(fullName)[1]
        newName=f"{name}_redacted{ext}"
        currentDir=os.path.dirname(self.appCalculations.currentImage())
        currentDirOs=os.path.expanduser(currentDir)
        path,_=QFileDialog.getSaveFileName(self,"Сохранение изображения",os.path.join(currentDirOs,newName),".png,.jpg")
        if path:
            self.originalImage.save(path)

    def openFolder(self):
        """Срабатывает если пользователь открывает папку"""
        folder=QFileDialog.getExistingDirectory(self, "Выбор папки", os.path.expanduser("~"))
        self.appCalculations.searchImage(folder, "folder")
        if self.appCalculations.isEmpty():
            QMessageBox.information(self, "Ошибка!", "В папке нет изображений!")
            self.showPlaceholder()
        self.showImage()

    def openImage(self,path):
        """Загружает изображение если картинка открыта приложением"""
        self.appCalculations.searchImage(path,"image")
        print(path)
        self.showImage()

    def showImage(self):
        if self.appCalculations.isEmpty():
            return
        path=self.appCalculations.currentImage()
        if not self.originalImage:
            self.originalImage=QPixmap(path)
        scaledImage=self.originalImage.scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(scaledImage)
        self.currentImage=scaledImage
        labelSize=self.label.size()
        currentImageSize=self.currentImage.size()
        offsetX=(labelSize.width()-currentImageSize.width())//2
        offsetY=(labelSize.height()-currentImageSize.height())//2
        self.offsetImage=QPoint(offsetX,offsetY)
        origW=self.originalImage.width()
        origH=self.originalImage.height()
        curW=self.currentImage.width()
        curH=self.currentImage.height()
        self.koefW=origW/curW
        self.koefH=origH/curH
        self.cropButton.setGeometry(self.offsetImage.x(),self.offsetImage.y(),80,20)
        self.saveButton.setGeometry(self.offsetImage.x(),self.offsetImage.y(),80,20)
        self.rubberBandDisplayUpdate()

    def calculateOriginalSelectionArea(self,rect):
        """Вычисление оригинальной области выделения"""
        #координаты выделенной области
        x1=rect.x()
        y1=rect.y()
        x2=x1+rect.width()
        y2=y1+rect.height()
        #Считаем смещение
        x1offset=x1-self.offsetImage.x()
        y1offset=y1-self.offsetImage.y()
        x2offset=x2-self.offsetImage.x()
        y2offset=y2-self.offsetImage.y()
        #Ограничиваем смещение чтоб не выйти за границы оригинала
        curW = self.currentImage.width()
        curH = self.currentImage.height()
        x1offset=max(0,x1offset)
        y1offset=max(0,y1offset)
        x2offset=max(0,x2offset)
        y2offset=max(0,y2offset)
        origX1=x1offset*self.koefW
        origY1=y1offset*self.koefH
        origX2=x2offset*self.koefW
        origY2=y2offset*self.koefH
        origRect=QRect(int(origX1),int(origY1),int(origX2-origX1),int(origY2-origY1))
        return origRect

    def calculateSelectionToOriginalArea(self,origRect):
        x1orig=origRect.x()
        y1orig=origRect.y()
        x2orig=x1orig+origRect.width()
        y2orig=y1orig+origRect.height()
        if self.koefW==0 or self.koefH==0:
            return
        x1display=int(x1orig/self.koefW)
        y1display=int(y1orig/self.koefH)
        x2display=int(x2orig/self.koefW)
        y2display=int(y2orig/self.koefH)
        x1display=x1display+self.offsetImage.x()
        y1display=y1display+self.offsetImage.y()
        x2display=x2display+self.offsetImage.x()
        y2display=y2display+self.offsetImage.y()
        origRect=QRect(x1display,y1display,(x2display-x1display),(y2display-y1display))
        return origRect

    def rubberBandDisplayUpdate(self):
        if not self.rubberBand or not self.rectSelection or not self.offsetImage:
            return
        newRect=self.calculateSelectionToOriginalArea(self.rectSelection)
        self.rubberBand.setGeometry(newRect)

    def showPlaceholder(self):
        self.label.clear()
        self.label.setText("Выберите папку!")

    def resizeEvent(self,event):
        super().resizeEvent(event)
        self.showImage()

    def cropImage(self):
        if self.rectSelection:
            origRect=self.rectSelection #self.calculateOriginalSelectionArea(self.rectSelection)
            croppedImage=self.originalImage.copy(origRect)
            self.originalImage=croppedImage
            self.showImage()
            self.rubberBand.hide()
            self.rubberBand=None
            self.cropButton.hide()
            self.saveButton.show()

    def name(self):
        path=self.appCalculations.currentImage()
        self.setWindowTitle(path)

if __name__ == "__main__":
    QApp=QApplication(sys.argv)
    app=App()
    app.show()
    sys.exit(QApp.exec())