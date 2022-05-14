setwd("~/BCC/Pesquisa/R-Script")

library(ggplot2)

consistency_data = read.csv("select_by_consistency.csv")
consistency_data$consistency <- factor(consistency_data$consistency,levels=c("ONE","QUORUM","ALL"), ordered=T)

ggplot(data=consistency_data, aes(x=users, y=latency, fill=consistency)) + 
  geom_point() +
  xlab("Número de usuários simultâneos") + 
  ylab("Tempo de resposta (ms)")

ggplot(data=consistency_data, aes(x=users, y=latency, fill=consistency)) + 
  geom_bar(stat="identity", width=5, position="dodge", color="black", size=1) +
  xlab("Número de usuários simultâneos") + 
  ylab("Tempo de resposta (ms)") +
  labs(fill = "Nível de consistência") +
  scale_fill_manual(values=c("#ffffff", "#aba9a9", "#252625"))+
  theme(text = element_text(size=18))

# section | Por replicação======================================================
replication_select <- read.csv("select_by_replication.csv")
replication_insert <- read.csv("insert_by_replication.csv")

replication_select$mode <- "select"
replication_insert$mode <- "insert"

replication <- rbind(replication_insert, replication_select)
replication$"Operação" <- replication$mode

ggplot(data=replication, aes(x=replication_factor, y=latency, group=mode)) + 
  geom_line(stat="identity", size=2, aes(linetype=mode, color=mode)) +
  xlab("Fator de replicação") + 
  ylab("Tempo de resposta (ms)") +
  labs(
    color="Operação",
    linetype="Operação"
  ) +
  scale_color_manual(values=c("#a9b0a9", "#737874"))

ggplot(data=replication, aes(x=replication_factor, y=latency, group=mode)) + 
  geom_point(aes(shape=mode, color=mode), size=4, stroke=4) +
  geom_line(size=1.3) +
  xlab("Fator de replicação") + 
  ylab("Tempo de resposta (ms)") +
  labs(
    color="Operação",
    shape="Operação"
  ) +
  scale_color_manual(values=c("#a9b0a9", "#737874")) +
  theme(text = element_text(size=18))


# section | Por tamanho ========================================================

size_data <- read.csv("select_by_size.csv")
size_data$size <- factor(size_data$size,levels=c("800","1600","2400", "3200", "4000"), ordered=T)

ggplot(data=size_data, aes(x=users, y=latency, group=size)) +
  geom_line(stat="identity", size=2, aes(linetype=size, color=size)) +
  xlab("Número de usuários simultâneos") + 
  ylab("Tempo de resposta (ms)") +
  labs(
    color="Tamanho (em bytes)",
    linetype="Tamanho (em bytes)"
  ) +
  scale_color_manual(values=c("#b1b5b1", "#b1b5b1", "#6b6e6b", "#6b6e6b", "#373837")) +
  scale_linetype_manual(values=c("solid", "dotted", "solid", "dotted", "solid"))

ggplot(data=size_data, aes(x=users, y=latency, group=size)) +
  geom_point(aes(shape=size, color=size), size=4, stroke=4) +
  geom_line(size=1.3) +
  xlab("Número de usuários simultâneos") + 
  ylab("Tempo de resposta (ms)") +
  labs(
    color="Tamanho (em bytes)",
    shape="Tamanho (em bytes)"
  ) +
  scale_color_manual(values=c("#b1b5b1", "#b1b5b1", "#6b6e6b", "#6b6e6b", "#373837")) +
  scale_shape_manual(values=c(15,16,17,18,4)) +
  theme(text = element_text(size=18))
