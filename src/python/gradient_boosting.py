import pdb
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

data_path = "./../../data/data.csv"

data = pd.read_csv(data_path)
data = data.drop('ID', axis=1)

y = data['default payment next month']
x = data[data.columns[data.columns!='default payment next month']]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

dmatrix_train = xgb.DMatrix(x_train, label=y_train)

params = {
    'eta': 0.767,
    'max_depth': 4,
    'subsample': 0.731,
    'colsample_bytree': 0.642,
    'learning_rate': 0.331,
    'num_round': 25,
    'objective': 'binary:logistic',
    'scale_pos_weight': 2.613
    }

model = xgb.train(params, dmatrix_train, 30)

dm_test = xgb.DMatrix(x_test)
y_pred = model.predict(dm_test)
y_pred = [int(i > 0.5) for i in y_pred]

cm = confusion_matrix(y_test, y_pred)

acc = (cm[0][0] + cm[1][1])/(cm[0][0] + cm[1][0] + cm[0][1] + cm[1][1])
precision = cm[1][1]/(cm[1][1]+cm[0][1])
recall = cm[1][1]/(cm[1][1]+cm[1][0])
f = (2*precision*recall)/(precision+recall)

print()
print("confusion matrix:")
print(cm)
print()
print("accuracy: {}".format(acc))
print("precision: {}".format(precision))
print("recall: {}".format(recall))
print("f-measure: {}".format(f))