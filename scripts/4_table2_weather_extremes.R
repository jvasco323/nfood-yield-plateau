
dir <- "D:/# Jvasco/# Portfolio/Curriculum/6. CIMMYT Scientist/_WUR PPS Wheat Trials/4-hberghuijs-model--final/output/"

sites <- c('DE BILT', 'EELDE', 'VLISSINGEN')
for(s in sites){
  print(s)

  data <- read.csv(paste0(dir, "extreme-weather-", s, ".csv"))
  png(paste0(dir, 'extreme-weather-', s, '.png'), units="in", width=12.2, height=4.5, res=1000)
  par(mfrow=c(1,3), mar=c(5,5,3,1), cex.lab=1.6, cex.axis=1.5, cex.main=1.5, xaxs='i', yaxs='i')
  
  # plot 1
  plot(data$year, data$TMAX_max, ylim=c(-20,40), xlab='Year', ylab='Temperature', main=s)
  grid(nx=NULL, ny=NULL)
  abline(h=0)
  # tmax
  points(data$year, data$TMAX_max, pch=21, col='darkred', bg='darkred')
  lines(data$year, data$TMAX_max, col='darkred', lty=1)
  reg <- lm(TMAX_max ~ year, data=data)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "darkred")} 
  points(data$year, data$TMAX_min, pch=21, col='orangered', bg='orangered')
  lines(data$year, data$TMAX_min, col='orangered', lty=1)
  reg <- lm(TMAX_min ~ year, data=data)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "orangered")} 
  # tmin
  points(data$year, data$TMIN_max, pch=21, col='royalblue', bg='royalblue')
  lines(data$year, data$TMIN_max, col='royalblue', lty=1)
  reg <- lm(TMIN_max ~ year, data=data)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "royalblue")} 
  points(data$year, data$TMIN_min, pch=21, col='darkblue', bg='darkblue')
  lines(data$year, data$TMIN_min, col='darkblue', lty=1)
  reg <- lm(TMIN_min ~ year, data=data)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "darkblue")} 
  legend(1985, 11, bty='y', cex=1.2, ncol=2, legend=c('TMAX_max', 'TMAX_min', 'TMIN_max', 'TMIN_min'), col=c('darkred', 'orangered', 'royalblue', 'darkblue'), pt.bg=c('darkred', 'orangered', 'royalblue', 'darkblue'), pch=21, lty=1)
  box()
  
  # plot 2
  plot(data$year, data$arid_days, ylim=c(0,200), xlab='Year', ylab='Number of days', main=s)
  grid(nx=NULL, ny=NULL)
  # arid days
  points(data$year, data$arid_days, pch=21, col='darkred', bg='darkred')
  lines(data$year, data$arid_days, col='darkred', lty=1)
  reg <- lm(arid_days ~ year, data=data)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "darkred")} 
  # wet days
  points(data$year, data$wet_days, pch=21, col='royalblue', bg='royalblue')
  lines(data$year, data$wet_days, col='royalblue', lty=1)
  reg <- lm(wet_days ~ year, data=data)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "royalblue")} 
  # frost days
  points(data$year, data$frost_days, pch=21, col='darkblue', bg='darkblue')
  lines(data$year, data$frost_days, col='darkblue', lty=1)
  reg <- lm(frost_days ~ year, data=data)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "darkblue")} 
  legend(2000, 140, bty='y', cex=1.2, ncol=1, legend=c('Arid days', 'Wet days', 'Frost days'), col=c('darkred', 'royalblue', 'darkblue'), pt.bg=c('darkred', 'royalblue', 'darkblue'), pch=21, lty=1)
  box()
  
  # plot 3
  plot(data$year, data$max_consec_summer_days, ylim=c(0,240), xlab='Year', ylab='Maximum consecutive days', main=s)
  grid(nx=NULL, ny=NULL)
  # arid days
  points(data$year, data$max_consec_summer_days, pch=21, col='darkred', bg='darkred')
  lines(data$year, data$max_consec_summer_days, col='darkred', lty=1)
  reg <- lm(max_consec_summer_days ~ year, data=data)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "darkred")} 
  # wet days
  points(data$year, data$max_consec_wet_days, pch=21, col='royalblue', bg='royalblue')
  lines(data$year, data$max_consec_wet_days, col='royalblue', lty=1)
  reg <- lm(max_consec_wet_days ~ year, data=data)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "royalblue")} 
  # frost days
  points(data$year, data$max_consec_frost_days, pch=21, col='darkblue', bg='darkblue')
  lines(data$year, data$max_consec_frost_days, col='darkblue', lty=1)
  reg <- lm(max_consec_frost_days ~ year, data=data)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "darkblue")} 
  legend('bottomright', bty='y', cex=1.2, ncol=1, legend=c('Summer days', 'Wet days', 'Frost days'), col=c('darkred', 'royalblue', 'darkblue'), pt.bg=c('darkred', 'royalblue', 'darkblue'), pch=21, lty=1)
  box()
  
  dev.off()
  
}
