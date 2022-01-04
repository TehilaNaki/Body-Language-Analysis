import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from POSE_DETECTION.detect_single_image_pose_coordinates import ImageToCoordinates


class PoseClassifier:
    def __init__(self, data_folder='data/'):
        mlb = MultiLabelBinarizer()
        x_train = pd.read_csv(data_folder + '\\data_x.csv')
        y_train = pd.read_csv(data_folder + '\\annotations.csv')

        # preprocess
        x_train['image_id'] = pd.to_numeric(x_train['image_id'], errors='coerce')
        y_train['label'] = y_train['label'].apply(eval)
        data = x_train.merge(y_train[['image_id', 'label']], on='image_id')
        binary_y = mlb.fit_transform(data['label'].tolist())

        # train
        forest = RandomForestClassifier(random_state=1)
        multi_target_forest = MultiOutputClassifier(forest, n_jobs=-1)
        multi_target_forest.fit(data.drop(['image_id', 'label'], axis=1), binary_y)

        self.mlb = mlb
        self.model = multi_target_forest
        self.img2coor = ImageToCoordinates()

    def classify_pose(self, image_path):
        coordinates = self.img2coor.get_coordinates(image_path)
        if coordinates is None:
            return None
        coordinates = [coordinates.iloc[0].tolist()]
        pred = self.model.predict(coordinates)
        transformed_pred = list(self.mlb.inverse_transform(pred)[0])
        return transformed_pred


# example of usage
if __name__ == '__main__':
    pose_classifier = PoseClassifier()
    image_path = '/Users/ruthmiller/PycharmProjects/AI_project/POSE_DETECTION/images/0019.jpg'
    poses = pose_classifier.classify_pose(image_path)
    print(f'Image path: {image_path}')
    print(f'Poses: {poses}')
