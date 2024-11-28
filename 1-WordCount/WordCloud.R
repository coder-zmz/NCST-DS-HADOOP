library(wordcloud2)

setwd("D:\\Code\\R")
# 读取词频,制表符分隔
data <- read.table("part-r-00000", sep = "\t", header = FALSE)
# 排序
data <- data[order(data$V2, decreasing = TRUE), ]
wordcloud2(data)
