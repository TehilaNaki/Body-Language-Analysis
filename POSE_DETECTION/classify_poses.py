import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from POSE_DETECTION.detect_single_image_pose_coordinates import ImageToCoordinates

data_folder = 'POSE_DETECTION/data/'
mlb = MultiLabelBinarizer()
x_train = pd.read_csv(data_folder + 'data_x_new_10-1-22.csv')
y_train = pd.read_csv(data_folder + 'annotations.csv')

# preprocess
x_train['image_id'] = pd.to_numeric(x_train['image_id'], errors='coerce')
y_train['label'] = y_train['label'].apply(eval)
data = x_train.merge(y_train[['image_id', 'label']], on='image_id')
binary_y = mlb.fit_transform(data['label'].tolist())

# train
forest = RandomForestClassifier(random_state=1)
multi_target_forest = MultiOutputClassifier(forest, n_jobs=-1)
multi_target_forest.fit(data.drop(['image_id', 'label'], axis=1), binary_y)

# test1 - from the train set
sample1 = [data.drop(['image_id', 'label'], axis=1).iloc[0].tolist()]
true_label1 = data.iloc[0]['label']
image_id1 = data.iloc[0]['image_id']
pred1 = multi_target_forest.predict(sample1)
transformed_pred1 = list(mlb.inverse_transform(pred1)[0])
print('image: ', image_id1)
print('prediction: ', transformed_pred1)
print('true label: ', true_label1)

# test2 - classify single image, using the ImageToCoordinates class (also from the train set)
img2coor = ImageToCoordinates()
image_path = '/Users/ruthmiller/PycharmProjects/AI_project/POSE_DETECTION/images/0019.jpg'
sample2 = img2coor.get_coordinates(image_path)
if sample2 is not None:
    sample2 = [sample2.iloc[0].tolist()]
    pred2 = multi_target_forest.predict(sample2)
    transformed_pred2 = list(mlb.inverse_transform(pred2)[0])
    print('image: ', image_path)
    print('prediction: ', transformed_pred2)


# TODO need to add test set