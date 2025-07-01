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
        # plots

        left, width = .255, .71
        bottom, height = .25, .71
        right = left + width
        top = bottom + height
        wspace = 0.2
        hspace = 0.2
        kws_points = dict(s=100, alpha=0.9, linewidth=0.7)
        # --------------------------------------------------------------------------------------------------------------
        f, ((ax1, ax2), (ax4, ax5)) = plt.subplots(2, 2, figsize=(13.5, 6.5*2))
        axes = plt.gca()
        f.subplots_adjust(wspace=wspace, hspace=hspace)
        # --------------------------------------------------------------------------------------------------------------
        # year vs day of anthesis
        ax1.grid(linestyle='-', zorder=0)
        # eelde
        ax1.plot(summary_eelde.year, summary_eelde.DOA, color='orangered', zorder=2)
        ax1.scatter(summary_eelde.year, summary_eelde.DOA, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Eelde')
        y = summary_eelde.DOA
        X = summary_eelde[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_eelde[["year"]].dropna())
        ax1.plot(summary_eelde.year, linr_model.predict(summary_eelde[["year"]]), color="orangered", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax1.text(left+0.7, bottom+0.025, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='orangered', horizontalalignment='right', verticalalignment='top', transform=ax1.transAxes, family='sans-serif', fontsize=16)
        # de bilt
        ax1.plot(summary_debilt.year, summary_debilt.DOA, color='darkblue', zorder=2)
        ax1.scatter(summary_debilt.year, summary_debilt.DOA, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='De Bilt')
        y = summary_debilt.DOA
        X = summary_debilt[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_debilt[["year"]].dropna())
        ax1.plot(summary_debilt.year, linr_model.predict(summary_debilt[["year"]]), color="darkblue", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax1.text(left+0.7, bottom-0.05, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='darkblue', horizontalalignment='right', verticalalignment='top', transform=ax1.transAxes, family='sans-serif', fontsize=16)
        # vlissingen
        ax1.plot(summary_vlissingen.year, summary_vlissingen.DOA, color='darkred', zorder=2)
        ax1.scatter(summary_vlissingen.year, summary_vlissingen.DOA, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Vlissingen')
        y = summary_vlissingen.DOA
        X = summary_vlissingen[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_vlissingen[["year"]].dropna())
        ax1.plot(summary_vlissingen.year, linr_model.predict(summary_vlissingen[["year"]]), color="darkred", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax1.text(left+0.7, bottom-0.125, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='darkred', horizontalalignment='right', verticalalignment='top', transform=ax1.transAxes, family='sans-serif', fontsize=16)
        # plot setup
        ax1.axhline(152, label='June 1st', linestyle='--', linewidth=1.75, color='black')
        ax1.axhline(172, label='June 21st', linestyle='-', linewidth=1.75, color='black')
        ax1.set_ylim([120, 190])
        ax1.set_xlim([1970, 2020])
        ax1.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=14)
        ax1.set_yticklabels([120, 130, 140, 150, 160, 170, 180, 190], fontsize=14)
        ax1.set_ylabel('Day of anthesis (day-of-the-year)', fontsize=16)
        ax1.set_facecolor('whitesmoke')
        ax1.legend(loc='lower left', fontsize=13)
        ax1.set_title('A) Day of anthesis', fontsize=16, fontweight='bold', loc='left')
        # --------------------------------------------------------------------------------------------------------------
        # day of anthesis vs yield
        ax2.grid(linestyle='-', zorder=0)
        ax2.scatter(summary_eelde.RAD_em_ant/1000000, summary_eelde.DOA, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Eelde')
        ax2.axvline(grain_fill_eelde.RAD_em_ant.mean()/1000000, color='orangered', linewidth=1.5)
        y = summary_eelde.DOA
        X = summary_eelde[["RAD_em_ant"]].dropna() / 1000000
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_eelde[["RAD_em_ant"]].dropna()/1000000)
        ax2.plot(summary_eelde.RAD_em_ant/1000000, linr_model.predict(summary_eelde[["RAD_em_ant"]]/1000000), color="orangered", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax2.scatter(summary_debilt.RAD_em_ant/1000000, summary_debilt.DOA, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='De Bilt')
        ax2.axvline(grain_fill_debilt.RAD_em_ant.mean()/1000000, color='darkblue', linewidth=1.5)
        y = summary_debilt.DOA
        X = summary_debilt[["RAD_em_ant"]].dropna() / 1000000
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_debilt[["RAD_em_ant"]].dropna()/1000000)
        ax2.plot(summary_debilt.RAD_em_ant/1000000, linr_model.predict(summary_debilt[["RAD_em_ant"]]/1000000), color="darkblue", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax2.scatter(summary_vlissingen.RAD_em_ant/1000000, summary_vlissingen.DOA, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Vlissingen')
        ax2.axvline(grain_fill_vlissingen.RAD_em_ant.mean()/1000000, color='darkred', linewidth=1.5)
        y = summary_vlissingen.DOA
        X = summary_vlissingen[["RAD_em_ant"]].dropna() / 1000000
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_vlissingen[["RAD_em_ant"]].dropna()/1000000)
        ax2.plot(summary_vlissingen.RAD_em_ant/1000000, linr_model.predict(summary_vlissingen[["RAD_em_ant"]]/1000000), color="darkred", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax2.axhline(152, label='June 1st', linestyle='--', linewidth=1.75, color='black')
        ax2.axhline(172, label='June 21st', linestyle='-', linewidth=1.75, color='black')
        ax2.set_ylim([120, 190])
        ax2.set_xlim([1200, 2000])
        ax2.set_xticklabels([1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000], fontsize=14)
        ax2.set_yticklabels([120, 130, 140, 150, 160, 170, 180, 190], fontsize=14)
        ax2.set_ylabel('Day of anthesis (day-of-the-year)', fontsize=16)
        ax2.set_xlabel('Radiation emergence-anthesis (MJ/m2)', fontsize=16)
        ax2.set_facecolor('whitesmoke')
        ax2.legend(loc='lower left', fontsize=12)
        ax2.set_title('B) Radiation vs anthesis', fontsize=16, fontweight='bold', loc='left')
        # --------------------------------------------------------------------------------------------------------------
        # year vs grain filling days
        ax4.grid(linestyle='-', zorder=0)
        # eelde
        ax4.plot(grain_fill_eelde.year, grain_fill_eelde.unique, color='orangered', zorder=2)
        ax4.scatter(grain_fill_eelde.year, grain_fill_eelde.unique, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Eelde')
        y = grain_fill_eelde.unique
        X = grain_fill_eelde[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_eelde[["year"]].dropna())
        ax4.plot(grain_fill_eelde.year, linr_model.predict(grain_fill_eelde[["year"]]), color="orangered", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax4.text(left+0.7, bottom+0.025, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='orangered', horizontalalignment='right', verticalalignment='top', transform=ax4.transAxes, family='sans-serif', fontsize=16)
        # de bilt
        ax4.plot(grain_fill_debilt.year, grain_fill_debilt.unique, color='darkblue', zorder=2)
        ax4.scatter(grain_fill_debilt.year, grain_fill_debilt.unique, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='De Bilt')
        y = grain_fill_debilt.unique
        X = grain_fill_debilt[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_debilt[["year"]].dropna())
        ax4.plot(grain_fill_debilt.year, linr_model.predict(grain_fill_debilt[["year"]]), color="darkblue", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax4.text(left+0.7, bottom-0.05, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='darkblue', horizontalalignment='right', verticalalignment='top', transform=ax4.transAxes, family='sans-serif', fontsize=16)
        # vlissingen
        ax4.plot(grain_fill_vlissingen.year, grain_fill_vlissingen.unique, color='darkred', zorder=2)
        ax4.scatter(grain_fill_vlissingen.year, grain_fill_vlissingen.unique, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Vlissingen')
        y = grain_fill_vlissingen.unique
        X = grain_fill_vlissingen[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_vlissingen[["year"]].dropna())
        ax4.plot(grain_fill_vlissingen.year, linr_model.predict(grain_fill_vlissingen[["year"]]), color="darkred", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax4.text(left+0.7, bottom-0.125, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='darkred', horizontalalignment='right', verticalalignment='top', transform=ax4.transAxes, family='sans-serif', fontsize=16)
        # plot setup
        ax4.set_ylim([35, 75])
        ax4.set_xlim([1970, 2020])
        ax4.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=14)
        ax4.set_yticklabels([35, 40, 45, 50, 55, 60, 65, 70, 75], fontsize=14)
        ax4.set_ylabel('Grain filling (number of days)', fontsize=16)
        ax4.set_facecolor('whitesmoke')
        ax4.legend(loc='lower left', fontsize=13)
        ax4.set_title('C) Grain filling days', fontsize=16, fontweight='bold', loc='left')
        # --------------------------------------------------------------------------------------------------------------
        # grain filling days vs yield
        ax5.grid(linestyle='-', zorder=0)
        ax5.scatter(grain_fill_eelde.RAD_ant_mat/1000000, grain_fill_eelde.unique, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Eelde')
        ax5.axvline(grain_fill_eelde.RAD_ant_mat.mean()/1000000, color='orangered', linewidth=1.5)
        y = grain_fill_eelde.unique
        X = grain_fill_eelde[["RAD_ant_mat"]].dropna() / 1000000
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_eelde[["RAD_ant_mat"]].dropna()/1000000)
        ax5.plot(grain_fill_eelde.RAD_ant_mat/1000000, linr_model.predict(grain_fill_eelde[["RAD_ant_mat"]]/1000000), color="orangered", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax5.scatter(grain_fill_debilt.RAD_ant_mat/1000000, grain_fill_debilt.unique, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='De Bilt')
        ax5.axvline(grain_fill_debilt.RAD_ant_mat.mean()/1000000, color='darkblue', linewidth=1.5)
        y = grain_fill_debilt.unique
        X = grain_fill_debilt[["RAD_ant_mat"]].dropna() / 1000000
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_debilt[["RAD_ant_mat"]].dropna()/1000000)
        ax5.plot(grain_fill_debilt.RAD_ant_mat/1000000, linr_model.predict(grain_fill_debilt[["RAD_ant_mat"]]/1000000), color="darkblue", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax5.scatter(grain_fill_vlissingen.RAD_ant_mat/1000000, grain_fill_vlissingen.unique, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Vlissingen')
        ax5.axvline(grain_fill_vlissingen.RAD_ant_mat.mean()/1000000, color='darkred', linewidth=1.5)
        y = grain_fill_vlissingen.unique
        X = grain_fill_vlissingen[["RAD_ant_mat"]].dropna() / 1000000
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_vlissingen[["RAD_ant_mat"]].dropna()/1000000)
        ax5.plot(grain_fill_vlissingen.RAD_ant_mat/1000000, linr_model.predict(grain_fill_vlissingen[["RAD_ant_mat"]]/1000000), color="darkred", label='', linewidth=1.5, linestyle='-', zorder=5)
        ax5.set_ylim([35, 75])
        ax5.set_xlim([750, 1200])
        ax5.set_xticklabels([750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200], fontsize=14)
        ax5.set_yticklabels([35, 40, 45, 50, 55, 60, 65, 70, 75], fontsize=14)
        ax5.set_ylabel('Grain filling days (#)', fontsize=16)
        ax5.set_xlabel('Radiation anthesis-maturity (MJ/m2)', fontsize=16)
        ax5.set_facecolor('whitesmoke')
        ax5.legend(loc='lower left', fontsize=12)
        ax5.set_title('D) Radiation vs grain filling', fontsize=16, fontweight='bold', loc='left')
        # --------------------------------------------------------------------------------------------------------------
        if(yld == 'yp'):
            f.savefig(os.path.join(dir, f"yield-vs-phenology-{yld}.png".format(yld=yld, soil=soil)), bbox_inches='tight', dpi=1000)
        else:
            f.savefig(os.path.join(dir, f"yield-vs-phenology-{yld}-{soil}.png".format(yld=yld, soil=soil)), bbox_inches='tight', dpi=1000)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
