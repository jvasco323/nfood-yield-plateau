# ----------------------------------------------------------------------------------------------------------------------
# LOAD REQUIRED LIBRARIES, DIRECTORIES, ETC. ---------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dir = r'D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\4-hberghuijs-model--final\output'

# ----------------------------------------------------------------------------------------------------------------------
# DATA -----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

data = pd.read_excel(os.path.join(dir, r".\20230926_yields_scenario_study.xlsx"), sheet_name="Sheet1")
data['yw_perc'] = 100 * data['Y_wl'] / data['Y_pp']
data['ywn_perc'] = 100 * data['Y_wnl'] / data['Y_pp']
data['ya_perc'] = 100 * data['Y_obs'] / data['Y_pp']
# data['yield_class'] = np.where(data.Y_obs < data.Y_obs.quantile(0.25), 'Low', np.nan)
# data['yield_class'] = np.where((data.Y_obs >= data.Y_obs.quantile(0.25)) & (data.Y_obs < data.Y_obs.quantile(0.75)), 'Medium', data.yield_class)
# data['yield_class'] = np.where(data.Y_obs >= data.Y_obs.quantile(0.75), 'High', data.yield_class)
data_new = pd.DataFrame()
for year in data.year.unique():
    subset_year = data[data.year == year]
    subset_year['yield_class'] = np.where(subset_year.Y_obs < subset_year.Y_obs.quantile(0.25), 'Low', np.nan)
    subset_year['yield_class'] = np.where((subset_year.Y_obs >= subset_year.Y_obs.quantile(0.25)) & (subset_year.Y_obs < subset_year.Y_obs.quantile(0.75)), 'Medium', subset_year.yield_class)
    subset_year['yield_class'] = np.where(subset_year.Y_obs >= subset_year.Y_obs.quantile(0.75), 'High', subset_year.yield_class)
    data_new = data_new.append(subset_year)
data = data_new
data.to_csv(os.path.join(dir, 'data.csv'))

# ----------------------------------------------------------------------------------------------------------------------
# YIELD GAPS SUMMARY ---------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

left, width = .215, .71
bottom, height = .25, .71
right = left + width
top = bottom + height
wspace = 0.20
hspace = 0.10
kws_points = dict(s=80, alpha=0.8, linewidth=0.7)
width_barplot = 0.75

f, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12.5, 7*2))
axes = plt.gca()
f.subplots_adjust(wspace=wspace, hspace=hspace)

data = data.sort_values("Y_obs", axis=0, ascending=False)
ax1.set_ylabel('Wheat yield & yield gap (t/ha)', family='sans-serif', fontsize=17, color='black')
ax1.set_xlabel('', family='sans-serif', fontsize=17, color='black')
ax1.grid(axis='y', linestyle='-', color='gainsboro')
ax1.bar(range(len(data.CropFieldID)), list(map(float, (data.Y_pp-data.Y_wl))), width_barplot, edgecolor='tan', bottom=list(map(float, data.Y_wl)), color='antiquewhite', label='Potential yield', zorder=3)
ax1.bar(range(len(data.CropFieldID)), list(map(float, (data.Y_wl-data.Y_wnl))), width_barplot, edgecolor='goldenrod', bottom=list(map(float, data.Y_wnl)), color='gold', label='Water limited yield', zorder=3)
ax1.bar(range(len(data.CropFieldID)), list(map(float, (data.Y_wnl-data.Y_obs))), width_barplot, edgecolor='orangered', bottom=list(map(float, data.Y_obs)), color='orange', label='Water & N limited yield', zorder=3)
ax1.bar(range(len(data.CropFieldID)), list(map(float, data.Y_obs)), width_barplot, edgecolor='darkblue', color='cornflowerblue', label='Actual yield', zorder=3)
ax1.set_xticks(range(len(data.CropFieldID)))
ax1.set_xticklabels('', rotation=90, family='sans-serif', fontsize=16, color='black')
ax1.set_yticks([0, 2, 4, 6, 8, 10, 12, 14])
ax1.set_yticklabels([0, 2, 4, 6, 8, 10, 12, 14], family='sans-serif', fontsize=16, color='black')
ax1.set_ylim([0, 14])
ax1.set_facecolor('white')
ax1.legend(loc='lower right', fontsize=15)
# ax1.axhline(data.Y_pp.mean()/1000, color='black', linestyle='-', zorder=5)
# ax1.axhline(data.Y_wl.mean()/1000, color='black', linestyle='--', zorder=5)
# ax1.axhline(data.Y_wnl.mean()/1000, color='black', linestyle='-.', zorder=5)
# ax1.axhline(data.Y_obs.mean()/1000, color='black', linestyle=':', zorder=5)

data = data.sort_values("ya_perc", axis=0, ascending=False)
ax2.set_ylabel('Wheat yield gap closure (% of Yp)', family='sans-serif', fontsize=17, color='black')
ax2.set_xlabel('Unique farm-field ID', family='sans-serif', fontsize=17, color='black')
ax2.grid(axis='y', linestyle='-', color='gainsboro')
ax2.bar(range(len(data.CropFieldID)), list(map(float, (100-data.yw_perc))), width_barplot, edgecolor='tan', bottom=list(map(float, data.yw_perc)), color='antiquewhite', label='Potential yield', zorder=3)
ax2.bar(range(len(data.CropFieldID)), list(map(float, (data.yw_perc-data.ywn_perc))), width_barplot, edgecolor='goldenrod', bottom=list(map(float, data.ywn_perc)), color='gold', label='Water limited yield', zorder=3)
ax2.bar(range(len(data.CropFieldID)), list(map(float, (data.ywn_perc-data.ya_perc))), width_barplot, edgecolor='orangered', bottom=list(map(float, data.ya_perc)), color='orange', label='Water & N limited yield', zorder=3)
ax2.bar(range(len(data.CropFieldID)), list(map(float, data.ya_perc)), width_barplot, edgecolor='darkblue', color='cornflowerblue', label='Actual yield', zorder=3)
ax2.set_xticks(range(len(data.CropFieldID)))
ax2.set_xticklabels('', rotation=90, family='sans-serif', fontsize=16, color='black')
ax2.set_yticks([0, 20, 40, 60, 80, 100])
ax2.set_yticklabels([0, 20, 40, 60, 80, 100], family='sans-serif', fontsize=16, color='black')
ax2.set_ylim([0, 100])
ax2.set_facecolor('white')
ax2.legend(loc='lower right', fontsize=15)
ax2.axhline(80, color='black', zorder=5)
ax2.axhline(data.ya_perc.mean(), color='black', linestyle='--', zorder=5)

f.savefig(os.path.join(dir, r".\figure4-wheat-yield-gaps.png"), bbox_inches='tight')
plt.gcf().clear()

# ----------------------------------------------------------------------------------------------------------------------
# YIELD GAPS SUMMARY ---------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

new_data = data.groupby(['yield_class'])['Y_obs', 'Y_wnl', 'Y_wl', 'Y_pp', 'ya_perc', 'ywn_perc', 'yw_perc'].mean().reset_index()
# print(new_data.to_string())
# new_data['water_stress'] = new_data.Y_pp - new_data.Y_wl
# new_data['water_stress'] = 100 - new_data.yw_perc
# new_data['n_stress'] = new_data.Y_wl - new_data.Y_wnl
# new_data['n_stress'] = new_data.yw_perc - new_data.ywn_perc
# new_data['other_stress'] = new_data.Y_wnl - new_data.Y_obs
# new_data['other_stress'] = new_data.ywn_perc - new_data.ya_perc

left, width = .215, .71
bottom, height = .25, .71
right = left + width
top = bottom + height
wspace = 0.25
hspace = 0.10
kws_points = dict(s=80, alpha=0.8, linewidth=0.7)
width_barplot = 0.75

f, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12.3, 5.4))
axes = plt.gca()
f.subplots_adjust(wspace=wspace, hspace=hspace)

new_data = new_data.sort_values("Y_obs", axis=0, ascending=False)
ax1.set_ylabel('Wheat yield & yield gap (t/ha)', family='sans-serif', fontsize=15, color='black')
ax1.set_xlabel('', family='sans-serif', fontsize=17, color='black')
ax1.grid(axis='y', linestyle='-', color='gainsboro')
ax1.bar(range(len(new_data.yield_class)), list(map(float, (new_data.Y_pp-new_data.Y_wl))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.Y_wl)), color='antiquewhite', label='Potential yield', zorder=3)
ax1.bar(range(len(new_data.yield_class)), list(map(float, (new_data.Y_wl-new_data.Y_wnl))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.Y_wnl)), color='gold', label='Water limited yield', zorder=3)
ax1.bar(range(len(new_data.yield_class)), list(map(float, (new_data.Y_wnl-new_data.Y_obs))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.Y_obs)), color='orange', label='Water & N limited yield', zorder=3)
ax1.bar(range(len(new_data.yield_class)), list(map(float, new_data.Y_obs)), width_barplot, edgecolor='black', color='cornflowerblue', label='Actual yield', zorder=3)
ax1.set_xticks(range(len(new_data.yield_class)))
ax1.set_yticks([0, 2, 4, 6, 8, 10, 12, 14])
ax1.set_yticklabels([0, 2, 4, 6, 8, 10, 12, 14], family='sans-serif', fontsize=14, color='black')
ax1.set_xticklabels(['Highest\nyielding\nfields', 'Average\nyielding\nfields', 'Lowest\nyielding\nfields'], family='sans-serif', fontsize=14, color='black')
ax1.set_ylim([0, 14])
ax1.set_facecolor('white')
# ax1.axhline(data.Y_pp.mean(), color='black', linestyle='-', zorder=5)
# ax1.axhline(data.Y_wl.mean(), color='black', linestyle='--', zorder=5)
# ax1.axhline(data.Y_wnl.mean(), color='black', linestyle='-.', zorder=5)
# ax1.axhline(data.Y_obs.mean(), color='black', linestyle=':', zorder=5)
ax1.set_title('A)', x=0.095, y=0.91, fontsize=16, fontweight='bold')

new_data = new_data.sort_values("ya_perc", axis=0, ascending=False)
ax2.set_ylabel('Wheat yield gap closure (% of Yp)', family='sans-serif', fontsize=15, color='black')
ax2.set_xlabel('', family='sans-serif', fontsize=17, color='black')
ax2.grid(axis='y', linestyle='-', color='gainsboro')
ax2.bar(range(len(new_data.yield_class)), list(map(float, (100-new_data.yw_perc))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.yw_perc)), color='antiquewhite', label='Potential yield', zorder=3)
ax2.bar(range(len(new_data.yield_class)), list(map(float, (new_data.yw_perc-new_data.ywn_perc))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.ywn_perc)), color='gold', label='Water limited yield', zorder=3)
ax2.bar(range(len(new_data.yield_class)), list(map(float, (new_data.ywn_perc-new_data.ya_perc))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.ya_perc)), color='orange', label='Water & N limited yield', zorder=3)
ax2.bar(range(len(new_data.yield_class)), list(map(float, new_data.ya_perc)), width_barplot, edgecolor='black', color='cornflowerblue', label='Actual yield', zorder=3)
ax2.set_xticks(range(len(new_data.yield_class)))
ax2.set_xticklabels(['Highest\nyielding\nfields', 'Average\nyielding\nfields', 'Lowest\nyielding\nfields'], family='sans-serif', fontsize=14, color='black')
ax2.set_yticks([0, 20, 40, 60, 80, 100])
ax2.set_yticklabels([0, 20, 40, 60, 80, 100], family='sans-serif', fontsize=14, color='black')
ax2.set_ylim([0, 100])
ax2.set_facecolor('white')
ax2.legend(loc='lower right', fontsize=12)
ax2.axhline(80, color='black', zorder=5)
ax2.patch.set_edgecolor('black')
ax2.set_title('B)', x=0.095, y=0.91, fontsize=16, fontweight='bold')

f.savefig(os.path.join(dir, r".\figure4-wheat-yield-gaps-new.png"), bbox_inches='tight', dpi=1000)
plt.gcf().clear()

# ----------------------------------------------------------------------------------------------------------------------
# YIELD GAPS SUMMARY ---------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

new_data = data.groupby(['year'])['Y_obs', 'Y_wnl', 'Y_wl', 'Y_pp', 'ya_perc', 'ywn_perc', 'yw_perc'].mean().reset_index()
# print(new_data.to_string())
# new_data['water_stress'] = new_data.Y_pp - new_data.Y_wl
# new_data['water_stress'] = 100 - new_data.yw_perc
# new_data['n_stress'] = new_data.Y_wl - new_data.Y_wnl
# new_data['n_stress'] = new_data.yw_perc - new_data.ywn_perc
# new_data['other_stress'] = new_data.Y_wnl - new_data.Y_obs
# new_data['other_stress'] = new_data.ywn_perc - new_data.ya_perc

left, width = .215, .71
bottom, height = .25, .71
right = left + width
top = bottom + height
wspace = 0.25
hspace = 0.10
kws_points = dict(s=80, alpha=0.8, linewidth=0.7)
width_barplot = 0.75

f, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12.3, 5.4))
axes = plt.gca()
f.subplots_adjust(wspace=wspace, hspace=hspace)

new_data = new_data.sort_values("year", axis=0, ascending=False)
ax1.set_ylabel('Wheat yield & yield gap (t/ha)', family='sans-serif', fontsize=15, color='black')
ax1.set_xlabel('', family='sans-serif', fontsize=17, color='black')
ax1.grid(axis='y', linestyle='-', color='gainsboro')
ax1.bar(range(len(new_data.year)), list(map(float, (new_data.Y_pp-new_data.Y_wl))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.Y_wl)), color='antiquewhite', label='Yg due to water stress (Yp-Yw)', zorder=3)
ax1.bar(range(len(new_data.year)), list(map(float, (new_data.Y_wl-new_data.Y_wnl))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.Y_wnl)), color='gold', label='Yg due to N stress (Yw-Ywn)', zorder=3)
ax1.bar(range(len(new_data.year)), list(map(float, (new_data.Y_wnl-new_data.Y_obs))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.Y_obs)), color='orange', label='Yg due to other factors (Ywn-Ya)', zorder=3)
ax1.bar(range(len(new_data.year)), list(map(float, new_data.Y_obs)), width_barplot, edgecolor='black', color='cornflowerblue', label='Actual yield (Ya)', zorder=3)
ax1.set_xticks(range(len(new_data.year)))
ax1.set_yticks([0, 2, 4, 6, 8, 10, 12, 14])
ax1.set_yticklabels([0, 2, 4, 6, 8, 10, 12, 14], family='sans-serif', fontsize=14, color='black')
ax1.set_xticklabels(['2015', '2016', '2017'], family='sans-serif', fontsize=14, color='black')
ax1.set_ylim([0, 14])
ax1.set_facecolor('white')
# ax1.axhline(data.Y_pp.mean(), color='black', linestyle='-', zorder=5)
# ax1.axhline(data.Y_wl.mean(), color='black', linestyle='--', zorder=5)
# ax1.axhline(data.Y_wnl.mean(), color='black', linestyle='-.', zorder=5)
# ax1.axhline(data.Y_obs.mean(), color='black', linestyle=':', zorder=5)
ax1.set_title('A)', x=0.095, y=0.91, fontsize=16, fontweight='bold')

new_data = new_data.sort_values("year", axis=0, ascending=False)
ax2.set_ylabel('Wheat yield gap closure (% of Yp)', family='sans-serif', fontsize=15, color='black')
ax2.set_xlabel('', family='sans-serif', fontsize=17, color='black')
ax2.grid(axis='y', linestyle='-', color='gainsboro')
ax2.bar(range(len(new_data.year)), list(map(float, (100-new_data.yw_perc))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.yw_perc)), color='antiquewhite', label='Yg due to water stress (Yp-Yw)', zorder=3)
ax2.bar(range(len(new_data.year)), list(map(float, (new_data.yw_perc-new_data.ywn_perc))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.ywn_perc)), color='gold', label='Yg due to N stress (Yw-Ywn)', zorder=3)
ax2.bar(range(len(new_data.year)), list(map(float, (new_data.ywn_perc-new_data.ya_perc))), width_barplot, edgecolor='black', bottom=list(map(float, new_data.ya_perc)), color='orange', label='Yg due to other factors (Ywn-Ya)', zorder=3)
ax2.bar(range(len(new_data.year)), list(map(float, new_data.ya_perc)), width_barplot, edgecolor='black', color='cornflowerblue', label='Actual yield (Ya)', zorder=3)
ax2.set_xticks(range(len(new_data.year)))
ax2.set_xticklabels(['2015', '2016', '2017'], family='sans-serif', fontsize=14, color='black')
ax2.set_yticks([0, 20, 40, 60, 80, 100])
ax2.set_yticklabels([0, 20, 40, 60, 80, 100], family='sans-serif', fontsize=14, color='black')
ax2.set_ylim([0, 100])
ax2.set_facecolor('white')
ax2.legend(loc='lower right', fontsize=12)
ax2.axhline(80, color='black', zorder=5)
ax2.patch.set_edgecolor('black')
ax2.set_title('B)', x=0.095, y=0.91, fontsize=16, fontweight='bold')

f.savefig(os.path.join(dir, r".\figure4-wheat-yield-gaps-new2.png"), bbox_inches='tight', dpi=1000)
plt.gcf().clear()

# ----------------------------------------------------------------------------------------------------------------------
# THE END --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
