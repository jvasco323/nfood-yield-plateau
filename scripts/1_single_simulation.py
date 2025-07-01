import pcse
from pcse.fileinput import YAMLCropDataProvider
import os
import pandas as pd
from pcse.base import ParameterProvider
from pcse.fileinput import ExcelWeatherDataProvider
from pcse.models import WOFOST8_ML_PP, WOFOST8_ML_NLP, WOFOST8_ML_NWLP, WOFOST8_ML_WLP
import yaml

cultivar = "Julius"
location = "Wageningen"
treatment = "N3"
year = 2015
nlim = True
wlim = False

# Get directories of input and output files
work_dir = os.getcwd()
input_dir = os.path.join(work_dir, "4-hberghuijs-model--final/input")
output_dir = os.path.join(work_dir, "4-hberghuijs-model--final/output")

# Set crop parameters and input data
agrod = yaml.safe_load(open(os.path.join(input_dir, "agro", f"{location}_{cultivar}_{year}_{treatment}_agro.yaml")))
agrod = agrod['AgroManagement']
cropdata = YAMLCropDataProvider(fpath=os.path.join(input_dir, "crop"), force_reload=True)
cropdata.set_active_crop('winterwheat', f"{cultivar}")
sitedata = yaml.safe_load(open(os.path.join(input_dir, "site", f"{location}_{year}_site.yaml")))
soildata = yaml.safe_load(open(os.path.join(input_dir, "soil", f"lelystad_soil.yaml")))
weatherdata = ExcelWeatherDataProvider(os.path.join(input_dir, "weather", f"WOFOST_Weather_{location}.xls"))
parameters = ParameterProvider(cropdata=cropdata, soildata=soildata, sitedata=sitedata)

# Choose model configuration
if(nlim == True and wlim == True):
    wofost = WOFOST8_ML_NWLP(parameters, weatherdata, agrod)
elif(nlim == False and wlim == True):
    wofost = WOFOST8_ML_WLP(parameters, weatherdata, agrod)
elif(nlim == True and wlim == False): 
    wofost = WOFOST8_ML_NLP(parameters, weatherdata, agrod)
else:
    wofost = WOFOST8_ML_PP(parameters, weatherdata, agrod)

# Run model
wofost.run_till_terminate()

# Store model output
output = pd.DataFrame(wofost.get_output()).set_index("day")
output.to_excel(os.path.join(output_dir, f"output_{cultivar}_{location}_{treatment}.xlsx"))