import pdb

import optuna
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

data_path = "./../../data/data.csv"

def objective(trial):
    svm_c = trial.suggest_loguniform('svr_c', 1e0, 1e2)
    gamma = trial.suggest_loguniform('gamma', 1e-1, 1e1)
    svm = SVR(kernel='rbf', C=svm_c, gamma=gamma)
    svm.fit(x_train, y_train)

    y_pred = svm.predict(x_test)
    y_pred = [int(i > 0.5) for i in y_pred]

    cm = confusion_matrix(y_test, y_pred)

    if 0 in cm:
        print()
        print("0 exists")
        print()
        return 1.0

    precision = cm[1][1]/(cm[1][1]+cm[0][1])
    recall = cm[1][1]/(cm[1][1]+cm[1][0])
    f = (2*precision*recall)/(precision+recall)

    print()
    print("confusion matrix:")
    print(cm)
    print("precision: {}".format(precision))
    print("recall: {}".format(recall))
    print("f-measure: {}".format(f))
    print()

    return 1.0-f


data = pd.read_csv(data_path)
data = data.drop('ID', axis=1)
data = data.drop('SEX', axis=1)
data = data.drop('EDUCATION', axis=1)
data = data.drop('MARRIAGE', axis=1)

print(data.shape)

y = data['default payment next month']
x = data[data.columns[data.columns!='default payment next month']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15)

study = optuna.create_study()
study.optimize(objective, n_trials=1000)
print(study.best_params)
print(study.best_value)
print(study.best_trial)