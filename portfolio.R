
mycols <- rep("NULL", 20); 
mycols[7] <- "numeric"; 
result <- rep(0,30)

for(no in 1:30){	
	valuefile <- paste("CM_project/scenario_",no,"/va100000_",no,"_price.csv",sep="")
	df <- read.table(valuefile, colClasses=mycols,skip=1,sep=",",header=FALSE)
	names(df) <- "fmv"
	result[no] <- sum(df$fmv)
}


ggplot(result, aes(result)) + 
  geom_histogram(aes(y =..density..), 
                 binwidth = 50000000,
                 col="red", 
                 fill="blue", 
                 alpha = .2) + 
  geom_density(col="black") + 
  labs(x="portfolio FMV", y="density")