import os
import cv2
import mediapipe as mp
import numpy as np
import time

# TODO need to install packages, see rows below
# pip install opencv-python
# pip install mediapipe
# pip install numpy
import pandas as pd

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_pose_landmark = mp_pose.PoseLandmark
landmarks = {'RIGHT_SHOULDER': mp_pose_landmark.RIGHT_SHOULDER, 'LEFT_SHOULDER': mp_pose_landmark.LEFT_SHOULDER,
             'RIGHT_ELBOW': mp_pose_landmark.RIGHT_ELBOW, 'LEFT_ELBOW': mp_pose_landmark.LEFT_ELBOW,
             'RIGHT_WRIST': mp_pose_landmark.RIGHT_WRIST, 'LEFT_WRIST': mp_pose_landmark.LEFT_WRIST,
             'RIGHT_HIP': mp_pose_landmark.RIGHT_HIP, 'LEFT_HIP': mp_pose_landmark.LEFT_HIP,
             'RIGHT_KNEE': mp_pose_landmark.RIGHT_KNEE, 'LEFT_KNEE': mp_pose_landmark.LEFT_KNEE,
             'RIGHT_ANKLE': mp_pose_landmark.RIGHT_ANKLE, 'LEFT_ANKLE': mp_pose_landmark.LEFT_ANKLE,
             'RIGHT_HEEL': mp_pose_landmark.RIGHT_HEEL, 'LEFT_HEEL': mp_pose_landmark.LEFT_HEEL,
             'RIGHT_FOOT_INDEX': mp_pose_landmark.RIGHT_FOOT_INDEX,
             'LEFT_FOOT_INDEX': mp_pose_landmark.LEFT_FOOT_INDEX}

# For static images:
data_folder = 'POSE_DETECTION/images/'
img_ext = ('.jpeg', '.jpg', '.png', '.tiff')
IMAGE_FILES = []
for file in os.listdir(data_folder):
    if file.endswith(img_ext):
        IMAGE_FILES.append(data_folder + file)
dict_list = []
BG_COLOR = (192, 192, 192)  # gray
with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        enable_segmentation=True,
        min_detection_confidence=0.5) as pose:
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        image_height, image_width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.pose_landmarks:
            continue
        print(
            f'Nose coordinates: ('
            f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
            f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
        )
        res = {'image_id': file.split('.')[0].split('/')[-1]}
        for landmark_key in landmarks.keys():
            # TODO maybe do not multiply by the width/height
            res[landmark_key + '_X'] = results.pose_landmarks.landmark[landmarks[landmark_key]].x * image_width
            res[landmark_key + '_Y'] = results.pose_landmarks.landmark[landmarks[landmark_key]].y * image_height
            res[landmark_key + '_VISIBILITY'] = results.pose_landmarks.landmark[landmarks[landmark_key]].visibility
        annotated_image = image.copy()
        # Draw segmentation on the image.
        # To improve segmentation around boundaries, consider applying a joint
        # bilateral filter to "results.segmentation_mask" with "image".
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        annotated_image = np.where(condition, annotated_image, bg_image)
        # Draw pose landmarks on the image.
        mp_drawing.draw_landmarks(
            annotated_image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        cv2.imwrite(
            '/Users/ruthmiller/Documents/computer_science_studies/4th_year/semesterA/AI/project/data/tmp/annotated_image/' + str(
                idx) + '.png', annotated_image)
        # Plot pose world landmarks.
        # mp_drawing.plot_landmarks(
        #     results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
        dict_list.append(res)

res_df = pd.DataFrame(dict_list)
res_df.to_csv('/Users/ruthmiller/PycharmProjects/AI_project/POSE_DETECTION/data/data_x_new_12-2-22.csv', index=False)
