import cv2
import duration as duration
from guizero import *
from tkinter import *
from tkinter import filedialog
from PIL import Image
import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *

from matplotlib.pyplot import grid

'''pip3 install guizero
 pip3 install guizero[images]
 set READTHEDOCS=True
 pip install picamera
 '''


# Functions------------------------------------------------
def calculate():
    pass
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
app = App(title=NAME, layout='grid')

# Widgets---------------------------------------------------
#message = Text(app, text=MESSAGE)
#message.text_size = 40
app.bg = 'pink'
up = PushButton(app, upload_img, text='Upload', grid=[0, 0, 40, 2])
up.bg = 'red'
take = PushButton(app, capture_img, text='Take a picture', grid=[40, 0, 30, 2])
take.bg = 'red'
rep = PushButton(app, calculate, text='Report', grid=[70, 0, 40, 2])
rep.bg = 'red'
pic = Drawing(app, grid=[1, 4, 70, 70])
viewer = Picture(app, grid=[1, 4, 70, 70])
#duration=Slider(app,start=0,end=100,grid=[50,50])
#duration.bg = 'green'
# Display---------------------------------------------------
app.display()
