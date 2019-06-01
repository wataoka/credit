import pdb
import optuna
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

def objective(trial):
    eta = trial.suggest_uniform('eta', 0.1, 0.9)
    max_depth = trial.suggest_int('max_depth', 4, 6)
    subsample = trial.suggest_uniform('subsample', 0.1, 1)
    colsample_bytree = trial.suggest_uniform('colsample_bytree', 0.1, 1)
    learning_rate = trial.suggest_uniform('learning_rate', 0, 1.0)
    num_round = trial.suggest_int('num_round', 1, 30)
    scale_pos_weight = trial.suggest_uniform('scale_pos_weight', 2.0, 4.0)

    params = {
        'eta': eta,
        'max_depth': max_depth,
        'learning_rate': learning_rate,
        'subsample': subsample,
        'colsample_bytree': colsample_bytree,
        'objective': 'binary:logistic',
        'silent': 1,
        'scale_pos_weight': scale_pos_weight
    }

    model = xgb.train(params, d_train, num_round)

    y_pred = model.predict(d_test)
    y_pred = [int(i > 0.5) for i in y_pred]
    
    cm = confusion_matrix(y_test, y_pred)
    
    acc = (cm[0][0] + cm[1][1])/(cm[0][0] + cm[1][0] + cm[0][1] + cm[1][1])
    precision = cm[1][1]/(cm[1][1]+cm[0][1])
    recall = cm[1][1]/(cm[1][1]+cm[1][0])
    f = (2*precision*recall)/(precision+recall)

    print()
    print("confusion matrix:")
    print(cm)
    print("accuracy: {}".format(acc))
    print("precision: {}".format(precision))
    print("recall: {}".format(recall))
    print("f-measure: {}".format(f))
    print()
    return 1.0 - f


data_path = "./../../data/data.csv"

data = pd.read_csv(data_path)
data = data.drop('ID', axis=1)

y = data['default payment next month']
x = data[data.columns[data.columns!='default payment next month']]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

d_train = xgb.DMatrix(x_train, label=y_train)
d_test = xgb.DMatrix(x_test, label=y_test)

study = optuna.create_study()
study.optimize(objective, n_trials=3000)

print("----- result -----")
print("best params")
print(study.best_params)
print()
print("best f-measure")
print(1.0 - study.best_value)
print()
print("best trial")
print(study.best_trial)