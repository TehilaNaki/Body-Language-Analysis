import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from POSE_DETECTION.detect_single_image_pose_coordinates import ImageToCoordinates
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import pickle

data_folder = 'POSE_DETECTION/data/'
mlb = MultiLabelBinarizer()
x_train = pd.read_csv(data_folder + 'data_x_new_10-1-22.csv')
y_train = pd.read_csv(data_folder + 'annotations.csv')

# preprocess
x_train['image_id'] = pd.to_numeric(x_train['image_id'], errors='coerce')
y_train['label'] = y_train['label'].apply(eval)
data = x_train.merge(y_train[['image_id', 'label']], on='image_id')
binary_y = mlb.fit_transform(data['label'].tolist())
features_names = data.drop(['image_id', 'label'], axis=1).columns

# train/test split
x_train, x_test, y_train, y_test = train_test_split(data, binary_y, train_size=0.9,
                                                    random_state=42)
x_test = x_test.drop(['image_id', 'label'], axis=1)

#############################################################
# generate synthetic data
synthetic_data = [x_train]
for i in range(1, 9):
    tmp_data = data.copy()
    tmp_data[features_names] = tmp_data[features_names] + i
    synthetic_data.append(tmp_data)
synthetic_data = pd.concat(synthetic_data, axis=0)
# decide whether to use synthetic x and y
x_train = synthetic_data
y_train = mlb.fit_transform(x_train['label'].tolist())
#############################################################


# training
forest = RandomForestClassifier(random_state=1)
multi_target_forest = MultiOutputClassifier(forest, n_jobs=-1)
multi_target_forest.fit(x_train.drop(['image_id', 'label'], axis=1), y_train)

# testing
labels_names = mlb.classes_
y_pred = multi_target_forest.predict(x_test)
y_pred_conf = np.max([[np.max(j) for j in i] for i in multi_target_forest.predict_proba(x_test)], 0)
print('accuracy:', accuracy_score(y_test, y_pred, normalize=True))
print(classification_report(y_test, y_pred, target_names=labels_names))

# # saving model
# pkl_dict = {'mlb': mlb, 'model': multi_target_forest}
# with open('POSE_DETECTION/model/multi_target_forest_dict.pickle', 'wb') as f:
#     pickle.dump(pkl_dict, f)

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

