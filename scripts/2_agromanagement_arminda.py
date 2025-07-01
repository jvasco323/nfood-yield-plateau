# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Import general packages

import os
import numpy as np
from random import randint

# ----------------------------------------------------------------------------------------------------------------------
# Specify directory

work_dir = os.getcwd()
dir = os.path.join(work_dir, "4-hberghuijs-model--final/input/agro-arminda")

# ----------------------------------------------------------------------------------------------------------------------
# Agromanager template

seasonal = """
Version: 1.0
AgroManagement:
{Season} 
"""

Season = """- {year_start}-{month_start_season}-{day_start_season}:
    CropCalendar:
       crop_name: 'winterwheat'
       variety_name: 'Arminda'
       crop_start_date: {year_start}-11-15
       crop_start_type: sowing
       crop_end_date: {year_end}-09-01
       crop_end_type: maturity
       max_duration: 340
    TimedEvents: null
    StateEvents: null"""

# ----------------------------------------------------------------------------------------------------------------------
# Winter wheat

year_start = np.arange(1971, 2016, 1)
year_end = np.arange(1972, 2017, 1)
month_start_season = "%02d" % 10
day_start_season = "%02d" % 1

for year in year_end:
   WW_Monocrop = seasonal.format(Season=Season.format(year_end=year, year_start=year-1, month_start_season=month_start_season, day_start_season=day_start_season))
   output = os.path.join(dir, "Agrom_WW_Monocrop_{year}.txt".format(year=year))
   with open(output, "w") as fp:
      fp.write(WW_Monocrop)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
