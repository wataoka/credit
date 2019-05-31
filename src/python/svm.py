import pdb

import optuna
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

data_path = "./../../data/data.csv"


data = pd.read_csv(data_path)
data = data.drop('ID', axis=1)
data = data.drop('EDUCATION', axis=1)
data = data.drop('MARRIAGE', axis=1)

y = data['default payment next month']
x = data[data.columns[data.columns!='default payment next month']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15)

svm = SVR(C=1.4701687180079286, epsilon=0.21811864828587813)
svm.fit(x_train, y_train)

y_pred = svm.predict(x_test)

cm = confusion_matrix(y_test, y_pred.round())

precision = cm[0][0]/(cm[0][0]+cm[1][0])
recall = cm[0][0]/(cm[0][0]+cm[0][1])
f = (2*precision*recall)/(precision+recall)

print("confusion matrix: {}".format(cm))
print("precision: {}".format(precision))
print("recall: {}".format(recall))
print("f-measure: {}".format(f))