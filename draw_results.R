library(ggplot2)
library(reshape2)

running_time <- data.frame(
		benchmark = rep(241.37,4),
		SVR = c(12.31,59.34,154.13,504.94)+c(8.50,8.93,9.64,12.17),
		boosted_tree = c(20.86,69.37,124.66,237.24)+c(8.50,8.93,9.64,12.17),
		ordinary_Kriging = c( 3.11,17.03,34.78,81.24)+c(8.50,8.93,9.64,12.17),
		k = c(100,500,1000,2000))



plotting_data <- melt(running_time, id="k",value.name="time",variable.name="method")
ggplot(data=plotting_data,
       aes(x=k, y=time, colour=method,linetype = method)) +
       geom_line(lwd = 0.8)+
       geom_point(aes(shape=method,size=2))+
       ylab("Average CPU time in seconds")+
       scale_size(guide='none')


RPD <- data.frame(
		SVR = c(2.96,1.20,1.01,0.18),
		boosted_tree = c(10.68,0.12,0.30,0.48),
		ordinary_Kriging = c(7.08,0.84,0.38,0.14),
		k = c(100,500,1000,2000))

plotting_data <- melt(RPD, id="k",value.name="rpd",variable.name="method")
ggplot(data=plotting_data,
       aes(x=k, y=rpd, colour=method,linetype = method)) +
       geom_line(lwd = 0.8)+
       geom_point(aes(shape=method,size=2))+
       ylab("Relative portfolio difference(%)")+
       scale_size(guide='none')



RPD <- data.frame(
      random_sampling = c(1.91,0.33,0.23,0.13),
      clustering = c(7.08,0.84,0.38,0.14),   
       k = c(100,500,1000,2000))

plotting_data <- melt(RPD, id="k",value.name="rpd",variable.name="method")
ggplot(data=plotting_data,
       aes(x=k, y=rpd, colour=method,linetype = method)) +
       geom_line(lwd = 0.8)+
       geom_point(aes(shape=method,size=2))+
       ylab("Relative portfolio difference(%)")+
       scale_size(guide='none')+
       ggtitle("ordinary Kriging")


RPD <- data.frame(
      random_sampling = c(1.90,0.46,0.39,0.20),
      clustering = c(10.68,0.12,0.30,0.48),   
       k = c(100,500,1000,2000))

plotting_data <- melt(RPD, id="k",value.name="rpd",variable.name="method")
ggplot(data=plotting_data,
       aes(x=k, y=rpd, colour=method,linetype = method)) +
       geom_line(lwd = 0.8)+
       geom_point(aes(shape=method,size=2))+
       ylab("Relative portfolio difference(%)")+
       scale_size(guide='none')+
       ggtitle("boosted tree")



RPD <- data.frame(
      random_sampling = c(1.89,1.30,1.25,0.14),
      clustering = c(2.96,1.20,1.01,0.18),   
       k = c(100,500,1000,2000))

plotting_data <- melt(RPD, id="k",value.name="rpd",variable.name="method")
ggplot(data=plotting_data,
       aes(x=k, y=rpd, colour=method,linetype = method)) +
       geom_line(lwd = 0.8)+
       geom_point(aes(shape=method,size=2))+
       ylab("Relative portfolio difference(%)")+
       scale_size(guide='none')+
       ggtitle("SVR")


RPD <- data.frame(
      random_sampling = c(1.23,0.29,0.26,0.16)/c(1.90,0.46,0.39,0.20)*100,
      clustering = c(0.34,0.10,0.10,0.05)/c(10.68,0.12,0.30,0.48)*100,   
       k = c(100,500,1000,2000))

plotting_data <- melt(RPD, id="k",value.name="rpd",variable.name="method")
ggplot(data=plotting_data,
       aes(x=k, y=rpd, colour=method,linetype = method)) +
       geom_line(lwd = 0.8)+
       geom_point(aes(shape=method,size=2))+
       ylab("CV of RPD (%)")+
       scale_size(guide='none')+
       ggtitle("boosted tree")





RPD <- data.frame(
      random_sampling = c(59.22,85.69,48.01,68.65),
      clustering = c(2.62,11.66,15.91,25.82),   
       k = c(100,500,1000,2000))

plotting_data <- melt(RPD, id="k",value.name="rpd",variable.name="method")
ggplot(data=plotting_data,
       aes(x=k, y=rpd, colour=method,linetype = method)) +
       geom_line(lwd = 0.8)+
       geom_point(aes(shape=method,size=2))+
       ylab("CV of RPD (%)")+
       scale_size(guide='none')+
       ggtitle("ordinary Kriging method")



RPD <- data.frame(
      random_sampling = c(1.37,0.67,0.55,0.10)/c(1.89,1.30,1.25,0.14)*100,
      clustering = c(0.35,0.15,0.23,0.14)/c(2.96,1.20,1.01,0.18)*100,   
       k = c(100,500,1000,2000))

plotting_data <- melt(RPD, id="k",value.name="rpd",variable.name="method")
ggplot(data=plotting_data,
       aes(x=k, y=rpd, colour=method,linetype = method)) +
       geom_line(lwd = 0.8)+
       geom_point(aes(shape=method,size=2))+
       ylab("CV of RPD (%)")+
       scale_size(guide='none')+
       ggtitle("SVR")


