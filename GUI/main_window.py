from tkinter import *

import cv2
from PIL import Image
from guizero import *
from guizero import App, Text

'''
pip3 install guizero
pip3 install guizero[images]
set READTHEDOCS=True
pip install picamera
'''
DATA_PATH = 'POSE_DETECTION/images'
EMOTIONS_LIST = ['positive_interaction', 'discomfort', 'insecure', 'anger', 'happines', 'excitement', 'confidence',
                 'confusion', 'reliability']


# Functions------------------------------------------------
def recommand(emo):
    pass


def calculate(emo_res, emo_list):
    button_list = {}
    emo_box = Box(app, grid=[5, 0], align='right')

    for emo in emo_list:
        # im = Image.open('emotion_icons/'+emo + '.jpg')
        im = Image.open('emotion_icons/angry' + '.jpg')
        im = im.resize((50, 50))
        box = Box(emo_box, align='top')
        PushButton(box, command=recommand(emo), align='right', image=im)
        txt = Text(box, align='right', text=emo, height=1, width=20)
        button_list[emo] = box
        if emo in emo_res:
            button_list[emo].bg = 'green'
        else:
            button_list[emo].bg = 'yellow'
    # return button_list


# Function for opening the file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/Pictures",
                                          title="Select a File",
                                          filetypes=(("IMAGE_FILES",
                                                      "*.jpg*"),
                                                     ("all files",
                                                      "*.*")))

    return filename


def upload_img():
    filename = browseFiles()
    # open method used to open different extension image file
    im = Image.open(filename)
    im = im.resize((400, 400))
    im.save("upload_images/upload_img1.jpg")
    viewer.image = r'upload_images/upload_img1.jpg'


def capture_img():
    cam = cv2.VideoCapture(0)
    frame = cam.read()[1]
    cv2.imwrite(r'compute_images/img.jpg', frame)
    im = Image.open(r'compute_images/img.jpg')
    im = im.resize((500, 20))
    im.save(r'compute_images/img.jpg')
    viewer.image = r'compute_images/img.jpg'


# APP-----------------------------------------------------
NAME = 'AI_PROJECT'
MESSAGE = 'please insert image'
app = App(title=NAME, layout='grid', height=650, width=650)

# Widgets---------------------------------------------------
# message = Text(app, text=MESSAGE)
# message.text_size = 40
b = Box(app, grid=[0, 1, 3, 1])
app.bg = 'lightblue'
up = PushButton(b, command=upload_img, text='Upload', align='left')
up.bg = 'red'
take = PushButton(b, command=capture_img, text='Take a picture', align='left')
take.bg = 'red'
rep = PushButton(b, command=calculate(['anger'], EMOTIONS_LIST), text='Report', align='left')
rep.bg = 'red'
viewer = Picture(app, image='mad.jpg', grid=[1, 0])
# name_img = TextBox(app, grid=[0, 1])
# text = Text(app, text="recommand",grid=[0,30])


# Display---------------------------------------------------
app.display()
