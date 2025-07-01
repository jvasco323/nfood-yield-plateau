# ----------------------------------------------------------------------------------------------------------------------
# general packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ----------------------------------------------------------------------------------------------------------------------
# working directories

input_dir = r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\1-calibration-jsilva-files\Data Input\WOFOST Inputs"
output_dir = r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\4-hberghuijs-model--final\output"

# ----------------------------------------------------------------------------------------------------------------------
# load data

stations = ['DE BILT', 'EELDE', 'VLISSINGEN']
for s in stations:

    weather = pd.read_excel(os.path.join(input_dir, f".\KNMI Weather\# WOFOST_Weather_KNMI_{s}_ANALYSIS.xlsx"))
    weather['DAY'] = pd.to_datetime(weather['DAY'])
    weather['year'] = weather['DAY'].dt.year
    weather['month'] = weather['DAY'].dt.month
    wheat_months = weather[(weather.month > 1) & (weather.month < 9)]

# ------------------------------------------------------------------------------------------------------------------
    # group by month

    average = wheat_months.groupby(['month'])['TMAX', 'TMIN'].mean().round(2).reset_index()
    average_wheat = average.transpose().drop(index='month')
    average_wheat = average_wheat.rename(columns={0: 'February', 1: 'March', 2: 'April', 3: 'May', 4: 'June', 5: 'July', 6: 'August'})
    sum = wheat_months.groupby(['month', 'year'])['IRRAD', 'RAIN'].sum().round(2).reset_index()
    sum = sum.groupby(['month'])['IRRAD', 'RAIN'].mean().round(2).reset_index()
    sum['IRRAD'] = sum['IRRAD']/1000
    sum['IRRAD'] = sum['IRRAD'].round(2)
    sum_wheat = sum.transpose().drop(index='month')
    sum_wheat = sum_wheat.rename(columns={0: 'February', 1: 'March', 2: 'April', 3: 'May', 4: 'June', 5: 'July', 6: 'August'})
    wheat_final = average_wheat.append(sum_wheat)
    wheat_final.to_csv(os.path.join(output_dir, r".\weather-summary-{s}.csv".format(s=s)))

    # ------------------------------------------------------------------------------------------------------------------
    # group by year

    average = wheat_months.groupby(['year'])['TMAX', 'TMIN'].mean().round(2).reset_index()
    average_wheat = average.transpose().drop(index='year')
    sum = wheat_months.groupby(['year'])['IRRAD', 'RAIN'].sum().round(2).reset_index()
    sum = sum.groupby(['year'])['IRRAD', 'RAIN'].mean().round(2).reset_index()
    sum['IRRAD'] = sum['IRRAD']/1000
    sum['IRRAD'] = sum['IRRAD'].round(2)
    sum_wheat = sum.transpose().drop(index='year')
    wheat_final = average_wheat.append(sum_wheat)
    wheat_final.to_csv(os.path.join(output_dir, f".\weather-summary-year-{s}.csv"))

    # ------------------------------------------------------------------------------------------------------------------
    # group by year for months < 8

    left, width = .255, .71
    bottom, height = .25, .71
    right = left + width
    top = bottom + height
    wspace = 0.25
    hspace = 0.25
    kws_points = dict(s=100, alpha=0.9, linewidth=0.7)
    # ------------------------------------------------------------------------------------------------------------------
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 6))
    axes = plt.gca()
    f.subplots_adjust(wspace=wspace, hspace=hspace)
    # ------------------------------------------------------------------------------------------------------------------
    ax1.grid(linestyle='-', linewidth=0.5, zorder=0)
    average = wheat_months.groupby(['year'])['TMAX', 'TMIN'].mean().round(2).reset_index()
    y = average.TMAX.dropna()
    X = average[["year"]].dropna()
    linr_model = LinearRegression().fit(X, y)
    linr_model.coef_
    linr_model.intercept_
    linr_model.predict(average[["year"]].dropna())
    r2 = r2_score(y_true=average.TMAX.dropna(), y_pred=linr_model.predict(average[["year"]].dropna()))
    ax1.plot(average.year, average.TMAX, color='orangered', zorder=3, label='')
    ax1.scatter(average.year, average.TMAX, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=4, label='TMAX')
    ax1.plot(average.year, linr_model.predict(average[["year"]]), color="black", label='R2={r2}'.format(r2=r2.round(2)), linestyle='--', zorder=5)
    ax1.text(left + 0.675, bottom + 0.5, '{coef} degC/yr'.format(coef=linr_model.coef_[0].round(3)), color='orangered',
             horizontalalignment='right', verticalalignment='top', transform=ax1.transAxes, family='sans-serif', fontsize=17)
    y = average.TMIN.dropna()
    X = average[["year"]].dropna()
    linr_model = LinearRegression().fit(X, y)
    linr_model.coef_
    linr_model.intercept_
    linr_model.predict(average[["year"]].dropna())
    r2 = r2_score(y_true=average.TMIN.dropna(), y_pred=linr_model.predict(average[["year"]].dropna()))
    ax1.plot(average.year, average.TMIN, color='darkblue', zorder=2, label='')
    ax1.scatter(average.year, average.TMIN, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='TMIN')
    ax1.plot(average.year, linr_model.predict(average[["year"]]), color="black", label='R2={r2}'.format(r2=r2.round(2)), linestyle='-', zorder=5)
    ax1.text(left + 0.675, bottom + 0.025, '{coef} degC/yr'.format(coef=linr_model.coef_[0].round(3)), color='darkblue',
         horizontalalignment='right', verticalalignment='top', transform=ax1.transAxes, family='sans-serif', fontsize=17)
    ax1.set_ylim([0, 20])
    ax1.set_xlim([1970, 2020])
    ax1.set_yticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
    ax1.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15)
    ax1.set_yticklabels([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20], fontsize=14)
    ax1.set_ylabel('Temperature (degrees C)', fontsize=15)
    ax1.set_facecolor('whitesmoke')
    ax1.legend(loc='lower right', ncol=2, fontsize=12)
    # x = average.year
    # y = average.TMAX
    # p = np.polyfit(x, y, deg=1)
    # x = average.year
    # y = p[1] + p[0] * average.year
    # ax1.plot(x, y, '-', color='black', zorder=5)
    # x = average.year
    # y = average.TMIN
    # p = np.polyfit(x, y, deg=1)
    # x = average.year
    # y = p[1] + p[0] * average.year
    # ax1.plot(x, y, '--', color='black', zorder=5)
    # ------------------------------------------------------------------------------------------------------------------
    ax2.grid(linestyle='-', linewidth=0.5, zorder=0)
    sum = wheat_months.groupby(['year'])['IRRAD', 'RAIN'].sum().round(2).reset_index()
    y = sum.IRRAD/1000
    X = sum[["year"]].dropna()
    linr_model = LinearRegression().fit(X, y)
    linr_model.coef_
    linr_model.intercept_
    linr_model.predict(average[["year"]].dropna())
    r2 = r2_score(y_true=sum.IRRAD/1000, y_pred=linr_model.predict(average[["year"]].dropna()))
    ax2.plot(sum.year, sum.IRRAD/1000, color='orangered', zorder=2, label='')
    ax2.scatter(sum.year, sum.IRRAD/1000, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Solar radiation')
    ax2.plot(sum.year, linr_model.predict(sum[["year"]]), color="black", label='R2={r2}'.format(r2=r2.round(2)), linestyle='--', zorder=5)
    ax2.text(left + 0.675, bottom + 0.515, '{coef} MJ/m2/yr'.format(coef=linr_model.coef_[0].round(1)), color='orangered',
             horizontalalignment='right', verticalalignment='top', transform=ax2.transAxes, family='sans-serif', fontsize=17)
    ax2.set_ylim([0, 3500])
    ax2.set_xlim([1970, 2020])
    ax2.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15)
    ax2.set_yticklabels([0, 500, 1000, 1500, 2000, 2500, 3000, 3500], fontsize=14)
    ax2.set_ylabel('Solar radiation (MJ/m2)', fontsize=15)
    ax2.legend(loc='lower right', ncol=1, fontsize=12)

    co2 = pd.read_excel(r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\1-calibration-jsilva-files\Data Input\Weather Data\CO2_NOAA.xlsx")
    co2 = co2[(co2.year > 1969) & (co2.year < 2018)]
    ax3 = ax2.twinx()
    ax3.plot(co2.year, co2['mean'], color='darkblue', zorder=2, label='')
    ax3.scatter(co2.year, co2['mean'], color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Atmospheric CO2')
    y = co2['mean']
    X = co2[["year"]].dropna()
    linr_model = LinearRegression().fit(X, y)
    linr_model.coef_
    linr_model.intercept_
    ax3.plot(co2.year, linr_model.predict(co2[["year"]]), color="black", label='R2={r2}'.format(r2=r2.round(2)),
         linestyle='-', zorder=5)
    ax2.text(left + 0.675, bottom + 0.155, '{coef} ppm/yr'.format(coef=linr_model.coef_[0].round(1)), color='darkblue',
         horizontalalignment='right', verticalalignment='top', transform=ax2.transAxes, family='sans-serif', fontsize=17)
    ax3.set_ylim([300, 475])
    ax3.set_yticks([300, 325, 350, 375, 400, 425, 450, 475])
    ax3.set_yticklabels([300, 325, 350, 375, 400, 425, 450, 475], fontsize=14)
    ax3.set_ylabel('Atmospheric CO2 concentration (ppm)', rotation=-90, fontsize=15, labelpad=17)
    ax3.legend(loc='lower right', ncol=1, fontsize=12, bbox_to_anchor=(1, 0.125))
    ax2.set_facecolor('whitesmoke')
    # x = sum.year
    # y = sum.IRRAD/1000
    # p = np.polyfit(x, y, deg=1)
    # x = sum.year
    # y = p[1] + p[0] * sum.year
    # ax2.plot(x, y, '-', color='black', zorder=5)
    # ------------------------------------------------------------------------------------------------------------------
    f.savefig(os.path.join(output_dir, f".\weather-analysis-{s}.pdf"), bbox_inches='tight')

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
