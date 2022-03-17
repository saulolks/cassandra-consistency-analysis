library(AlgDesign)


data = expand.grid("users" = c(10, 20, 30, 40, 50),
            "lines"  = c(1000, 5000, 10000),
            "consistency" = c("ONE", "QUORUM", "ALL"),
            "interval" = c(100, 500, 1000))
write.csv(
  data,
  file="scenarios.csv",
  row.names = T
)
