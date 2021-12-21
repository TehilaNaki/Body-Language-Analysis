import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer

mlb = MultiLabelBinarizer()

data_folder = 'POSE_DETECTION/data/'
x_train = pd.read_csv(data_folder + 'data_x.csv')
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

# test
sample1 = [data.drop(['image_id', 'label'], axis=1).iloc[0].tolist()]
true_label1 = data.iloc[0]['label']
image_id1 = data.iloc[0]['image_id']
pred1 = multi_target_forest.predict(sample1)
transformed_pred1 = list(mlb.inverse_transform(pred1)[0])
print('image: ', image_id1)
print('prediction: ', transformed_pred1)
print('true label: ', true_label1)

#
# clf = RandomForestClassifier(max_depth=2, random_state=0)
# clf.fit(data.drop(['image_id', 'label'], axis=1), np.array(data['label']))
