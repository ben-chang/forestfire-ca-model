setwd("C:/Users/Alasdair/Desktop/GSA")

df <- read.csv("[file_name].csv", header = T)
head(df)
summary(df)

# create training and testing sample
set.seed(2017)
train.size <- 0.8
df.train.index <- sample.int(length(df$risk), round(length(df$risk) * train.size))
df.train.sample <- df[df.train.index,]
df.test.sample <- df[-train.size,]

# calculate regression model
fit1 <- lm(risk ~ treatment, data = df.train.sample)

summary(fit1)

# Plot regression model
par(mar=c(5,5,4,2))
regression.plot(fit1, pch=".", conf.bands = TRUE, 
                xlab='Fuel Treatment Intensity (%)',
                ylab='Wildfire Risk Probability')

# Create prediction column for both samples 
df.train.sample$pred.risk <- predict(fit1, newdata = subset(df.train.sample.clean, select=treatment))
df.test.sample$pred.risk <- predict(fit1, newdata = subset(df.test.sample.clean, select=treatment))

# Post-Hoc testing on training sample
train.corr <- cor(df.train.sample$pred.risk, df.train.sample$risk)
train.RMSE <- sqrt(mean((df.train.sample$pred.risk - df.train.sample$risk)^2))
train.MAE <- mean(abs(df.train.sample$pred.risk - df.train.sample$risk))
c(train.corr^2, train.RMSE, train.MAE)

# Post-hoc testing on testing sample
test.corr <- cor(df.test.sample$pred.risk, df.train.sample$risk)
test.RMSE <- sqrt(mean((df.test.sample$pred.risk - df.test.sample$risk)^2))
test.MAE <- mean(abs(df.test.sample$pred.risk - df.test.sample$risk))
c(test.corr^2, test.RMSE, test.MAE)
