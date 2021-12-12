import subprocess
import cv2
from guizero import *
from tkinter import *
from PIL import Image
# import filedialog module
from tkinter import filedialog
import pyautogui as pg
# from picamera import PiCamera
from PIL import Image
from matplotlib.pyplot import grid

'''pip3 install guizero
 pip3 install guizero[images]
 set READTHEDOCS=True
 pip install picamera
 '''


# Functions------------------------------------------------
# Function for opening the file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("IMAGE_FILES",
                                                      "*.png*"),
                                                     ("all files",
                                                      "*.*")))
    return filename


def upload_img():
    filename = browseFiles()
    # open method used to open different extension image file
    im = Image.open(filename)
    # This method will show image in any image viewer
    im.save("upload_images/upload_img1.jpg")
    viewer.image = r'upload_images/upload_img1.jpg'


def capture_img():
    cam = cv2.VideoCapture(0)
    frame = cam.read()[1]
    cv2.imwrite(r'compute_images/img.png', frame)
    viewer.image = r'compute_images/img.png'


# APP-----------------------------------------------------
NAME = 'AI_PROJECT'
MESSAGE = 'please insert image'
app = App(title=NAME,layout='grid')

# Widgets---------------------------------------------------
 #message = Text(app, text=MESSAGE,grid=[8,0])
 #message.text_size = 40
app.bg = 'pink'
# img=Picture(app,image='img1.png')
up = PushButton(app, upload_img, text='Upload',grid=[0,0,40,2])
up.bg = 'red'
take = PushButton(app, capture_img, text='Take a picture',grid=[40,0,30,2])
take.bg = 'red'
pic = Drawing(app, grid=[1,4,70,70])
viewer = Picture(app,grid=[1,4,70,70])
# Display---------------------------------------------------
app.display()
