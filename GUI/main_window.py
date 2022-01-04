from tkinter import *

import cv2
from PIL import Image
from guizero import *
from guizero import App, Text
from datetime import datetime

from POSE_DETECTION.pose_classifer import PoseClassifier

'''
pip3 install guizero
pip3 install guizero[images]
set READTHEDOCS=True
pip install picamera
'''
DATA_PATH = 'POSE_DETECTION/images'
POSITIVE_EMO = ['positive_interaction', 'authority', 'appriciative', 'confidence', 'calm', 'excitement', 'happy',
                'reliability']
NEGATIVE_EMO = ['insecure', 'fear', 'discomfort', 'anger', 'shy', 'confusion', 'stubborn', 'sad']


# Functions------------------------------------------------
def classify_pose(path):
    pose_classifier = PoseClassifier(r'C:\Users\Tehila Naki\PycharmProjects\AI_project\POSE_DETECTION\data')
    poses = pose_classifier.classify_pose(path)
    return poses


def recommand(emo):
    pass


def visual(emo_res, pos, neg):
    button_list = {}
    pos_box = Box(app, grid=[1, 0, 1, 2], align='left')
    neg_box = Box(app, grid=[2, 0, 1, 2], align='left')
    '''if emo_res == None:
        rec_txt.destroy()
        rec_txt=Text(app,text='THERE NO classify_pose',grid=[0,2,3,1],height=5, width=110,bg='pink',align='center')'''
    for emo in pos:
        im = Image.open('emotion_icons/' + emo + '.jpg')
        im = im.resize((50, 50))
        box = Box(pos_box, align='top')
        PushButton(box, command=recommand(emo), align='right', image=im)
        Emo = emo[0].upper() + emo[1:]
        txt = Text(box, align='right', text=Emo, height=4, width=21)
        button_list[emo] = box
        if emo_res != None and emo in emo_res:
            button_list[emo].bg = 'green'
        else:
            button_list[emo].bg = 'yellow'
    for emo in neg:
        im = Image.open('emotion_icons/' + emo + '.jpg')
        im = im.resize((50, 50))
        box = Box(neg_box, align='top')
        PushButton(box, command=recommand(emo), align='right', image=im)
        Emo = emo[0].upper() + emo[1:]
        txt = Text(box, align='right', text=Emo, height=4, width=21)
        button_list[emo] = box
        if emo_res != None and emo in emo_res:
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
    n_file = open('new_images/number', 'r+')
    number = n_file.read()
    n_file.seek(0)
    n_file.truncate()
    n_file.write(str(int(number) + 1))
    n_file.close()
    curr_time = datetime.today().strftime("%d-%m-%Y--%H%M%S")
    return 'new_images/' + 'img' + number + '_' + curr_time + '.jpg'


def view_img(img_path):
    poses = classify_pose(img_path)
    visual(poses, POSITIVE_EMO, NEGATIVE_EMO)


def upload_img():
    filename = browseFiles()
    im = Image.open(filename)
    viewer.image = im
    filename = get_new_name()
    im.save(filename)
    view_img(filename)


def capture_img():
    cam = cv2.VideoCapture(0)
    frame = cam.read()[1]
    filename = get_new_name()
    cv2.imwrite(filename, frame)
    im = Image.open(filename)
    viewer.image = im
    view_img(filename)


# APP-----------------------------------------------------
NAME = 'AI_PROJECT'
MESSAGE = 'please insert image'
app = App(title=NAME, layout='grid', height=728, width=998)
app.bg = 'lightblue'
# Widgets---------------------------------------------------
b = Box(app, grid=[0, 1])

up = PushButton(b, command=upload_img, text='Upload', align='left', height=5, width=30)
up.bg = 'red'

take = PushButton(b, command=capture_img, text='Take a picture', align='left', height=5, width=30)
take.bg = 'red'

viewer = Picture(app, image='emotion_icons/mad.jpg', grid=[0, 0], height=500, width=480)

rec_txt = Text(app, grid=[0, 2, 3, 1], height=5, width=110, bg='pink', align='center', text='recommand')

# Display---------------------------------------------------
app.display()
