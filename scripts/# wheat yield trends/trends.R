
# --------------------------------------------------------------
# actual trends

data <- read.csv('ya_groningen.csv')
data <- subset(data, Perioden <= 2016)
reg <- lm(data$yield_tha ~ data$Perioden)
summary(reg)
data <- read.csv('ya_flevoland.csv')
data <- subset(data, Perioden <= 2016)
reg <- lm(data$yield_tha ~ data$Perioden)
summary(reg)
data <- read.csv('ya_zuidholland.csv')
data <- subset(data, Perioden <= 2016)
reg <- lm(data$yield_tha ~ data$Perioden)
summary(reg)

# --------------------------------------------------------------
# genetic trends

site <- 'eelde'
genetics <- read.csv(paste0('julius/# yp_emmeans_', site, '.csv'))
reg <- lm(genetics$emmean ~ genetics$yr_release)
summary(reg)
plot(genetics$yr_release, genetics$emmean, ylim=c(7,13))
abline(reg, col=2, lwd=2)
abline(v=1994)

genetics_94 <- subset(genetics, yr_release >= 1994)
reg <- lm(genetics_94$emmean ~ genetics_94$yr_release)
summary(reg)
plot(genetics_94$yr_release, genetics_94$emmean, ylim=c(7,13))
abline(reg, col=2, lwd=2)

# --------------------------------------------------------------
# climate trends 

variety <- 'julius'
site <- 'VLISSINGEN'
file <- paste0(variety, '/yp-long-term-summary-', site, '-co2-clay.xlsx')
climate <- readxl::read_excel(file)
reg <- lm(climate$TWSO ~ climate$year)
summary(reg)
plot(climate$year, climate$TWSO, ylim=c(8000,14000))
abline(reg, col=2, lwd=2)
abline(v=1994)

climate_94 <- subset(climate, year >= 1994)


plot(climate_94$year, climate_94$TWSO, ylim=c(8000,14000))
reg <- lm(climate_94$TWSO ~ climate_94$year)
summary(reg)
abline(reg, col=2, lwd=2)

aa <- subset(climate_94, TWSO > 11000) # for vlissingen
reg <- lm(aa$TWSO ~ aa$year)
summary(reg)
abline(reg, col=2, lwd=2)





climate$anthesis <- lubridate::yday(as.Date(climate$DOE))
climate_94 <- subset(climate, year >= 1994)
plot(climate_94$anthesis, climate_94$TWSO)
abline(h=11000, col=2)

# --------------------------------------------------------------
# climate trends 

variety <- 'julius'
site <- 'VLISSINGEN'
file <- paste0(variety, '/yp-long-term-daily-', site, '-co2-clay.xlsx')
climate <- readxl::read_excel(file)

climate$day <- as.Date(climate$DAY)
climate$yday <- lubridate::yday(climate$day)
climate <- subset(climate, day > as.Date('1994-11-01'))

plot(climate$yday, climate$EVS)
sbst1 <- subset(climate, day > as.Date('2005-11-01') & day < as.Date('2006-09-01'))
sbst2 <- subset(climate, day > as.Date('2006-11-01') & day < as.Date('2007-09-01'))
sbst3 <- subset(climate, day > as.Date('2012-11-01') & day < as.Date('2013-09-01'))
points(sbst1$yday, sbst1$EVS, col=2)
points(sbst2$yday, sbst2$EVS, col=3)
points(sbst3$yday, sbst3$EVS, col=4)

climate$year <- lubridate::year(as.Date(climate$DAY))
climate$month <- lubridate::month(as.Date(climate$DAY))

aa <- aggregate(climate$IRRAD/1000000, by=list('month'=climate$month, 'year'=climate$year), FUN=sum)
ab <- aggregate(climate[c('TMAX', 'TMIN')], by=list('month'=climate$month, 'year'=climate$year), FUN=mean)


par(mfrow=c(1,3))

plot(aa$month, aa$x, xlim=c(0,8))
lines(aa$month[aa$year==2006], aa$x[aa$year==2006], col=2)
lines(aa$month[aa$year==2007], aa$x[aa$year==2007], col=3)
lines(aa$month[aa$year==2013], aa$x[aa$year==2013], col=4)


plot(ab$month, ab$TMAX, xlim=c(0,8))
lines(ab$month[ab$year==2006], ab$TMAX[ab$year==2006], col=2)
lines(ab$month[ab$year==2007], ab$TMAX[ab$year==2007], col=3)
lines(ab$month[ab$year==2013], ab$TMAX[ab$year==2013], col=4)

plot(ab$month, ab$TMIN, xlim=c(0,8))
lines(ab$month[ab$year==2006], ab$TMIN[ab$year==2006], col=2)
lines(ab$month[ab$year==2007], ab$TMIN[ab$year==2007], col=3)
lines(ab$month[ab$year==2013], ab$TMIN[ab$year==2013], col=4)

dev.off()
climate_july <- subset(climate, month ==7)
plot(climate_july$yday, climate_july$TEMP)
lines(climate_july$yday[climate_july$year==2006], climate_july$TEMP[climate_july$year==2006], col=2)
lines(climate_july$yday[climate_july$year==2007], climate_july$TEMP[climate_july$year==2007], col=3)
lines(climate_july$yday[climate_july$year==2013], climate_july$TEMP[climate_july$year==2013], col=4)

