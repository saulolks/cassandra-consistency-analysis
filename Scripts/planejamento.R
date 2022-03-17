library(AlgDesign)


comb = expand.grid(
    "Intervalo entre req." = c(50, 100, 500, 1000),
    "Qnt. usuários" = c(10, 20, 30, 40, 50),
    "Tamanho da req.(kb)"  = c(10, 50, 100, 250, 500),
    "Nível consistência" = c("ONE", "QUORUM", "ALL")
)

write.csv(
  comb,
  file="fullfact_tests.csv",
  row.names = F
)

LakeHuron
