# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

yp_dir = r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\4-hberghuijs-model--final\output"
co2_dir = r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\4-hberghuijs-model--final\output\co2-check"

# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------

for soil in ['clay']:
    for yld in ['yp']:

        # plot data
        left, width = .255, .71
        bottom, height = .25, .71
        right = left + width
        top = bottom + height
        wspace = 0.25
        hspace = 0.25
        kws_points = dict(s=100, alpha=0.9, linewidth=0.7)
        f, ((ax1, ax3, ax5), (ax2, ax4, ax6)) = plt.subplots(2, 3, figsize=(18, 11.5))
        axes = plt.gca()
        f.subplots_adjust(wspace=wspace, hspace=hspace)

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        s = 'EELDE'
        # simulated yp
        path = os.path.join(yp_dir, f".\yp-long-term-summary-{s}-co2-{soil}.xlsx")
        yp = pd.read_excel(path)
        yp['DOM'] = pd.to_datetime(yp['DOM'])
        yp['year'] = yp['DOM'].dt.year
        yp['yield_tha'] = yp['TWSO'] / 1000
        # 360 ppm
        path = os.path.join(co2_dir, f".\yp-long-term-summary-{s}-360.xlsx")
        low_co2 = pd.read_excel(path)
        low_co2['DOM'] = pd.to_datetime(low_co2['DOM'])
        low_co2['year'] = low_co2['DOM'].dt.year
        low_co2['yield_tha'] = low_co2['TWSO'] / 1000
        # 400 ppm
        path = os.path.join(co2_dir, f".\yp-long-term-summary-{s}-400.xlsx")
        high_co2 = pd.read_excel(path)
        high_co2['DOM'] = pd.to_datetime(high_co2['DOM'])
        high_co2['year'] = high_co2['DOM'].dt.year
        high_co2['yield_tha'] = high_co2['TWSO'] / 1000
        # --------------------------------------------------------------------------------------------------------------
        ax1.grid(linestyle='-', zorder=0, color='gainsboro')
        # ----------
        # CO2 effect
        y = yp.yield_tha
        ax1.plot(yp.year, yp.yield_tha, color='darkblue', zorder=2)
        ax1.scatter(yp.year, yp.yield_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yearly CO2')
        X = yp[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(yp[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(yp[["year"]].dropna()))
        slope_yp_eelde = linr_model.coef_[0].round(3)
        ax1.plot(yp.year, linr_model.predict(yp[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='-', zorder=5)
        # -------
        # 360 ppm
        y = low_co2.yield_tha
        ax1.plot(low_co2.year, low_co2.yield_tha, color='orangered', zorder=2)
        ax1.scatter(low_co2.year, low_co2.yield_tha, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='360 ppm')
        X = low_co2[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(low_co2[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(low_co2[["year"]].dropna()))
        slope_yp_eelde = linr_model.coef_[0].round(3)
        ax1.plot(low_co2.year, linr_model.predict(low_co2[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='--', zorder=5)
        ax1.set_ylim([7, 14])
        ax1.set_xlim([1970, 2020])
        ax1.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax1.set_yticklabels([7, 8, 9, 10, 11, 12, 13, 14], fontsize=14.5)
        ax1.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax1.set_facecolor('white')
        ax1.legend(loc='lower right', ncol=1, fontsize=11)
        ax1.set_title('A) Northeast', x=0.22, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        ax2.grid(linestyle='-', zorder=0, color='gainsboro')
        # ----------
        # CO2 effect
        y = yp.yield_tha
        ax2.plot(yp.year, yp.yield_tha, color='darkblue', zorder=2)
        ax2.scatter(yp.year, yp.yield_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yearly CO2')
        X = yp[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(yp[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(yp[["year"]].dropna()))
        slope_yp_eelde = linr_model.coef_[0].round(3)
        ax2.plot(yp.year, linr_model.predict(yp[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='-', zorder=5)
        # -------
        # 400 ppm
        y = high_co2.yield_tha
        ax2.plot(high_co2.year, high_co2.yield_tha, color='orangered', zorder=2)
        ax2.scatter(high_co2.year, high_co2.yield_tha, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='400 ppm')
        X = high_co2[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(high_co2[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(high_co2[["year"]].dropna()))
        slope_yp_eelde = linr_model.coef_[0].round(3)
        ax2.plot(high_co2.year, linr_model.predict(high_co2[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='--', zorder=5)
        ax2.set_ylim([7, 14])
        ax2.set_xlim([1970, 2020])
        ax2.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax2.set_yticklabels([7, 8, 9, 10, 11, 12, 13, 14], fontsize=14.5)
        ax2.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax2.set_facecolor('white')
        ax2.legend(loc='lower right', ncol=1, fontsize=11)
        ax2.set_title('D) Northeast', x=0.22, y=0.9, fontsize=16, fontweight='bold')

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        s = 'DE BILT'
        # simulated yp
        path = os.path.join(yp_dir, f".\yp-long-term-summary-{s}-co2-{soil}.xlsx")
        yp = pd.read_excel(path)
        yp['DOM'] = pd.to_datetime(yp['DOM'])
        yp['year'] = yp['DOM'].dt.year
        yp['yield_tha'] = yp['TWSO'] / 1000
        # 360 ppm
        path = os.path.join(co2_dir, f".\yp-long-term-summary-{s}-360.xlsx")
        low_co2 = pd.read_excel(path)
        low_co2['DOM'] = pd.to_datetime(low_co2['DOM'])
        low_co2['year'] = low_co2['DOM'].dt.year
        low_co2['yield_tha'] = low_co2['TWSO'] / 1000
        # 400 ppm
        path = os.path.join(co2_dir, f".\yp-long-term-summary-{s}-400.xlsx")
        high_co2 = pd.read_excel(path)
        high_co2['DOM'] = pd.to_datetime(high_co2['DOM'])
        high_co2['year'] = high_co2['DOM'].dt.year
        high_co2['yield_tha'] = high_co2['TWSO'] / 1000
        # --------------------------------------------------------------------------------------------------------------
        ax3.grid(linestyle='-', zorder=0, color='gainsboro')
        # ----------
        # CO2 effect
        y = yp.yield_tha
        ax3.plot(yp.year, yp.yield_tha, color='darkblue', zorder=2)
        ax3.scatter(yp.year, yp.yield_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yearly CO2')
        X = yp[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(yp[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(yp[["year"]].dropna()))
        slope_yp_debilt = linr_model.coef_[0].round(3)
        ax3.plot(yp.year, linr_model.predict(yp[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_debilt, int=abs(linr_model.intercept_).round(1)), linestyle='-', zorder=5)
        # -------
        # 360 ppm
        y = low_co2.yield_tha
        ax3.plot(low_co2.year, low_co2.yield_tha, color='orangered', zorder=2)
        ax3.scatter(low_co2.year, low_co2.yield_tha, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='360 ppm')
        X = low_co2[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(low_co2[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(low_co2[["year"]].dropna()))
        slope_yp_eelde = linr_model.coef_[0].round(3)
        ax3.plot(low_co2.year, linr_model.predict(low_co2[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='--', zorder=5)
        ax3.set_ylim([7, 14])
        ax3.set_xlim([1970, 2020])
        ax3.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax3.set_yticklabels([7, 8, 9, 10, 11, 12, 13, 14], fontsize=14.5)
        ax3.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax3.set_facecolor('white')
        ax3.legend(loc='lower right', ncol=1, fontsize=11)
        ax3.set_title('B) Central', x=0.18, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        ax4.grid(linestyle='-', zorder=0, color='gainsboro')
        # ----------
        # CO2 effect
        y = yp.yield_tha
        ax4.plot(yp.year, yp.yield_tha, color='darkblue', zorder=2)
        ax4.scatter(yp.year, yp.yield_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yearly CO2')
        X = yp[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(yp[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(yp[["year"]].dropna()))
        slope_yp_debilt = linr_model.coef_[0].round(3)
        ax4.plot(yp.year, linr_model.predict(yp[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_debilt, int=abs(linr_model.intercept_).round(1)), linestyle='-', zorder=5)
        # -------
        # 400 ppm
        y = high_co2.yield_tha
        ax4.plot(high_co2.year, high_co2.yield_tha, color='orangered', zorder=2)
        ax4.scatter(high_co2.year, high_co2.yield_tha, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='400 ppm')
        X = high_co2[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(high_co2[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(high_co2[["year"]].dropna()))
        slope_yp_eelde = linr_model.coef_[0].round(3)
        ax4.plot(high_co2.year, linr_model.predict(high_co2[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='--', zorder=5)
        ax4.set_ylim([7, 14])
        ax4.set_xlim([1970, 2020])
        ax4.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax4.set_yticklabels([7, 8, 9, 10, 11, 12, 13, 14], fontsize=14.5)
        ax4.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax4.set_facecolor('white')
        ax4.legend(loc='lower right', ncol=1, fontsize=11)
        ax4.set_title('E) Central', x=0.18, y=0.9, fontsize=16, fontweight='bold')

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        s = 'VLISSINGEN'
        # simulated yp
        path = os.path.join(yp_dir, f".\yp-long-term-summary-{s}-co2-{soil}.xlsx")
        yp = pd.read_excel(path)
        yp['DOM'] = pd.to_datetime(yp['DOM'])
        yp['year'] = yp['DOM'].dt.year
        yp['yield_tha'] = yp['TWSO'] / 1000
        # 360 ppm
        path = os.path.join(co2_dir, f".\yp-long-term-summary-{s}-360.xlsx")
        low_co2 = pd.read_excel(path)
        low_co2['DOM'] = pd.to_datetime(low_co2['DOM'])
        low_co2['year'] = low_co2['DOM'].dt.year
        low_co2['yield_tha'] = low_co2['TWSO'] / 1000
        # 400 ppm
        path = os.path.join(co2_dir, f".\yp-long-term-summary-{s}-400.xlsx")
        high_co2 = pd.read_excel(path)
        high_co2['DOM'] = pd.to_datetime(high_co2['DOM'])
        high_co2['year'] = high_co2['DOM'].dt.year
        high_co2['yield_tha'] = high_co2['TWSO'] / 1000
        # --------------------------------------------------------------------------------------------------------------
        ax5.grid(linestyle='-', zorder=0, color='gainsboro')
        # ----------
        # CO2 effect
        y = yp.yield_tha
        ax5.plot(yp.year, yp.yield_tha, color='darkblue', zorder=2)
        ax5.scatter(yp.year, yp.yield_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yearly CO2')
        X = yp[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(yp[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(yp[["year"]].dropna()))
        slope_yp_vlissingen = linr_model.coef_[0].round(3)
        ax5.plot(yp.year, linr_model.predict(yp[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_vlissingen, int=abs(linr_model.intercept_).round(1)), linestyle='-', zorder=5)
        # -------
        # 360 ppm
        y = low_co2.yield_tha
        ax5.plot(low_co2.year, low_co2.yield_tha, color='orangered', zorder=2)
        ax5.scatter(low_co2.year, low_co2.yield_tha, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='360 ppm')
        X = low_co2[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(low_co2[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(low_co2[["year"]].dropna()))
        slope_yp_eelde = linr_model.coef_[0].round(3)
        ax5.plot(low_co2.year, linr_model.predict(low_co2[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='--', zorder=5)
        ax5.set_ylim([7, 14])
        ax5.set_xlim([1970, 2020])
        ax5.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax5.set_yticklabels([7, 8, 9, 10, 11, 12, 13, 14], fontsize=14.5)
        ax5.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax5.set_facecolor('white')
        ax5.legend(loc='lower right', ncol=1, fontsize=11)
        ax5.set_title('C) Southwest', x=0.23, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        ax6.grid(linestyle='-', zorder=0, color='gainsboro')
        # ----------
        # CO2 effect
        y = yp.yield_tha
        ax6.plot(yp.year, yp.yield_tha, color='darkblue', zorder=2)
        ax6.scatter(yp.year, yp.yield_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yearly CO2')
        X = yp[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(yp[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(yp[["year"]].dropna()))
        slope_yp_vlissingen = linr_model.coef_[0].round(3)
        ax6.plot(yp.year, linr_model.predict(yp[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_vlissingen, int=abs(linr_model.intercept_).round(1)), linestyle='-', zorder=5)
        # -------
        # 400 ppm
        y = high_co2.yield_tha
        ax6.plot(high_co2.year, high_co2.yield_tha, color='orangered', zorder=2)
        ax6.scatter(high_co2.year, high_co2.yield_tha, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='400 ppm')
        X = high_co2[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(high_co2[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(high_co2[["year"]].dropna()))
        slope_yp_eelde = linr_model.coef_[0].round(3)
        ax6.plot(high_co2.year, linr_model.predict(high_co2[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='--', zorder=5)
        ax6.set_ylim([7, 14])
        ax6.set_xlim([1970, 2020])
        ax6.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax6.set_yticklabels([7, 8, 9, 10, 11, 12, 13, 14], fontsize=14.5)
        ax6.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax6.set_facecolor('white')
        ax6.legend(loc='lower right', ncol=1, fontsize=11)
        ax6.set_title('F) Southwest', x=0.23, y=0.9, fontsize=16, fontweight='bold')

        # ------------------------------------------------------------------------------------------------------------------
        f.savefig(os.path.join(yp_dir, f"figure1-wheat-trends-{yld}-co2.png"), bbox_inches='tight', dpi=1000)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
