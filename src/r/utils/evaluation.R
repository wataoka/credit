accuracy <- function(preds, labels) {
    acc = 0.0
    for (i in 1:dim(preds)[1]) {
        acc <- acc + preds[i, as.integer(labels[i]) + 1]
    }
    return(acc / dim(preds)[1])
}

precision <- function(preds, labels) {
    num_preds_p = 0
    num_correct_preds_p = 0
    for (i in 1:dim(preds)[1]) {
        if (preds[i, 1] < preds[i, 2]) {
            num_preds_p = num_preds_p + 1
            if (labels[i] == 1) {
                num_correct_preds_p = num_correct_preds_p + 1
            }
        }
    }
    return(num_correct_preds_p/num_preds_p)
}

recall <- function(preds, labels) {
    num_p = 0
    num_preds_p = 0
    for (i in 1:dim(preds)[1]) {
        if (labels[i] == 1) {
            num_p = num_p + 1
            if (preds[i, 1] < preds[i, 2]) {
                num_preds_p = num_preds_p + 1
            }
        }
    }
    return(num_preds_p/num_p)
}

f_measure <- function(preds, labels) {
    rec <- recall(preds, labels)
    prec <- precision(preds, labels)
    return((2*rec*prec)/(rec+prec))
}