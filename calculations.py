import os
include_ext=('.jpg','.jpeg','.png','.gif','.webp','.bmp')

class Calculations:
    def __init__(self):
        self.i=0
        self.images=[]

    def searchImage(self,folder,type):
        """Поиск всех изображений в папке"""
        self.images=[]
        image=None
        if type=="folder":
            self.i=0
        elif type=="image":
            #folder-images/image1.png
            image=folder
            folder = os.path.dirname(image)
            #folder-images
            #images-images/image1.png
            #print(self.images[0])

        for i in os.listdir(folder):
            ext=os.path.splitext(i)[1].lower()
            if ext in include_ext:
                path_image = os.path.join(folder, i)
                self.images.append(path_image)
        if type=="image":
            try:
                self.i=self.images.index(image)
            except:
                print("Картинки не существует!")
        self.images.sort()
        print(f"картинка {self.images[0]}")


    def next(self):
        if not self.isEmpty():
            self.i = (self.i+1) % len(self.images)

    def prev(self):
        if not self.isEmpty():
            self.i = (self.i - 1) % len(self.images)

    def isEmpty(self):
        return len(self.images)==0

    def currentImage(self):
        return self.images[self.i]

    def currentIndex(self):
        return self.i

    def count(self):
        return len(self.images)

    def getImages(self):
        return self.images