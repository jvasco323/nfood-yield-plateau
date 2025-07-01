
input_dir = "D:/# Jvasco/# Portfolio/Curriculum/6. CIMMYT Scientist/_WUR PPS Wheat Trials/1-calibration-jsilva-files/Data Input/WOFOST Inputs"
output_dir = "D:/# Jvasco/# Portfolio/Curriculum/6. CIMMYT Scientist/_WUR PPS Wheat Trials/4-hberghuijs-model--final/output"

# ----------------------------------------------------------------------------------------------------------------------
# load data

stations = c('DE BILT', 'EELDE', 'VLISSINGEN')
weather_crop_veg_final <- c()
weather_crop_rep_final <- c()
weather_crop_all_final <- c()

for(s in stations){
  # weather data
  weather = readxl::read_excel(paste0(input_dir, "/KNMI Weather/# WOFOST_Weather_KNMI_", s, "_ANALYSIS.xlsx"))
  weather['DAY'] = as.Date(weather$DAY, format='%Y-%m-%d')
  weather['year'] = format(as.Date(weather$DAY, format="%Y-%m-%d"),"%Y")
  # crop data
  crop = readxl::read_excel(paste0(output_dir, "/yp-long-term-summary-", s, "-co2-clay.xlsx"))
  crop['DOE'] = as.Date(crop$DOE, format='%Y-%m-%d')
  crop['DOA'] = as.Date(crop$DOA, format='%Y-%m-%d')
  crop['DOM'] = as.Date(crop$DOM, format='%Y-%m-%d')
  for(y in unique(crop$year)){
    # subset crop per yr
    crop_yr <- subset(crop, year == y)
    doe <- crop_yr$DOE
    doa <- crop_yr$DOA
    dom <- crop_yr$DOM
    # subset weather
    weather_veg <- subset(weather, DAY > doe & DAY < doa)
    weather_rep <- subset(weather, DAY > doa & DAY < dom)
    weather_all <- subset(weather, DAY > doe & DAY < dom)
    # to data frame
    weather_crop_veg <- data.frame('station'=s, 'year'=y, 
                                   'mean_tmax'=mean(weather_veg$TMAX), 'mean_tmin'=mean(weather_veg$TMIN),
                                   'sum_rad'=sum(weather_veg$IRRAD), 'sum_rain'=sum(weather_veg$RAIN))
    weather_crop_veg_final <- rbind(weather_crop_veg_final, weather_crop_veg)
    # to data frame
    weather_crop_rep <- data.frame('station'=s, 'year'=y, 
                                   'mean_tmax'=mean(weather_rep$TMAX), 'mean_tmin'=mean(weather_rep$TMIN),
                                   'sum_rad'=sum(weather_rep$IRRAD), 'sum_rain'=sum(weather_rep$RAIN))
    weather_crop_rep_final <- rbind(weather_crop_rep_final, weather_crop_rep)
    # to data frame
    weather_crop_all <- data.frame('station'=s, 'year'=y, 
                                   'mean_tmax'=mean(weather_all$TMAX), 'mean_tmin'=mean(weather_all$TMIN),
                                   'sum_rad'=sum(weather_all$IRRAD), 'sum_rain'=sum(weather_all$RAIN))
    weather_crop_all_final <- rbind(weather_crop_all_final, weather_crop_all) } }

# ----------------------------------------------------------------------------------------------------------------------
# fit regressions

models_final_all_stations = c()
models_final_veg_stations = c()
models_final_rep_stations = c()
for(s in stations){
  # all season
  weather_crop_all_final_s <- subset(weather_crop_all_final, station == s)
  weather_crop_all_final_s$sum_rad <- weather_crop_all_final_s$sum_rad/1000 # conversion kJ to MJ
  model_tmax <- lm(mean_tmax ~ year, data=weather_crop_all_final_s)
  model_tmax <- data.frame(cbind(VariableName=rownames(summary(model_tmax)$coef), summary(model_tmax)$coef)[,c(1,2,5)])
  model_tmax$y_var <- 'mean_tmax'
  rownames(model_tmax) <- NULL
  model_tmin <- lm(mean_tmin ~ year, data=weather_crop_all_final_s)
  model_tmin <- data.frame(cbind(VariableName=rownames(summary(model_tmin)$coef), summary(model_tmin)$coef)[,c(1,2,5)])
  model_tmin$y_var <- 'mean_tmin'
  rownames(model_tmin) <- NULL
  model_srad <- lm(sum_rad ~ year, data=weather_crop_all_final_s)
  model_srad <- data.frame(cbind(VariableName=rownames(summary(model_srad)$coef), summary(model_srad)$coef)[,c(1,2,5)])
  model_srad$y_var <- 'sum_rad'
  rownames(model_srad) <- NULL
  model_rain <- lm(sum_rain ~ year, data=weather_crop_all_final_s)
  model_rain <- data.frame(cbind(VariableName=rownames(summary(model_rain)$coef), summary(model_rain)$coef)[,c(1,2,5)])
  model_rain$y_var <- 'sum_rain'
  rownames(model_rain) <- NULL
  models_final_all <- rbind(model_srad, model_tmax, model_tmin, model_rain)
  models_final_all$signif <- ifelse(models_final_all$Pr...t.. < 0.05, '*', 'ns')
  models_final_all$time <- 'all_season'
  models_final_all$station <- s
  models_final_all_stations <- rbind(models_final_all_stations, models_final_all)
  # vegetative
  weather_crop_veg_final_s <- subset(weather_crop_veg_final, station == s)
  weather_crop_veg_final_s$sum_rad <- weather_crop_veg_final_s$sum_rad/1000 # conversion kJ to MJ
  model_tmax <- lm(mean_tmax ~ year, data=weather_crop_veg_final_s)
  model_tmax <- data.frame(cbind(VariableName=rownames(summary(model_tmax)$coef), summary(model_tmax)$coef)[,c(1,2,5)])
  model_tmax$y_var <- 'mean_tmax'
  rownames(model_tmax) <- NULL
  model_tmin <- lm(mean_tmin ~ year, data=weather_crop_veg_final_s)
  model_tmin <- data.frame(cbind(VariableName=rownames(summary(model_tmin)$coef), summary(model_tmin)$coef)[,c(1,2,5)])
  model_tmin$y_var <- 'mean_tmin'
  rownames(model_tmin) <- NULL
  model_srad <- lm(sum_rad ~ year, data=weather_crop_veg_final_s)
  model_srad <- data.frame(cbind(VariableName=rownames(summary(model_srad)$coef), summary(model_srad)$coef)[,c(1,2,5)])
  model_srad$y_var <- 'sum_rad'
  rownames(model_srad) <- NULL
  model_rain <- lm(sum_rain ~ year, data=weather_crop_veg_final_s)
  model_rain <- data.frame(cbind(VariableName=rownames(summary(model_rain)$coef), summary(model_rain)$coef)[,c(1,2,5)])
  model_rain$y_var <- 'sum_rain'
  rownames(model_rain) <- NULL
  models_final_veg <- rbind(model_srad, model_tmax, model_tmin, model_rain)
  models_final_veg$signif <- ifelse(models_final_veg$Pr...t.. < 0.05, '*', 'ns')
  models_final_veg$time <- 'vegetative'
  models_final_veg$station <- s
  models_final_veg_stations <- rbind(models_final_veg_stations, models_final_veg)
  # reproductive
  weather_crop_rep_final_s <- subset(weather_crop_rep_final, station == s)
  weather_crop_rep_final_s$sum_rad <- weather_crop_rep_final_s$sum_rad/1000 # conversion kJ to MJ
  model_tmax <- lm(mean_tmax ~ year, data=weather_crop_rep_final_s)
  model_tmax <- data.frame(cbind(VariableName=rownames(summary(model_tmax)$coef), summary(model_tmax)$coef)[,c(1,2,5)])
  model_tmax$y_var <- 'mean_tmax'
  rownames(model_tmax) <- NULL
  model_tmin <- lm(mean_tmin ~ year, data=weather_crop_rep_final_s)
  model_tmin <- data.frame(cbind(VariableName=rownames(summary(model_tmin)$coef), summary(model_tmin)$coef)[,c(1,2,5)])
  model_tmin$y_var <- 'mean_tmin'
  rownames(model_tmin) <- NULL
  model_srad <- lm(sum_rad ~ year, data=weather_crop_rep_final_s)
  model_srad <- data.frame(cbind(VariableName=rownames(summary(model_srad)$coef), summary(model_srad)$coef)[,c(1,2,5)])
  model_srad$y_var <- 'sum_rad'
  rownames(model_srad) <- NULL
  model_rain <- lm(sum_rain ~ year, data=weather_crop_rep_final_s)
  model_rain <- data.frame(cbind(VariableName=rownames(summary(model_rain)$coef), summary(model_rain)$coef)[,c(1,2,5)])
  model_rain$y_var <- 'sum_rain'
  rownames(model_rain) <- NULL
  models_final_rep <- rbind(model_srad, model_tmax, model_tmin, model_rain)
  models_final_rep$signif <- ifelse(models_final_rep$Pr...t.. < 0.05, '*', 'ns')
  models_final_rep$time <- 'reproductive'
  models_final_rep$station <- s
  models_final_rep_stations <- rbind(models_final_rep_stations, models_final_rep)}
all_models <- rbind(models_final_veg_stations, models_final_rep_stations, models_final_all_stations)
  
# ----------------------------------------------------------------------------------------------------------------------
# final table

all_models <- subset(all_models, VariableName == 'year')
all_models$Estimate <- round(as.numeric(all_models$Estimate), 3)
all_models$Estimate <- paste(all_models$Estimate, all_models$signif)
all_models <- all_models[c(7,6,4,1,2)]
all_models <- reshape2::dcast(all_models, time + y_var ~ station, value.var='Estimate')
all_models <- all_models[order(all_models$y_var),]
all_models <- all_models[c(2,1,4,3,5)]
tabResultX <- xtable::xtable(all_models)
print(tabResultX, include.rownames=FALSE)
