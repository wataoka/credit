DATA_PATH = "./../data/data.csv"

get_data_table <- function() {
    data_table <- fread(DATA_PATH)
    data_table[, ID:=NULL]
    data_table[, SEX:=as.factor(SEX)]
    data_table[, EDUCATION:=as.factor(EDUCATION)]
    data_table[, MARRIAGE:=as.factor(MARRIAGE)]
    
    names(data_table)[24] <- "default_payment_next_month"

    return(data_table)
}