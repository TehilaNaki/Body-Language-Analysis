import cv2
import mediapipe as mp
import pandas as pd


class ImageToCoordinates:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose
        mp_pose_landmark = self.mp_pose.PoseLandmark
        self.landmarks = {'RIGHT_SHOULDER': mp_pose_landmark.RIGHT_SHOULDER, 'LEFT_SHOULDER': mp_pose_landmark.LEFT_SHOULDER,
                     'RIGHT_ELBOW': mp_pose_landmark.RIGHT_ELBOW, 'LEFT_ELBOW': mp_pose_landmark.LEFT_ELBOW,
                     'RIGHT_WRIST': mp_pose_landmark.RIGHT_WRIST, 'LEFT_WRIST': mp_pose_landmark.LEFT_WRIST,
                     'RIGHT_HIP': mp_pose_landmark.RIGHT_HIP, 'LEFT_HIP': mp_pose_landmark.LEFT_HIP,
                     'RIGHT_KNEE': mp_pose_landmark.RIGHT_KNEE, 'LEFT_KNEE': mp_pose_landmark.LEFT_KNEE,
                     'RIGHT_ANKLE': mp_pose_landmark.RIGHT_ANKLE, 'LEFT_ANKLE': mp_pose_landmark.LEFT_ANKLE,
                     'RIGHT_HEEL': mp_pose_landmark.RIGHT_HEEL, 'LEFT_HEEL': mp_pose_landmark.LEFT_HEEL,
                     'RIGHT_FOOT_INDEX': mp_pose_landmark.RIGHT_FOOT_INDEX,
                     'LEFT_FOOT_INDEX': mp_pose_landmark.LEFT_FOOT_INDEX}
        self.img_ext = ('.jpeg', '.jpg', '.png', '.tiff')

    def get_coordinates(self, image_path):
        with self.mp_pose.Pose(
                static_image_mode=True,
                model_complexity=2,
                enable_segmentation=True,
                min_detection_confidence=0.5) as pose:
            image = cv2.imread(image_path)
            image_height, image_width, _ = image.shape
            # Convert the BGR image to RGB before processing.
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            res = {}
            if not results.pose_landmarks:
                return None
            for landmark_key in self.landmarks.keys():
                # TODO maybe do not multiply by the width/height
                res[landmark_key + '_X'] = results.pose_landmarks.landmark[self.landmarks[landmark_key]].x * image_width
                res[landmark_key + '_Y'] = results.pose_landmarks.landmark[self.landmarks[landmark_key]].y * image_height
                res[landmark_key + '_VISIBILITY'] = results.pose_landmarks.landmark[self.landmarks[landmark_key]].visibility
            return pd.DataFrame([res])

