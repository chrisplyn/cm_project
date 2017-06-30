args <- commandArgs(trailingOnly = TRUE)

if(length(args) != 1){
    stop("input a dataset")
}

suppressMessages(library(caret))

folder <- "CM_project/scenario_1/2000"
trainfile <- paste(folder,"/training_processed.csv",sep="")
testfile <- paste(folder,"/testing_processed.csv",sep="")

colClasses <- c("numeric", "NULL", rep("factor",2), rep("numeric",4))
colNames <- c("fmv", "NULL","type","gender","age","value","rate","maturity")


training <- read.table(trainfile,
		header=F,
		colClasses = colClasses,
        col.names = colNames,
		sep=",")


fitControl <- trainControl(method = "repeatedcv",
                           number = 5, #5-fold cv
                           selectionFunction = "tolerance",
                           repeats = 5)



gbmGrid <-  expand.grid(interaction.depth = c(4,5,6),
                        shrinkage = c(0.001,0.01),
                        n.trees = (1:20)*50,
                        n.minobsinnode = c(5,10)
                        )


start_time <- proc.time()
set.seed(1)
gbmFit <- train(fmv~., 
                 data = training,
                 method = "gbm",
                 trControl = fitControl,
                 verbose = FALSE,
                 tuneGrid = gbmGrid)
training.time <- as.numeric((proc.time() - start_time)[1],units="secs")
cat(paste(training.time,'\n'))

whichOpt <- tolerance(gbmFit$results, metric = "RMSE",tol=1.5, maximize=FALSE)
gbmFit$results[whichOpt,]

plot(gbmFit)


testing <- read.table(testfile,
                header=F,
                colClasses = colClasses,
                col.names = colNames,
                sep=",")

start <- Sys.time()
y_hat <- predict(gbmFit, newdata = testing[-1])
testing.time <- as.numeric(Sys.time()-start,units="secs")
cat(testing.time)

benchmark <- sum(testing$fmv) + sum(training$fmv)
total <- sum(y_hat) + sum(training$fmv)

APD <- abs(total-benchmark)
RPD <- APD/benchmark
MAD <- sum(abs(testing$fmv-y_hat))/100000
RMSE <- sqrt(sum((testing$fmv-y_hat)^2)/100000)

output <- paste(args[1],"/bt_random_results.csv",sep="")
write(c(APD,RPD,MAD,RMSE), file = output ,append = FALSE, sep = ",")