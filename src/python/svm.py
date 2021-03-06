import pdb
import optuna
import pandas as pd
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

data_path = "./../../data/data.csv"

data = pd.read_csv(data_path)
data = data.drop('ID', axis=1)
# data = data.drop('EDUCATION', axis=1)
# data = data.drop('MARRIAGE', axis=1)

y = data['default payment next month']
x = data[data.columns[data.columns!='default payment next month']]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15)

svm = SVC(kernel='rbf', C=100, gamma='auto', class_weight='balanced')
svm.fit(x_train, y_train)

y_pred = svm.predict(x_test)
y_pred = [int(i > 0.5) for i in y_pred]

cm = confusion_matrix(y_test, y_pred)

precision = cm[1][1]/(cm[1][1]+cm[0][1])
recall = cm[1][1]/(cm[1][1]+cm[1][0])
f = (2*precision*recall)/(precision+recall)

print()
print("confusion matrix:")
print(cm)
print()
print("precision: {}".format(precision))
print("recall: {}".format(recall))
print("f-measure: {}".format(f))