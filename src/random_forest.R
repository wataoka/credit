require(ranger)
require(dplyr)
require(data.table)
require(randomForest)

source("utils/data.R")
source("utils/evaluation.R")

# load data
data_table = get_data_table()

# split into train and test (80:20)
num_data <- nrow(data_table)
num_train <- sample(num_data, num_data*0.8)

train_table <- data_table[num_train]
test_table <- data_table[-num_train]

# train
ranger_model <- ranger(
  formula = as.factor(default_payment_next_month) ~ ., # default.payment.next.monthが目的変数になる
  data = train_table,
  num.trees = 1000,
  mtry = 5,
  write.forest = TRUE,
  importance = 'impurity',
  probability = TRUE
)

# evaluate  
preds = predict(ranger_model, data=test_table)
labels = test_table[, 24]

acc <- accuracy(preds, labels)
rec <- recall(preds, labels)
prec <- precision(preds, labels)
f <- f_measure(preds, labels)

sprintf("accuracy: %.3f",  acc)
sprintf("recall: %.3f",  rec)
sprintf("precision: %.3f",  prec)
sprintf("f measure: %.3f",  f)