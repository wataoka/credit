require(e1071)
require(kernlab)
require(dplyr)
require(data.table)

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
train_table %>%
    mutate(
        default_payment_next_month = as.factor(default_payment_next_month == 1)
    ) %>%
    ksvm(
        default_payment_next_month ~ .,
        data=train_table
    ) -> svm_model

# evaluate  
preds = predict(decision_tree_model, test_table)
labels = test_table[, 24]

acc <- accuracy(preds, labels)
rec <- recall(preds, labels)
prec <- precision(preds, labels)
f <- f_measure(preds, labels)

sprintf("accuracy: %.3f",  acc)
sprintf("recall: %.3f",  rec)
sprintf("precision: %.3f",  prec)
sprintf("f measure: %.3f",  f)