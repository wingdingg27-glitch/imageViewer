import sys
import os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calculations import Calculations
from calculations import include_ext
import pytest

@pytest.fixture
def createImages(tmp_path):
    f = tmp_path / "images"
    f.mkdir()
    (f / "image1.jpg").write_text("abcd")
    (f / "image4.exe").write_text("jkl;")
    (f / "image3.webp").write_text("ghjkl")
    (f / "image2.png").write_text("apple")
    calc=Calculations()
    calc.searchImage(f,"folder")
    return calc,f

def test_loadFromFolder(createImages):
    calc,f=createImages
    assert calc.count()==3
    assert calc.currentIndex()==0
    assert calc.getImages()==[
        str(f/"image1.jpg"),
        str(f/"image2.png"),
        str(f/"image3.webp"),
    ]

def test_openImage(createImages):
    calc,_=createImages
    #print(f/"image2.png")
    assert calc.currentIndex()==0
    assert calc.count()==3
    #assert calc.currentImage().endswith("image2.PNG")

def test_prevNextImage():
    calc=Calculations()
    calc.images=["image1.jpg","image2.png","image3.gif"]
    calc.i=0
    calc.next()
    assert calc.currentIndex()==1
    calc.next()
    assert calc.currentIndex()==2
    calc.next()
    assert calc.currentIndex()==0
    calc.prev()
    assert calc.currentIndex()==2
    calc.prev()
    assert calc.currentIndex()==1
    calc.prev()
    assert calc.currentIndex()==0

def test_isEmpty():
    calc=Calculations()
    assert calc.isEmpty()==True
    assert calc.i==0
    calc.next()
    calc.prev()