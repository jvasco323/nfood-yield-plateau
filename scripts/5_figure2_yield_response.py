# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

dir = r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\4-hberghuijs-model--final\output"

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

for soil in ['clay', 'sand']:
    for yld in ['yp', 'yw']:

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # summary data

        # de bilt
        summary_debilt = pd.read_excel(os.path.join(dir, f"{yld}-long-term-summary-DE BILT-co2-{soil}.xlsx"))
        summary_debilt['DOA'] = pd.to_datetime(summary_debilt['DOA'])
        summary_debilt['DOA'] = summary_debilt['DOA'].dt.dayofyear
        summary_debilt['DOM'] = pd.to_datetime(summary_debilt['DOM'])
        summary_debilt['year'] = summary_debilt['DOM'].dt.year
        summary_debilt['month'] = summary_debilt['DOM'].dt.month
        summary_debilt['yp'] = summary_debilt['TWSO']/1000
        summary_debilt['hi'] = 100 * summary_debilt['TWSO']/summary_debilt['TAGP']
        # eelde
        summary_eelde = pd.read_excel(os.path.join(dir, f"{yld}-long-term-summary-EELDE-co2-{soil}.xlsx"))
        summary_eelde['DOA'] = pd.to_datetime(summary_eelde['DOA'])
        summary_eelde['DOA'] = summary_eelde['DOA'].dt.dayofyear
        summary_eelde['DOM'] = pd.to_datetime(summary_eelde['DOM'])
        summary_eelde['year'] = summary_eelde['DOM'].dt.year
        summary_eelde['month'] = summary_eelde['DOM'].dt.month
        summary_eelde['yp'] = summary_eelde['TWSO']/1000
        summary_eelde['hi'] = 100 * summary_eelde['TWSO']/summary_eelde['TAGP']
        # vlissingen
        summary_vlissingen = pd.read_excel(os.path.join(dir, f"{yld}-long-term-summary-VLISSINGEN-co2-{soil}.xlsx"))
        summary_vlissingen['DOA'] = pd.to_datetime(summary_vlissingen['DOA'])
        summary_vlissingen['DOA'] = summary_vlissingen['DOA'].dt.dayofyear
        summary_vlissingen['DOM'] = pd.to_datetime(summary_vlissingen['DOM'])
        summary_vlissingen['year'] = summary_vlissingen['DOM'].dt.year
        summary_vlissingen['month'] = summary_vlissingen['DOM'].dt.month
        summary_vlissingen['yp'] = summary_vlissingen['TWSO']/1000
        summary_vlissingen['hi'] = 100 * summary_vlissingen['TWSO']/summary_vlissingen['TAGP']

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # daily data

        # de bilt ------------------------------------------------------------------------------------------------------
        daily_debilt = pd.read_excel(os.path.join(dir, f"{yld}-long-term-daily-DE BILT-co2-{soil}.xlsx"))
        daily_debilt = daily_debilt[(daily_debilt.DVS >= 1) & (daily_debilt.DVS <=2)]
        daily_debilt['day'] = pd.to_datetime(daily_debilt['day'])
        daily_debilt['year'] = daily_debilt['day'].dt.year
        daily_debilt['month'] = daily_debilt['day'].dt.month
        daily_debilt['unique'] = 1
        daily_debilt['TEMP'] = (daily_debilt['TMAX'] + daily_debilt['TMIN']) / 2
        # grain filling days
        grain_fill_debilt = daily_debilt.groupby(['year'])['unique'].sum().reset_index()
        grain_fill_debilt = pd.merge(grain_fill_debilt, summary_debilt, on='year')
        # temperature sums
        daily_debilt = pd.read_excel(os.path.join(dir, f"{yld}-long-term-daily-DE BILT-co2-{soil}.xlsx"))
        daily_debilt['DAY'] = pd.to_datetime(daily_debilt['DAY'], format='%Y-%m-%d')
        df_final = pd.DataFrame()
        for yr in summary_debilt.year.unique():
            summary_subset = summary_debilt[summary_debilt.year == yr]
            filtered_df = daily_debilt.loc[(daily_debilt['DAY'] >= summary_subset.DOE.unique()[0]) & (daily_debilt['DAY'] < summary_subset.DOM.unique()[0])]
            filtered_df['TSUM'] = np.where(filtered_df['TEMP'] < 0, 0, filtered_df['TEMP'])
            filtered_df['TSUM'] = filtered_df['TSUM'].cumsum()
            em_ant = filtered_df.loc[(filtered_df['DVS'] >= 0) & (daily_debilt['DVS'] <= 1)]
            ant_mat = filtered_df.loc[(filtered_df['DVS'] >= 1) & (daily_debilt['DVS'] <= 2)]
            df = pd.DataFrame(data={'year': yr,
                                    'GDD_em_mat': filtered_df['TSUM'].max(),
                                    'GDD_em_ant': em_ant['TSUM'].max(),
                                    'GDD_ant_mat': ant_mat['TSUM'].max() - ant_mat['TSUM'].min(),
                                    'growing_season_days': len(filtered_df),
                                    'em_ant_days': len(em_ant),
                                    'ant_mat_days': len(ant_mat)-1,
                                    'RAD_em_mat': filtered_df['IRRAD'].cumsum().max(),
                                    'RAD_em_ant': em_ant['IRRAD'].cumsum().max(),
                                    'RAD_ant_mat': ant_mat['IRRAD'].cumsum().max() - ant_mat['IRRAD'].cumsum().min() }, index=[0])
            df_final = df_final.append(df)
        summary_debilt = pd.merge(summary_debilt, df_final, on='year')
        grain_fill_debilt = pd.merge(grain_fill_debilt, df_final, on='year')
        # eelde --------------------------------------------------------------------------------------------------------
        daily_eelde = pd.read_excel(os.path.join(dir, f"{yld}-long-term-daily-EELDE-co2-{soil}.xlsx"))
        daily_eelde = daily_eelde[(daily_eelde.DVS >= 1) & (daily_eelde.DVS <=2)]
        daily_eelde['day'] = pd.to_datetime(daily_eelde['day'])
        daily_eelde['year'] = daily_eelde['day'].dt.year
        daily_eelde['month'] = daily_eelde['day'].dt.month
        daily_eelde['unique'] = 1
        daily_eelde['TEMP'] = (daily_eelde['TMAX'] + daily_eelde['TMIN']) / 2
        # grain filling days
        grain_fill_eelde = daily_eelde.groupby(['year'])['unique'].sum().reset_index()
        grain_fill_eelde = pd.merge(grain_fill_eelde, summary_eelde, on='year')
        # temperature sums
        daily_eelde = pd.read_excel(os.path.join(dir, f"{yld}-long-term-daily-EELDE-co2-{soil}.xlsx"))
        daily_eelde['DAY'] = pd.to_datetime(daily_eelde['DAY'], format='%Y-%m-%d')
        df_final = pd.DataFrame()
        for yr in summary_eelde.year.unique():
            summary_subset = summary_eelde[summary_eelde.year == yr]
            filtered_df = daily_eelde.loc[(daily_eelde['DAY'] >= summary_subset.DOE.unique()[0]) & (daily_eelde['DAY'] < summary_subset.DOM.unique()[0])]
            filtered_df['TSUM'] = np.where(filtered_df['TEMP'] < 0, 0, filtered_df['TEMP'])
            filtered_df['TSUM'] = filtered_df['TSUM'].cumsum()
            em_ant = filtered_df.loc[(filtered_df['DVS'] >= 0) & (daily_eelde['DVS'] <= 1)]
            ant_mat = filtered_df.loc[(filtered_df['DVS'] >= 1) & (daily_eelde['DVS'] <= 2)]
            df = pd.DataFrame(data={'year': yr,
                                    'GDD_em_mat': filtered_df['TSUM'].max(),
                                    'GDD_em_ant': em_ant['TSUM'].max(),
                                    'GDD_ant_mat': ant_mat['TSUM'].max() - ant_mat['TSUM'].min(),
                                    'growing_season_days': len(filtered_df),
                                    'em_ant_days': len(em_ant),
                                    'ant_mat_days': len(ant_mat)-1,
                                    'RAD_em_mat': filtered_df['IRRAD'].cumsum().max(),
                                    'RAD_em_ant': em_ant['IRRAD'].cumsum().max(),
                                    'RAD_ant_mat': ant_mat['IRRAD'].cumsum().max() - ant_mat['IRRAD'].cumsum().min() }, index=[0])
            df_final = df_final.append(df)
        summary_eelde = pd.merge(summary_eelde, df_final, on='year')
        grain_fill_eelde = pd.merge(grain_fill_eelde, df_final, on='year')
        # vlissingen ---------------------------------------------------------------------------------------------------
        daily_vlissingen = pd.read_excel(os.path.join(dir, f"{yld}-long-term-daily-VLISSINGEN-co2-{soil}.xlsx"))
        daily_vlissingen = daily_vlissingen[(daily_vlissingen.DVS >= 1) & (daily_vlissingen.DVS <=2)]
        daily_vlissingen['day'] = pd.to_datetime(daily_vlissingen['day'])
        daily_vlissingen['year'] = daily_vlissingen['day'].dt.year
        daily_vlissingen['month'] = daily_vlissingen['day'].dt.month
        daily_vlissingen['unique'] = 1
        daily_vlissingen['TEMP'] = (daily_vlissingen['TMAX'] + daily_vlissingen['TMIN']) / 2
        # grain filling days
        grain_fill_vlissingen = daily_vlissingen.groupby(['year'])['unique'].sum().reset_index()
        grain_fill_vlissingen = pd.merge(grain_fill_vlissingen, summary_vlissingen, on='year')
        # temperature sums
        daily_vlissingen = pd.read_excel(os.path.join(dir, f"{yld}-long-term-daily-VLISSINGEN-co2-{soil}.xlsx"))
        daily_vlissingen['DAY'] = pd.to_datetime(daily_vlissingen['DAY'], format='%Y-%m-%d')
        df_final = pd.DataFrame()
        for yr in summary_vlissingen.year.unique():
            summary_subset = summary_vlissingen[summary_vlissingen.year == yr]
            filtered_df = daily_vlissingen.loc[(daily_vlissingen['DAY'] >= summary_subset.DOE.unique()[0]) & (daily_vlissingen['DAY'] < summary_subset.DOM.unique()[0])]
            filtered_df['TSUM'] = np.where(filtered_df['TEMP'] < 0, 0, filtered_df['TEMP'])
            filtered_df['TSUM'] = filtered_df['TSUM'].cumsum()
            em_ant = filtered_df.loc[(filtered_df['DVS'] >= 0) & (daily_vlissingen['DVS'] <= 1)]
            ant_mat = filtered_df.loc[(filtered_df['DVS'] >= 1) & (daily_vlissingen['DVS'] <= 2)]
            df = pd.DataFrame(data={'year': yr,
                                    'GDD_em_mat': filtered_df['TSUM'].max(),
                                    'GDD_em_ant': em_ant['TSUM'].max(),
                                    'GDD_ant_mat': ant_mat['TSUM'].max() - ant_mat['TSUM'].min(),
                                    'growing_season_days': len(filtered_df),
                                    'em_ant_days': len(em_ant),
                                    'ant_mat_days': len(ant_mat)-1,
                                    'RAD_em_mat': filtered_df['IRRAD'].cumsum().max(),
                                    'RAD_em_ant': em_ant['IRRAD'].cumsum().max(),
                                    'RAD_ant_mat': ant_mat['IRRAD'].cumsum().max() - ant_mat['IRRAD'].cumsum().min() }, index=[0])
            df_final = df_final.append(df)
        summary_vlissingen = pd.merge(summary_vlissingen, df_final, on='year')
        grain_fill_vlissingen = pd.merge(grain_fill_vlissingen, df_final, on='year')

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        left, width = .255, .71
        bottom, height = .25, .71
        right = left + width
        top = bottom + height
        wspace = 0.2
        hspace = 0.3
        kws_points = dict(s=100, alpha=0.9, linewidth=0.7)
        # --------------------------------------------------------------------------------------------------------------
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(13, 13))
        axes = plt.gca()
        f.subplots_adjust(wspace=wspace, hspace=hspace)
        # --------------------------------------------------------------------------------------------------------------
        # co2
        ax1.grid(linestyle='-', zorder=0, color='gainsboro')
        ax1.scatter(summary_eelde['mean'], summary_eelde['yp'], color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        y = summary_eelde['yp']
        X = summary_eelde[["mean"]].dropna()
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_eelde[["mean"]].dropna())
        if (est2.pvalues["mean"] < 0.05):
            ax1.plot(summary_eelde['mean'], linr_model.predict(summary_eelde[["mean"]]), color="orangered", label='y = {slope}x - {int}'.format(slope=linr_model.coef_[0].round(3), int=abs(linr_model.intercept_).round(2)), linewidth=1.75, linestyle='-', zorder=5)
        ax1.scatter(summary_debilt['mean'], summary_debilt['yp'], color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        y = summary_debilt['yp']
        X = summary_debilt[["mean"]].dropna()
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_debilt[["mean"]].dropna())
        if (est2.pvalues["mean"] < 0.05):
            ax1.plot(summary_debilt['mean'], linr_model.predict(summary_debilt[["mean"]]), color="darkblue", label='y = {slope}x - {int}'.format(slope=linr_model.coef_[0].round(3), int=abs(linr_model.intercept_).round(2)), linewidth=1.75, linestyle='-', zorder=5)
        ax1.scatter(summary_vlissingen['mean'], summary_vlissingen['yp'], color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        y = summary_vlissingen['yp']
        X = summary_vlissingen[["mean"]].dropna()
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_vlissingen[["mean"]].dropna())
        if (est2.pvalues["mean"] < 0.05):
            ax1.plot(summary_vlissingen['mean'], linr_model.predict(summary_vlissingen[["mean"]]), color="darkred", label='y = {slope}x - {int}'.format(slope=linr_model.coef_[0].round(3), int=abs(linr_model.intercept_).round(2)), linewidth=1.75, linestyle='-', zorder=5)
        ax1.set_ylim([6, 14])
        ax1.set_xlim([320, 420])
        ax1.set_yticklabels([6, 7, 8, 9, 10, 11, 12, 13, 14], fontsize=15)
        ax1.set_xticklabels([320, 340, 360, 380, 400, 420], fontsize=15, rotation=45)
        ax1.set_xlabel('Atm. CO2 concentration (ppm)', fontsize=16)
        ax1.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax1.set_facecolor('white')
        ax1.legend(loc='lower right', ncol=2, fontsize=14)
        ax1.set_title('A) Atmospheric CO2', y=0.9, x=0.30, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        # radiation
        ax2.grid(linestyle='-', zorder=0, color='gainsboro')
        ax2.scatter(summary_eelde.RAD_em_mat/1000000, summary_eelde.yp, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        ax2.scatter(summary_debilt.RAD_em_mat/1000000, summary_debilt.yp, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        ax2.scatter(summary_vlissingen.RAD_em_mat/1000000, summary_vlissingen.yp, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        all = summary_eelde.append(summary_debilt).append(summary_vlissingen)
        all.RAD_em_mat = all.RAD_em_mat/1000000
        all = all[['RAD_em_mat', 'yp']]
        all.to_csv(r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\4-hberghuijs-model--final\output\rad-vs-yield-{yld}-{soil}.csv".format(yld=yld, soil=soil))
        x = np.arange(0, 2*1600, 1)
        if(yld == 'yp'):
            a = 2.629902e+03
            b = round(4.796968e-03, 4)
        elif(yld=='yw' and soil =='clay'):
            a = 2.580519e+03
            b = round(4.802315e-03, 4)
        else:
            a = 2.553114e+03
            b = round(4.799133e-03, 4)
        ax2.plot(x, np.where(x < a, b * x, a * b), linestyle='-', linewidth=2.5, color='black', zorder=3, label=r'Yp = {b}x, x < {a}'.format(b=b, a=int(a)) + '\n' + r'Yp = {ab}, x > {a}'.format(ab=round(a*b, 1), a=int(a)))
        ax2.set_ylim([6, 14])
        ax2.set_xlim([1000, 3250])
        ax2.set_yticklabels([6, 7, 8, 9, 10, 11, 12, 13, 14], fontsize=15)
        ax2.set_xticklabels([1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250], fontsize=15, rotation=45)
        ax2.set_xlabel('Growing season radiation (MJ/m2)', fontsize=16)
        ax2.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax2.set_facecolor('white')
        ax2.legend(loc='lower left', fontsize=13)
        ax2.set_title('B) Solar radiation', y=0.9, x=0.29, fontsize=16, fontweight='bold')
        # ----------------------------------------------------------------------------------------------------------------------
        # gdd
        ax3.grid(linestyle='-', zorder=0, color='gainsboro')
        ax3.scatter(summary_eelde.GDD_em_mat, summary_eelde.yp, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        ax3.scatter(summary_debilt.GDD_em_mat, summary_debilt.yp, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        ax3.scatter(summary_vlissingen.GDD_em_mat, summary_vlissingen.yp, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        all = summary_eelde.append(summary_debilt).append(summary_vlissingen)
        all = all[['GDD_em_mat', 'yp']]
        all.to_csv(r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\4-hberghuijs-model--final\output\gdd-vs-yield-{yld}-{soil}.csv".format(yld=yld, soil=soil))
        x = np.arange(1900, 2801, 1)
        if (yld == 'yp'):
            a = 1.051289e+01
            b = round(8.798759e-04, 4)
            c = -3.739196e+08
        elif (yld == 'yw' and soil == 'clay'):
            a = 1.013687e+01
            b = round(1.019509e-03, 4)
            c = -3.651783e+08
        else:
            a = 6.633562e+00
            b = round(2.420836e-03, 4)
            c = -3.370429e+08
        ax3.plot(x, a + b * x + c * 0.99**x, linestyle='-', linewidth=2.5, color='black', zorder=3, label=r'Yp = a - bx - c*0.99^x')
        ax3.set_ylim([6, 14])
        ax3.set_xlim([1900, 2700])
        ax3.set_yticklabels([6, 7, 8, 9, 10, 11, 12, 13, 14], fontsize=15)
        ax3.set_xticklabels([1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700], fontsize=15, rotation=45)
        ax3.set_xlabel('Growing season GDD', fontsize=16)
        ax3.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax3.set_facecolor('white')
        ax3.legend(loc='lower right', fontsize=13)
        ax3.set_title('C) Temperature', y=0.9, x=0.26, fontsize=16, fontweight='bold')
        # ----------------------------------------------------------------------------------------------------------------------
        # etp
        ax4.grid(linestyle='-', zorder=0, color='gainsboro')
        ax4.scatter(summary_eelde.CTRAT*10 + summary_eelde.CEVST*10, summary_eelde.yp, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        ax4.scatter(summary_debilt.CTRAT*10 + summary_debilt.CEVST*10, summary_debilt.yp, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        ax4.scatter(summary_vlissingen.CTRAT*10 + summary_vlissingen.CEVST*10, summary_vlissingen.yp, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        all = summary_eelde.append(summary_debilt).append(summary_vlissingen)
        all = all[['yp', 'CTRAT', 'CEVST']]
        all.to_csv(r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\4-hberghuijs-model--final\output\etp-vs-yield-{yld}-{soil}.csv".format(yld=yld, soil=soil))
        x = np.arange(0, 500, 1)
        if (yld == 'yp'):
            a = round(354.88228769, 1)
            b = round(0.03542195, 3)
            c = round(-20.44353373, 1)
        elif (yld == 'yw' and soil == 'clay'):
            a = round(303.61197206, 1)
            b = round(0.04078942, 3)
            c = round(-60.46358392, 1)
        else:
            a = round(302.0154397, 1)
            b = round(0.0405648, 3)
            c = round(-61.8033283, 1)
        ax4.plot(x, np.where((x + c) < a, b * (x + c), a * b), linestyle='-', linewidth=2.5, color='black', zorder=3, label=r'Yw = {b}x {bc}, x < {ac}'.format(b=b, bc=round(b * c, 1), ac=int(a - c)) + '\n' + r'Yp = {ab}, x > {ac}'.format(ab=round(a * b, 1), ac=int(a - c)))
        ax4.set_ylim([6, 14])
        ax4.set_xlim([150, 500])
        ax4.set_yticklabels([6, 7, 8, 9, 10, 11, 12, 13, 14], fontsize=15)
        ax4.set_xticklabels([150, 200, 150, 300, 350, 400, 450, 500], fontsize=15, rotation=45)
        ax4.set_xlabel('Growing season evapotranspiration (mm)', fontsize=16)
        ax4.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax4.set_facecolor('white')
        ax4.legend(loc='lower left', fontsize=13)
        ax4.set_title('D) Evapotranspiration', y=0.9, x=0.34, fontsize=16, fontweight='bold')
        # ----------------------------------------------------------------------------------------------------------------------
        if(yld == 'yp'):
            f.savefig(os.path.join(dir, f"figure2-wheat-response-weather-{yld}.png"), bbox_inches='tight', dpi=1000)
        else:
            f.savefig(os.path.join(dir, f"figure2-wheat-response-weather-{yld}-{soil}.png"), bbox_inches='tight', dpi=1000)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
