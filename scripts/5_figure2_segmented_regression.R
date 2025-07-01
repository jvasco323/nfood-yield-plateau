#=====================================================================================================
#=====================================================================================================

rm(list=ls())
library(segmented)
library(quantreg)

#=====================================================================================================
#=====================================================================================================

dir <- 'D:/# Jvasco/# Portfolio/Curriculum/6. CIMMYT Scientist/_WUR PPS Wheat Trials/4-hberghuijs-model--final'
site <- 'debilt'
yld <- 'yp'
soil <- 'sand'
path = paste0(dir, "/output/gf-vs-yield-", site, "-", yld, "-", soil, ".csv")
ya = read.csv(path)
ya$unique2 <- ya$unique^2
quadraticModel <- lm(yp ~ unique + unique2, data=ya)
summary(quadraticModel)
plot(ya$unique, ya$yp)
quadraticModel <- quantreg::rq(yp ~ unique + unique2, data=ya, tau=0.9)
summary(quadraticModel)
coefs5 <- coef(quadraticModel)
curve(coefs5[1]+coefs5[2]*(x)+coefs5[3]*x^2,add=T,col="black", lwd=2,lty=2)
derivative <- abs(coefs5[2])/(2*abs(coefs5[3]))
y <- coefs5[1]+coefs5[2]*(derivative)+coefs5[3]*derivative^2

#=====================================================================================================
#=====================================================================================================

dir <- 'D:/# Jvasco/# Portfolio/Curriculum/6. CIMMYT Scientist/_WUR PPS Wheat Trials/4-hberghuijs-model--final'
yld <- 'yw'
soil <- 'clay'
path = paste0(dir, "/output/rad-vs-yield-", yld, "-", soil, ".csv")
ya = read.csv(path)
ya$RAD_em_mat <- ya$RAD_em_mat
y5 = quantreg::nlrq(yp ~ ifelse((RAD_em_mat)<a, b*(RAD_em_mat), b*a), start=c(a=2400,b=0.05), data=ya, tau=0.90)
summary(y5)
plot(ya$RAD_em_mat, ya$yp, ylim=c(0,13), xlim=c(0,3000))
coefs5 <- coef(y5)
curve(ifelse((x)<coefs5[1], coefs5[2]*(x), coefs5[1]*coefs5[2]),add=T,col="black", lwd=2,lty=2)

dir <- 'D:/# Jvasco/# Portfolio/Curriculum/6. CIMMYT Scientist/_WUR PPS Wheat Trials/4-hberghuijs-model--final'
yld <- 'yw'
soil <- 'clay'
path = paste0(dir, "/output/gdd-vs-yield-", yld, "-", soil, ".csv")
ya = read.csv(path)
y5 = nlrq(yp ~ a + b * GDD_em_mat + I(c * 0.99 ** GDD_em_mat), start=c(a=10, b=5, c=10000), data=ya, tau=0.90)
summary(y5)
coefs5 <- coef(y5)
plot(ya$GDD_em_mat, ya$yp)
curve(coefs5[1] + coefs5[2] * x + coefs5[3] * 0.99**x, add=T,col="black", lwd=2,lty=2)

dir <- 'D:/# Jvasco/# Portfolio/Curriculum/6. CIMMYT Scientist/_WUR PPS Wheat Trials/4-hberghuijs-model--final'
yld <- 'yw'
soil <- 'sand'
path = paste0(dir, "/output/etp-vs-yield-", yld, "-", soil, ".csv")
ya = read.csv(path)
ya$CTRAT = ya$CTRAT*10 + ya$CEVST*10
y5 = quantreg::nlrq(yp ~ ifelse((CTRAT+c)<a, b*(CTRAT+c), b*a), start=c(a=400,b=0.8,c=8), data=ya, tau=0.90)
summary(y5)
coefs5 <- coef(y5)
plot(ya$CTRAT, ya$yp, xlim=c(0,500), ylim=c(0,13))
curve(ifelse((x+coefs5[3])<coefs5[1], coefs5[2]*(x+coefs5[3]), coefs5[1]*coefs5[2]),add=T,col="black", lwd=2,lty=2)
