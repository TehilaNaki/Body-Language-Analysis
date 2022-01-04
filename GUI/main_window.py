from tkinter import *

import cv2
from PIL import Image
from guizero import *
from guizero import App, Text
from datetime import datetime


'''
pip3 install guizero
pip3 install guizero[images]
set READTHEDOCS=True
pip install picamera
'''
DATA_PATH = 'POSE_DETECTION/images'
'''EMOTIONS_LIST = ['positive_interaction', 'discomfort', 'insecure', 'anger', 'happines', 'excitement', 'confidence',
                 'confusion', 'reliability']'''
EMOTIONS_LIST = ['positive_interaction','anger', 'confidence','discomfort','reliability']

# Functions------------------------------------------------
def recommand(emo):
    pass


def calculate(emo_res, emo_list):
    button_list = {}
    emo_box = Box(app, grid=[5, 0], align='right')

    for emo in emo_list:
        im = Image.open('emotion_icons/'+emo + '.jpg')
        #im = Image.open('emotion_icons/appriciative' + '.jpg')
        im = im.resize((50, 50))
        box = Box(emo_box, align='top')
        PushButton(box, command=recommand(emo), align='right', image=im)
        Emo=emo[0].upper()+emo[1:]
        txt = Text(box, align='right', text=Emo, height=1, width=20)
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
def get_new_name():
    n_file =open('new_images/number','r+')
    number=n_file.read()
    n_file.seek(0)
    n_file.truncate()
    n_file.write(str(int(number)+1))
    n_file.close()
    curr_time = datetime.today().strftime("%d-%m-%Y--%H%M%S")
    return 'new_images/'+'img'+number+'_'+curr_time+'.jpg'


def save_view_img(img_path):
    im = Image.open(img_path)
    im = im.resize((400, 400))
    viewer.image = im

def upload_img():
    filename = browseFiles()
    # open method used to open different extension image file
    save_view_img(r'new_images/'+filename)


def capture_img():
    cam = cv2.VideoCapture(0)
    frame = cam.read()[1]
    filename=get_new_name()
    cv2.imwrite(filename, frame)
    save_view_img(filename)


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
viewer = Picture(app, image='emotion_icons/mad.jpg', grid=[1, 0])
# name_img = TextBox(app, grid=[0, 1])
# text = Text(app, text="recommand",grid=[0,30])


# Display---------------------------------------------------
app.display()
