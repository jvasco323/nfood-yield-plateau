# ----------------------------------------------------------------------------------------------------------------------
# IMPORT GENERAL PACKAGES
# ----------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import datetime as dt

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT PCSE PACKAGES
# ----------------------------------------------------------------------------------------------------------------------

import openpyxl
import sqlalchemy
import traitlets_pcse
import requests
import xlrd

import pcse
import glob
import re
import itertools

# ----------------------------------------------------------------------------------------------------------------------
# SPECIFY DIRECTORY
# ----------------------------------------------------------------------------------------------------------------------

dir = r'D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\4-hberghuijs-model--final\output'

# ----------------------------------------------------------------------------------------------------------------------
# EXTREME WEATHER EVENTS
# ----------------------------------------------------------------------------------------------------------------------

sites = ['DE BILT', 'EELDE', 'VLISSINGEN']

for site in sites:
    daily = pd.read_excel(os.path.join(dir, 'yp-long-term-daily-{site}-co2-clay.xlsx'.format(site=site)))
    summary = pd.read_excel(os.path.join(dir, 'yp-long-term-summary-{site}-co2-clay.xlsx'.format(site=site)))
    summary['DOS'] = pd.to_datetime(summary['DOS'], format='%Y%m%d', errors='ignore')
    summary['DOM'] = pd.to_datetime(summary['DOM'], format='%Y%m%d', errors='ignore')
    summary['harv_year'] = summary['DOM'].dt.year
    years = summary.harv_year.unique()
    final_weather = pd.DataFrame()

    for yr in years:
        print('PROCESSED' + '. . . {site} . . . {yr}'.format(site=site, yr=yr))
        # Load and subset dataframes -----------------------------------------------------------------------------------
        summary_yr = summary[(summary.harv_year == yr)]
        sowing_date = summary_yr.DOS.unique()[0]
        harvest_date = summary_yr.DOM.unique()[0]
        # Growing season only ------------------------------------------------------------------------------------------
        subset_daily = daily[(daily.DAY >= sowing_date) & (daily.DAY <= harvest_date)]
        summary_yr['AI_index'] = (subset_daily.RAIN.sum()/subset_daily.ET0.sum())
        # Growing season -----------------------------------------------------------------------------------------------
        summary_yr['season_days'] = len(subset_daily)
        # Mean temperatures --------------------------------------------------------------------------------------------
        summary_yr['TMAX_mean'] = subset_daily.TMAX.mean().round(3)
        summary_yr['TMIN_mean'] = subset_daily.TMIN.mean().round(3)
        summary_yr['TEMP_mean'] = subset_daily.TEMP.mean().round(3)
        # Maximum temperatures -----------------------------------------------------------------------------------------
        summary_yr['TMAX_max'] = subset_daily.TMAX.max().round(3)
        summary_yr['TMIN_max'] = subset_daily.TMIN.max().round(3)
        # Minimum temperatures -----------------------------------------------------------------------------------------
        summary_yr['TMAX_min'] = subset_daily.TMAX.min().round(3)
        summary_yr['TMIN_min'] = subset_daily.TMIN.min().round(3)
        # Cumulative variables -----------------------------------------------------------------------------------------
        summary_yr['RAD_sum'] = subset_daily.IRRAD.sum().round(3)
        summary_yr['ET0_sum'] = subset_daily.ET0.sum().round(3)
        summary_yr['RAIN_sum'] = subset_daily.RAIN.sum().round(3)
        # Coefficient of variation -------------------------------------------------------------------------------------
        summary_yr['TMAX_cv'] = 100*(subset_daily.TMAX.mean()/subset_daily.TMAX.std()).round(3)
        summary_yr['TMIN_cv'] = 100*(subset_daily.TMIN.mean()/subset_daily.TMIN.std()).round(3)
        summary_yr['TEMP_cv'] = 100*(subset_daily.TEMP.mean()/subset_daily.TEMP.std()).round(3)
        summary_yr['RAIN_cv'] = 100*(subset_daily.RAIN.mean()/subset_daily.RAIN.std()).round(3)
        summary_yr['ET0_cv'] = 100*(subset_daily.ET0.mean()/subset_daily.ET0.std()).round(3)
        # Biologically effective degrees day ---------------------------------------------------------------------------
        degree_day = subset_daily[(subset_daily.TEMP > 10) & (subset_daily.TEMP < 30)]
        summary_yr['biol_eff_degr_day'] = degree_day.TEMP.sum().round(3)
        # Wet days -----------------------------------------------------------------------------------------------------
        wet_days = subset_daily[subset_daily.RAIN > 1]
        summary_yr['wet_days'] = len(wet_days)
        # Frost days ---------------------------------------------------------------------------------------------------
        frost_days = subset_daily[subset_daily.TMIN < 0]
        summary_yr['frost_days'] = len(frost_days)
        # Summer days --------------------------------------------------------------------------------------------------
        summer_days = subset_daily[subset_daily.TMAX > 30]
        summary_yr['summer_days'] = len(summer_days)
        # Tropical nights ----------------------------------------------------------------------------------------------
        tropical_nights = subset_daily[subset_daily.TMIN > 20]
        summary_yr['tropical_nights'] = len(tropical_nights)
        # Heavy precipitation days -------------------------------------------------------------------------------------
        heavy_rain_days = subset_daily[subset_daily.RAIN > 10]
        summary_yr['heavy_rain_days'] = len(heavy_rain_days)
        # Very heavy precipitation days --------------------------------------------------------------------------------
        very_heavy_rain_days = subset_daily[subset_daily.RAIN > 20]
        summary_yr['very_heavy_rain_days'] = len(very_heavy_rain_days)
        # Consecutive dry days (longest period of consecutive days with RAIN < 1mm) ------------------------------------
        subset_daily['rainfall_less1'] = np.where(subset_daily.RAIN < 1, 1, 0)
        if subset_daily['rainfall_less1'].sum() != 0:
            a = subset_daily['rainfall_less1']
            z = [(x[0], len(list(x[1]))) for x in itertools.groupby(a)]
            summary_yr['max_consec_dry_days'] = max(z, key=lambda x: x[1])[1]
        else:
            summary_yr['max_consec_dry_days'] = 0
        # Consecutive wet days (longest period of consecutive days with RAIN > 1mm) ------------------------------------
        subset_daily['rainfall_great1'] = np.where(subset_daily.RAIN > 1, 1, 0)
        if subset_daily['rainfall_great1'].sum() != 0:
            a = subset_daily['rainfall_great1']
            z = [(x[0], len(list(x[1]))) for x in itertools.groupby(a)]
            summary_yr['max_consec_wet_days'] = max(z, key=lambda x: x[1])[1]
        else:
            summary_yr['max_consec_wet_days'] = 0
        # Consecutive summer days (longest period of consecutive days with TMAX > 25) ----------------------------------
        subset_daily['tmax_great25'] = np.where(subset_daily.TMAX > 25, 1, 0)
        if subset_daily['tmax_great25'].sum() != 0:
            a = subset_daily['tmax_great25']
            z = [(x[0], len(list(x[1]))) for x in itertools.groupby(a)]
            summary_yr['max_consec_summer_days'] = max(z, key=lambda x: x[1])[1]
        else:
            summary_yr['max_consec_summer_days'] = 0
        # Consecutive frost days (longest period of consecutive days with TMIN < 0) ------------------------------------
        subset_daily['tmin_below0'] = np.where(subset_daily.TMIN < 0, 1, 0)
        if subset_daily['tmin_below0'].sum() != 0:
            a = subset_daily['tmin_below0']
            z = [(x[0], len(list(x[1]))) for x in itertools.groupby(a)]
            summary_yr['max_consec_frost_days'] = max(z, key=lambda x: x[1])[1]
        else:
            summary_yr['max_consec_frost_days'] = 0
        # Arid days ----------------------------------------------------------------------------------------------------
        arid_days = subset_daily[subset_daily.RAIN < subset_daily.ET0]
        summary_yr['arid_days'] = len(arid_days)
        # Append and save dataframe ------------------------------------------------------------------------------------
        final_weather = final_weather.append(summary_yr)

    final_weather = final_weather.drop_duplicates()
    final_weather.to_csv(os.path.join(dir, 'extreme-weather-{site}.csv'.format(site=site)), index=False)

# ----------------------------------------------------------------------------------------------------------------------
# THE END
# ----------------------------------------------------------------------------------------------------------------------
