setwd("C:/Users/T-Gamer/Google Drive/Estudos/Pesquisa/Avaliação de Desempenho Full-Factorial Cassandra/Scripts")

install.packages("rstatix")
install.packages("car")

library("rstatix")
library("dplyr")
library("car")

# Verificando normalidade dos dados
data$consistency <- factor(data$consistency)
data$users <- factor(data$users)
data %>% group_by(consistency) %>% shapiro_test(average)

# Verificando variância homogênea
leveneTest(average ~ consistency, data = data)

# Caso variância não seja homogênea
oneway.test(average ~ consistency, data = data)

# Verificando outliers
data %>% group_by(consistency) %>% identify_outliers(average)

# Aplicando ANOVA
data.aov <- aov(formula = average ~ consistency, data = data)
summary(data.aov)

TukeyHSD(data.aov)

# Teste não-paramétrico
friedman.test(y=data$average, groups=data$consistency, blocks=data$name)
