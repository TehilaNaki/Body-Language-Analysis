import pickle
from POSE_DETECTION.detect_single_image_pose_coordinates import ImageToCoordinates
import os
import re


class PoseClassifier:
    def __init__(self, data_folder='model'):
        data_folder = re.split(r'/|\\', data_folder)
        model_path = os.sep.join(data_folder + ['multi_target_forest_dict.pickle'])
        print(model_path)
        with open(model_path, 'rb') as f:
            model_dict = pickle.load(f)
            self.mlb = model_dict['mlb']
            self.model = model_dict['model']
        self.img2coor = ImageToCoordinates()

    def classify_pose(self, image_path):
        coordinates = self.img2coor.get_coordinates(image_path)
        if coordinates is None:
            return None
        coordinates = [coordinates.iloc[0].tolist()]
        pred = self.model.predict(coordinates)
        transformed_pred = list(self.mlb.inverse_transform(pred)[0])
        print(transformed_pred)
        return transformed_pred


# example of usage
if __name__ == '__main__':
    pose_classifier = PoseClassifier()
    image_path = '/Users/ruthmiller/PycharmProjects/AI_project/POSE_DETECTION/images/57.jpg'
    poses = pose_classifier.classify_pose(image_path)
    print(f'Image path: {image_path}')
    print(f'Poses: {poses}')
