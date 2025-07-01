
dir <- "D:/# Jvasco/# Portfolio/Curriculum/6. CIMMYT Scientist/_WUR PPS Wheat Trials/4-hberghuijs-model--final/output/"

sites <- c('DE BILT', 'EELDE', 'VLISSINGEN')
for(s in sites){
  print(s)
  
  # ----------------------------------------------------------------------------
  #  yp

  print('Yp')
  yp_julius = readxl::read_excel(paste0(dir, "julius-2009/yp-long-term-summary-", s, "-co2-clay.xlsx"))
  yp_julius$var <- 'Julius'
  yp_arminda = readxl::read_excel(paste0(dir, "arminda-1977/yp-long-term-summary-", s, "-co2-clay.xlsx"))
  yp_arminda$var <- 'Arminda'
  yp <- rbind(yp_julius, yp_arminda)
  
  reg <- lm(TWSO ~ year * as.factor(var), data=yp)
  summary(reg)
  print(anova(reg))
  
  png(paste0(dir, '# comparisons/yp-', s, '.png'), units="in", width=10, height=5.5, res=1000)
  par(mfrow=c(1,2), mar=c(5,5,3,1), cex.lab=1.2)
  # plot 1
  plot(yp$year, yp$TWSO, ylim=c(5000, 14000), main=paste0('Yp - ', s),
       xlab='Year', ylab='Wheat yield (t/ha)')
  points(yp_arminda$year, yp_arminda$TWSO, col=2)
  lines(yp_arminda$year, yp_arminda$TWSO, col=2)
  reg <- lm(TWSO ~ year, data=yp_arminda)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = 2)} 
  points(yp_julius$year, yp_julius$TWSO, col='blue')
  lines(yp_julius$year, yp_julius$TWSO, col='blue')
  reg <- lm(TWSO ~ year, data=yp_julius)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "blue")} 
  legend('topleft', legend=c('Arminda', 'Julius'), col=c(2, 'blue'), lty=1)
  # plot 2
  rhsp_dt <- reshape2::dcast(yp, year ~ var, value.var='TWSO')
  rhsp_dt$diff <- rhsp_dt$Julius - rhsp_dt$Arminda
  plot(rhsp_dt$year, rhsp_dt$diff, ylim=c(500,2500),
       xlab='Year', ylab='Yield Julius - Yield Arminda (t/ha)')
  points(rhsp_dt$year, rhsp_dt$diff, col=1)
  lines(rhsp_dt$year, rhsp_dt$diff, col=1)
  reg <- lm(diff ~ year, data=rhsp_dt)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = 1)} 
  box()
  dev.off()
  
  # ----------------------------------------------------------------------------
  # yw - clay
  
  print('Yw-clay')
  yw_julius = readxl::read_excel(paste0(dir, "julius-2009/yw-long-term-summary-", s, "-co2-clay.xlsx"))
  yw_julius$var <- 'Julius'
  yw_arminda = readxl::read_excel(paste0(dir, "arminda-1977/yw-long-term-summary-", s, "-co2-clay.xlsx"))
  yw_arminda$var <- 'Arminda'
  yw <- rbind(yw_julius, yw_arminda)
  
  reg <- lm(TWSO ~ year * as.factor(var), data=yw)
  summary(reg)
  print(anova(reg))
  
  png(paste0(dir, '# comparisons/yw-clay-', s, '.png'), units="in", width=10, height=5.5, res=1000)
  par(mfrow=c(1,2), mar=c(5,5,3,1), cex.lab=1.2)
  # plot 1
  plot(yw$year, yw$TWSO, ylim=c(5000, 14000), main=paste0('Yw clay - ', s),
       xlab='Year', ylab='Wheat yield (t/ha)')
  points(yw_arminda$year, yw_arminda$TWSO, col=2)
  lines(yw_arminda$year, yw_arminda$TWSO, col=2)
  reg <- lm(TWSO ~ year, data=yw_arminda)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = 2)} 
  points(yw_julius$year, yw_julius$TWSO, col='blue')
  lines(yw_julius$year, yw_julius$TWSO, col='blue')
  reg <- lm(TWSO ~ year, data=yw_julius)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "blue")} 
  legend('topleft', legend=c('Arminda', 'Julius'), col=c(2, 'blue'), lty=1)
  # plot 2
  rhsp_dt <- reshape2::dcast(yw, year ~ var, value.var='TWSO')
  rhsp_dt$diff <- rhsp_dt$Julius - rhsp_dt$Arminda
  plot(rhsp_dt$year, rhsp_dt$diff, ylim=c(500,2500),
       xlab='Year', ylab='Yield Julius - Yield Arminda (t/ha)')
  points(rhsp_dt$year, rhsp_dt$diff, col=1)
  lines(rhsp_dt$year, rhsp_dt$diff, col=1)
  reg <- lm(diff ~ year, data=rhsp_dt)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = 1)} 
  box()
  dev.off()
  
  # ----------------------------------------------------------------------------
  # yw - sand
  
  print('Yw-sand')
  yw_julius = readxl::read_excel(paste0(dir, "julius-2009/yw-long-term-summary-", s, "-co2-sand.xlsx"))
  yw_julius$var <- 'Julius'
  yw_arminda = readxl::read_excel(paste0(dir, "arminda-1977/yw-long-term-summary-", s, "-co2-sand.xlsx"))
  yw_arminda$var <- 'Arminda'
  yw <- rbind(yw_julius, yw_arminda)
  
  reg <- lm(TWSO ~ year * as.factor(var), data=yw)
  summary(reg)
  print(anova(reg))
  
  png(paste0(dir, '# comparisons/yw-sand-', s, '.png'), units="in", width=10, height=5.5, res=1000)
  par(mfrow=c(1,2), mar=c(5,5,3,1), cex.lab=1.2)
  # plot 1
  plot(yw$year, yw$TWSO, ylim=c(5000, 14000), main=paste0('Yw sand - ', s),
       xlab='Year', ylab='Wheat yield (t/ha)')
  points(yw_arminda$year, yw_arminda$TWSO, col=2)
  lines(yw_arminda$year, yw_arminda$TWSO, col=2)
  reg <- lm(TWSO ~ year, data=yw_arminda)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = 2)} 
  points(yw_julius$year, yw_julius$TWSO, col='blue')
  lines(yw_julius$year, yw_julius$TWSO, col='blue')
  reg <- lm(TWSO ~ year, data=yw_julius)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = "blue")} 
  legend('topleft', legend=c('Arminda', 'Julius'), col=c(2, 'blue'), lty=1)
  # plot 2
  rhsp_dt <- reshape2::dcast(yw, year ~ var, value.var='TWSO')
  rhsp_dt$diff <- rhsp_dt$Julius - rhsp_dt$Arminda
  plot(rhsp_dt$year, rhsp_dt$diff, ylim=c(500,2500),
       xlab='Year', ylab='Yield Julius - Yield Arminda (t/ha)')
  points(rhsp_dt$year, rhsp_dt$diff, col=1)
  lines(rhsp_dt$year, rhsp_dt$diff, col=1)
  reg <- lm(diff ~ year, data=rhsp_dt)
  summary_model <- summary(reg)
  p_value <- summary_model$coefficients[2, 4]
  if (p_value < 0.05) {abline(reg, col = 1)} 
  box()
  dev.off()
  
}
