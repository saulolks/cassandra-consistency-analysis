install.packages("remotes")
remotes::install_github("coolbutuseless/ggpattern", force=TRUE)
install.packages('Rcpp')

# imports
library(Rcpp)
library(readr)
library(ggplot2)
library(dplyr)
library(tidyr)
library("ggpattern")


# interno (eixo y/eixo x)
data <- read_csv("C:/Users/T-Gamer/Google Drive/Estudos/Pesquisa/Avaliação de Desempenho Full-Factorial Cassandra/Data/Results/sample_result.csv")

# preprocessing
data$error <- as.numeric(sub(",", ".", sub("%","",data$error)))/100
data_stress$error <- as.numeric(sub(",", ".", sub("%","",data_stress$error)))
data_stress$error <- as.numeric(sub(",", ".", data_stress$error))

# 1. consistencia/tempo resposta/usuarios ----
chart1_data <- data
chart1_data$consistency <- factor(chart1_data$consistency,levels=c("ONE","QUORUM","ALL"), ordered=T)
chart1_data_aux <- chart1_data %>% group_by(consistency, users) %>% summarise(average=mean(average))

ggplot(data=chart1_data_aux, aes(x=users, y=average, fill=consistency)) + 
  geom_point() +
  xlab("Concurrent users") + 
  ylab("Response time (ms)")

ggplot(data=chart1_data_aux, aes(x=users, y=average, fill=consistency)) + 
  geom_bar(stat="identity", width=5, position="dodge", color="black") +
  xlab("Concurrent users") + 
  ylab("Response time (ms)") +
  #labs(fill = "Consistency level") +
  scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18)) +
  geom_col_pattern(
    aes(pattern = consistency),
    colour = "black",
    pattern_fill = "black",
    pattern_angle = 45,
    pattern_density = 0.1,
    pattern_spacing = 0.01,
    position = position_dodge2(preserve = 'single'),
  ) 



# 2. intervalo/tempo resposta/usuarios ----
chart2_data <- data
chart2_data$interval <- factor(chart2_data$interval,levels=c("100","500","1000"), ordered=T)
chart2_data_aux <- chart2_data %>% group_by(interval, users) %>% summarise(average=mean(average))

ggplot(data=chart2_data_aux, aes(x=users, y=average, fill=interval)) + 
  geom_bar(stat="identity", width=5, position="dodge", color="black") +
  xlab("Concurrent users") + 
  ylab("Response time (ms)") +
  scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18)) +
  geom_col_pattern(
    aes(pattern = interval),
    colour = "black",
    pattern_fill = "black",
    pattern_angle = 45,
    pattern_density = 0.1,
    pattern_spacing = 0.01,
    position = position_dodge2(preserve = 'single'),
  )

ggplot(chart2_data_aux, aes(x = users, y = average)) + 
  geom_line(aes(color = interval, linetype = interval))



# 3. linhas/tempo resposta/usuarios ----
chart3_data <- data
chart3_data$lines <- factor(chart3_data$lines,levels=c("1000","5000","10000"), ordered=T)
chart3_data_aux <- chart3_data %>% group_by(lines, users) %>% summarise(average=mean(average))

ggplot(data=chart3_data_aux, aes(x=users, y=average, fill=lines)) + 
  geom_bar(stat="identity", width=5, position="dodge", color="black") +
  xlab("Concurrent users") + 
  ylab("Response time (ms)") +
  labs(fill = "Size") +
  #scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18))

ggplot(chart3_data_aux, aes(x = users, y = average)) + 
  geom_line(aes(color = lines, linetype = lines), size=2) +
  scale_linetype_manual(values=c("twodash", "dotted", "solid"))+
  scale_color_manual(values=c("#aba9a9", "#363636", "#252625"))



# 4. consistencia/tempo resposta/linhas ----
chart4_data <- data
chart4_data$consistency <- factor(chart4_data$consistency,levels=c("ONE","QUORUM","ALL"), ordered=T)
chart4_data_aux <- chart4_data %>% group_by(consistency, lines) %>% summarise(average=mean(average))

ggplot(data=chart4_data_aux, aes(x=lines, y=average, fill=consistency)) + 
  geom_bar(stat="identity", width=5, position="dodge", color="black") +
  xlab("Concurrent users") + 
  ylab("Response time (ms)") +
  labs(fill = "Consistency") +
  #scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18))

ggplot(chart4_data_aux, aes(x = lines, y = average)) + 
  geom_line(aes(color = consistency, linetype = consistency), size=2) +
  ylab("Response time (ms)") +
  xlab("Lines") + 
  scale_linetype_manual(values=c("twodash", "dotted", "solid"))+
  scale_color_manual(values=c("#aba9a9", "#363636", "#252625"))


# 5. consistencia/erro/usuarios ----
chart5_data <- data
chart5_data$consistency <- factor(chart5_data$consistency,levels=c("ONE","QUORUM","ALL"), ordered=T)
chart5_data_aux <- chart5_data %>% group_by(consistency, users) %>% summarise(error=mean(error))

ggplot(data=chart5_data_aux, aes(x=users, y=error, fill=consistency)) + 
  geom_bar(stat="identity", width=5, position="dodge", color="black") +
  xlab("Concurrent users") + 
  ylab("Error (%)") +
  labs(fill = "Consistency") +
  #scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18))


# 6. linhas/erro/usuarios ----
chart6_data <- data
chart6_data$lines <- factor(chart6_data$lines,levels=c("1000","5000","10000"), ordered=T)
chart6_data_aux <- chart6_data %>% group_by(lines, users) %>% summarise(error=mean(error))

ggplot(data=chart6_data_aux, aes(x=users, y=error, fill=lines)) + 
  geom_bar(stat="identity", width=5, position="dodge", color="black") +
  xlab("Concurrent users") + 
  ylab("Error (%)") +
  scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18)) +
  geom_col_pattern(
    aes(pattern = lines),
    colour = "black",
    pattern_fill = "black",
    pattern_angle = 45,
    pattern_density = 0.1,
    pattern_spacing = 0.01,
    position = position_dodge2(preserve = 'single'),
  )


# 7. consistencia/erro/usuarios (STRESS) ----
chart1stress_data <- data_stress
chart1stress_data$consistency <- factor(chart1stress_data$consistency,levels=c("ONE","QUORUM","ALL"), ordered=T)
chart1stress_data_aux <- chart1stress_data %>% group_by(users) %>% summarise(error=mean(error), average=mean(average))

ggplot(data=chart1stress_data_aux, aes(x=users, y=error, fill=consistency)) + 
  geom_point() +
  xlab("Concurrent users") + 
  ylab("Response time (ms)")

ggplot(data=chart1stress_data, aes(x=users, y=error, fill=consistency)) + 
  geom_bar(stat="identity", width=5, position="dodge", color="black") +
  xlab("Concurrent users") + 
  ylab("Response time (ms)") +
  labs(fill = "Consistency level") +
  scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18))


ggplot(data=chart1stress_data, aes=(x=users)) +
  geom_line(aes(x=users,y=average)) +
  geom_line(aes(x=users,y=error, size=2)) +
  scale_y_continuous(name="Average response time", sec.axis = sec_axis(trans=~./10000, name="Error rate"))

ggplot() +
  geom_bar(data=chart1stress_data_aux, aes(y=average, fill=users)) +
  geom_line(data=chart1stress_data_aux, aes(x=users,y=error, size=2)) +
  scale_y_continuous(name="Average response time", sec.axis = sec_axis(trans=~./5000, name="Error rate"))

# 8. ./erro-tempo/usuarios (STRESS) ----


# 9. consistencia/throughput/usuarios (STRESS) ----
chart3stress_data <- data_stress
chart3stress_data$consistency <- factor(chart3stress_data$consistency,levels=c("ONE","QUORUM","ALL"), ordered=T)
chart3stress_data_aux <- chart3stress_data %>% group_by(consistency,users) %>% summarise(throughput=mean(throughput))

ggplot(data=chart3stress_data_aux, aes(x=users, y=throughput, fill=consistency)) + 
  geom_point() +
  xlab("Concurrent users") + 
  ylab("Response time (ms)")

ggplot(data=chart3stress_data_aux, aes(x=users, y=throughput, fill=consistency)) + 
  geom_bar(stat="identity", width=5, position="dodge", color="black") +
  xlab("Concurrent users") + 
  ylab("Response time (ms)") +
  labs(fill = "Consistency level") +
  scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18))


# LAB -----
library(ggplot2)

data1 <- data_stress %>% filter(consistency == "ALL")
data1$error <- 100*data1$error
ggp <- ggplot(data1)  + 
  geom_bar(aes(x=users, y=average),stat="identity", fill="cyan",colour="#006000")+
  geom_line(aes(x=users, y=100*error),stat="identity",color="red",size=2)+
  labs(title= "Stress error and average time to respond",
       x="Year",y="Average response time")+
  scale_y_continuous(sec.axis=sec_axis(~.*0.01,name="Error rate"))
ggp
