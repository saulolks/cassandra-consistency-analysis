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
data_error$error <- as.numeric(sub(",", ".", sub("%","",data_error$error)))/100

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
  labs(fill = "Interval time") +
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
  geom_line(aes(color = size, linetype = size))



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
  geom_line(aes(color = consistency, linetype = consistency), size=1)


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
  labs(fill = "Size") +
  #scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18))


# 7. consistencia/erro/usuarios (STRESS) ----
chart1stress_data <- data_error
chart1stress_data$consistency <- factor(chart1stress_data$consistency,levels=c("ONE","QUORUM","ALL"), ordered=T)
chart1stress_data_aux <- chart1stress_data %>% group_by(consistency,users) %>% summarise(error=mean(error))

ggplot(data=chart1stress_data_aux, aes(x=users, y=error, fill=consistency)) + 
  geom_point() +
  xlab("Concurrent users") + 
  ylab("Response time (ms)")

ggplot(data=chart1stress_data_aux, aes(x=users, y=average, fill=consistency)) + 
  geom_bar(stat="identity", width=5, position="dodge", color="black") +
  xlab("Concurrent users") + 
  ylab("Response time (ms)") +
  labs(fill = "Consistency level") +
  scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18))


# 8. ./erro-tempo/usuarios (STRESS) ----


# 9. consistencia/erro/usuarios (STRESS) ----