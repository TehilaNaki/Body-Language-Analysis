from datetime import datetime
from tkinter import *
import cv2
from PIL import Image
from guizero import *
from POSE_DETECTION.pose_classifer import PoseClassifier
import recommendation as r

DATA_PATH = 'POSE_DETECTION/images'
POSITIVE_EMO = ['positive interaction', 'authoritative', 'confidence', 'calm', 'excitement', 'happiness',
                'reliability']
NEGATIVE_EMO = ['insecurity', 'fear', 'discomfort', 'anger', 'shyness', 'confusion', 'stubbornness']
FILES_TYPES = ['JPG', 'PNG', 'jpg', 'png', 'jpeg']


# Functions------------------------------------------------
def classify_pose(path):
    pose_classifier = PoseClassifier(r'..\POSE_DETECTION\model')
    poses = pose_classifier.classify_pose(path)
    return poses


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
    if im.format != 'jpg':
        im = im.convert("RGB")
    #   im = im.rotate(90)
    if im.width > 595 or im.height > 480:
        im.resize((595, 480))
    filename = get_new_name()
    viewer.image = im
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


def recommend(*emo):
    emo = ''.join(emo)
    rec = Window(app, title=emo, width=850, height=765)
    rec.bg = 'beige'
    rec.font = 'Calibri'
    rec._text_size = 15
    txt_rec = Text(rec, align='top')
    txt_rec.value = r.rec[emo]
    rec.show()


def visual(emo_res, pos, neg):
    if emo_res is None or len(emo_res) == 0:
        app.info("Information", "Unable to identify body language:(")
    button_list = {}
    pos_box = Box(app, grid=[1, 1, 1, 2], align='left')
    neg_box = Box(app, grid=[2, 1, 1, 2], align='left')
    for emo in pos:
        im = Image.open('emotion_icons/' + emo + '.jpg')
        im = im.resize((70, 70))
        box = Box(pos_box, align='top')
        PushButton(box, command=recommend, args=emo, align='right', image=im)
        Emo = emo[0].upper() + emo[1:]
        Text(box, align='right', text=Emo, height=5, width=21)
        button_list[emo] = box
        if emo_res is not None and emo in emo_res:
            button_list[emo].bg = 'LightCyan2'
        else:
            button_list[emo].bg = 'ivory2'
    for emo in neg:
        im = Image.open('emotion_icons/' + emo + '.jpg')
        im = im.resize((70, 70))
        box = Box(neg_box, align='top')
        PushButton(box, command=recommend, args=emo, align='right', image=im)
        Emo = emo[0].upper() + emo[1:]
        Text(box, align='right', text=Emo, height=5, width=21)
        button_list[emo] = box
        if emo_res is not None and emo in emo_res:
            button_list[emo].bg = 'LightCyan2'
        else:
            button_list[emo].bg = 'ivory2'


# Function for opening the file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/Pictures",
                                          title="Select a File",
                                          filetypes=(("IMAGE_FILES",
                                                      "*.*"),
                                                     ("all files",
                                                      "*.*")))
    if filename != '' and filename.split('.')[-1] not in FILES_TYPES:
        app.error(f'Not Valid', f'Unsupported file type\n Select image file type!!\n {FILES_TYPES}')
        return browseFiles()
    else:
        return filename


# APP-----------------------------------------------------
NAME = 'BODY LANGUAGE ANALYSIS'
MESSAGE = 'Please insert image'
BG_IMAGE = 'emotion_icons/open image.jpg'
app = App(title=NAME, layout='grid', height=800, width=985)
app.bg = 'pink1'
app.font = 'Calibri bold'
# APP Widgets---------------------------------------------------
b = Box(app, grid=[0, 2])

up = PushButton(b, command=upload_img, text='Upload', align='left', height=5, width=35)
up.bg = 'pink1'

take = PushButton(b, command=capture_img, text='Take a picture', align='left', height=5, width=36)
take.bg = 'pink1'

viewer = Picture(app, image=BG_IMAGE, grid=[0, 1], height=595, width=480)
view_img(BG_IMAGE)

# explane
Text(app, grid=[0, 3, 3, 1], height=3, width=120, bg='pink1', align='top',
     text='For an explanation of image analysis and additional recommendations for a specific classification:\n Click '
          'the icon button next to the classification.')
# title
Text(app, grid=[0, 0, 3, 1], height=1, width=120, bg='pink1', align='top', text='BODY LANGUAGE ANALYSIS')

# Display---------------------------------------------------
app.display()
