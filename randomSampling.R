args <- commandArgs(trailingOnly = TRUE)

no <- args[1]
k <- args[2]
contractfile <- paste("CM_project/scenario_",no,"/va100000.csv",sep="")
valuefile <- paste("CM_project/scenario_",no,"/va100000_",no,"_price.csv",sep="")

mycols <- rep("NULL", 20); 
mycols[c(1,7)] <- "numeric"; 
df <- read.table(valuefile, colClasses=mycols,skip=1,sep=",",header=FALSE)
names(df) <- c("id","fmv")
df <- df[with(df, order(id)),]

contract <- read.table(contractfile, sep=",",header=TRUE)
contract <- contract[with(contract, order(id)), ]
contract <- cbind(df$fmv, contract)
contract$gender <- as.numeric(contract$gender)-1
contract$guarantee.type <- as.numeric(contract$guarantee.type)-1

n <- dim(contract)[1]
training_idx <- sample(1:n,as.numeric(k))
trainData <- contract[training_idx,]
testData <- contract[-training_idx,]

trainfile <- paste("CM_project/scenario_",no,"/",k,"/random_train.csv",sep="")
testfile <- paste("CM_project/scenario_",no,"/",k,"/random_test.csv",sep="")
write.table(trainData, file = trainfile, sep = ",", row.names=FALSE,col.names=FALSE)
write.table(testData, file = testfile, sep = ",", row.names=FALSE,col.names=FALSE)