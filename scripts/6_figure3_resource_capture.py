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
        wspace = 0.25
        hspace = 0.25
        kws_points = dict(s=100, alpha=0.9, linewidth=0.7)
        # --------------------------------------------------------------------------------------------------------------
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 6.5))
        axes = plt.gca()
        f.subplots_adjust(wspace=wspace, hspace=hspace)
        # --------------------------------------------------------------------------------------------------------------
        # gdd eme-ant vs. anthesis date
        ax1.grid(linestyle='-', zorder=0,color='gainsboro')
        ax1.axhline(152, label='June 1st', linestyle='--', linewidth=1.75, color='black')
        ax1.scatter(summary_eelde.DOA, summary_eelde.GDD_em_mat, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        y = summary_eelde[['GDD_em_mat']]
        X = summary_eelde[["DOA"]]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_eelde[["DOA"]])
        if (est2.pvalues["DOA"] < 0.05):
            ax1.plot(summary_eelde.DOA, linr_model.predict(summary_eelde[["DOA"]]), color="orangered", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax1.scatter(summary_debilt.DOA, summary_debilt.GDD_em_mat, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        y = summary_debilt[['GDD_em_mat']]
        X = summary_debilt[["DOA"]]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_debilt[["DOA"]].dropna())
        if (est2.pvalues["DOA"] < 0.05):
            ax1.plot(summary_debilt.DOA, linr_model.predict(summary_debilt[["DOA"]]), color="darkblue", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax1.scatter(summary_vlissingen.DOA, summary_vlissingen.GDD_em_mat, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        y = summary_vlissingen[['GDD_em_mat']]
        X = summary_vlissingen[["DOA"]]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_vlissingen[["DOA"]].dropna())
        if (est2.pvalues["DOA"] < 0.05):
            ax1.plot(summary_vlissingen.DOA, linr_model.predict(summary_vlissingen[["DOA"]]), color="darkred", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax1.axvline(172, label='June 21st', linestyle='-', linewidth=1.75, color='black')
        ax1.set_xlim([130, 190])
        ax1.set_ylim([1700, 2700])
        ax1.set_yticklabels([1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700], fontsize=15)
        ax1.set_xticklabels([130, 140, 150, 160, 170, 180, 190], fontsize=15)
        ax1.set_xlabel('Day of anthesis (DOY)', fontsize=16)
        ax1.set_ylabel('GDD emergence-anthesis', fontsize=16)
        ax1.set_facecolor('white')
        ax1.legend(loc='lower right', fontsize=12.5, ncol=2)
        ax1.set_title('A)', x=0.075, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        # gdd ant-mat vs. grain filling days
        ax2.grid(linestyle='-', zorder=0, color='gainsboro')
        ax2.scatter(grain_fill_eelde.unique, grain_fill_eelde.GDD_ant_mat, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        y = grain_fill_eelde[['GDD_ant_mat']]
        X = grain_fill_eelde[["unique"]]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_eelde[["unique"]])
        if (est2.pvalues["unique"] < 0.05):
            ax2.plot(grain_fill_eelde.unique, linr_model.predict(grain_fill_eelde[["unique"]]), color="orangered", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax2.scatter(grain_fill_debilt.unique, grain_fill_debilt.GDD_ant_mat, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        y = grain_fill_debilt[['GDD_ant_mat']]
        X = grain_fill_debilt[["unique"]]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_debilt[["unique"]].dropna())
        if (est2.pvalues["unique"] < 0.05):
            ax2.plot(grain_fill_debilt.unique, linr_model.predict(grain_fill_debilt[["unique"]]), color="darkblue", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax2.scatter(grain_fill_vlissingen.unique, grain_fill_vlissingen.GDD_ant_mat, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        y = grain_fill_vlissingen[['GDD_ant_mat']]
        X = grain_fill_vlissingen[["unique"]]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_vlissingen[["unique"]].dropna())
        if (est2.pvalues["unique"] < 0.05):
            ax2.plot(grain_fill_vlissingen.unique, linr_model.predict(grain_fill_vlissingen[["unique"]]), color="darkred", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax2.set_xlim([40, 70])
        ax2.set_ylim([860, 910])
        ax2.set_yticklabels([860, 870, 880, 890, 900, 910], fontsize=15)
        ax2.set_xticklabels([40, 45, 50, 55, 60, 65, 70], fontsize=15)
        ax2.set_xlabel('Day of anthesis (DOY)', fontsize=16)
        ax2.set_ylabel('GDD anthesis-maturity', fontsize=16)
        ax2.set_facecolor('white')
        ax2.legend(loc='lower right', fontsize=12.5, ncol=2)
        ax2.set_title('B)', x=0.075, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        if(yld == 'yp'):
            f.savefig(os.path.join(dir, f"figure-s1-wheat-phenology-{yld}.png"), bbox_inches='tight', dpi=1000)
        else:
            f.savefig(os.path.join(dir, f"figure-s1-wheat-phenology-{yld}-{soil}.png"), bbox_inches='tight', dpi=1000)

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # plots

        left, width = .255, .71
        bottom, height = .25, .71
        right = left + width
        top = bottom + height
        wspace = 0.25
        hspace = 0.25
        kws_points = dict(s=100, alpha=0.9, linewidth=0.7)
        # --------------------------------------------------------------------------------------------------------------
        f, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(13.5, 6.5*3))
        axes = plt.gca()
        f.subplots_adjust(wspace=wspace, hspace=hspace)

        # --------------------------------------------------------------------------------------------------------------
        summary_debilt_new = pd.read_excel(os.path.join(dir, f"{yld}-long-term-summary-DE BILT-co2-{soil}.xlsx"))
        summary_debilt_new['DOA'] = pd.to_datetime(summary_debilt_new['DOA'])
        summary_debilt_new['DOA'] = summary_debilt_new['DOA'].dt.dayofyear
        summary_debilt_new['DOM'] = pd.to_datetime(summary_debilt_new['DOM'])
        summary_debilt_new['DOM_doy'] = summary_debilt_new['DOM'].dt.dayofyear
        summary_debilt_new['gr_fill_days'] = summary_debilt_new.DOM_doy - summary_debilt_new.DOA
        summary_debilt_new['year'] = summary_debilt_new['DOM'].dt.year
        summary_debilt_new['month'] = summary_debilt_new['DOM'].dt.month
        summary_debilt_new['yp'] = summary_debilt_new['TWSO']/1000
        summary_debilt_new['hi'] = 100 * summary_debilt_new['TWSO']/summary_debilt_new['TAGP']
        # summary data
        summary_eelde_new = pd.read_excel(os.path.join(dir, f"{yld}-long-term-summary-EELDE-co2-{soil}.xlsx"))
        summary_eelde_new['DOA'] = pd.to_datetime(summary_eelde_new['DOA'])
        summary_eelde_new['DOA'] = summary_eelde_new['DOA'].dt.dayofyear
        summary_eelde_new['DOM'] = pd.to_datetime(summary_eelde_new['DOM'])
        summary_eelde_new['DOM_doy'] = summary_eelde_new['DOM'].dt.dayofyear
        summary_eelde_new['gr_fill_days'] = summary_eelde_new.DOM_doy - summary_eelde_new.DOA
        summary_eelde_new['year'] = summary_eelde_new['DOM'].dt.year
        summary_eelde_new['month'] = summary_eelde_new['DOM'].dt.month
        summary_eelde_new['yp'] = summary_eelde_new['TWSO']/1000
        summary_eelde_new['hi'] = 100 * summary_eelde_new['TWSO']/summary_eelde_new['TAGP']
        # summary data
        summary_vlissingen_new = pd.read_excel(os.path.join(dir, f"{yld}-long-term-summary-VLISSINGEN-co2-{soil}.xlsx"))
        summary_vlissingen_new['DOA'] = pd.to_datetime(summary_vlissingen_new['DOA'])
        summary_vlissingen_new['DOA'] = summary_vlissingen_new['DOA'].dt.dayofyear
        summary_vlissingen_new['DOM'] = pd.to_datetime(summary_vlissingen_new['DOM'])
        summary_vlissingen_new['DOM_doy'] = summary_vlissingen_new['DOM'].dt.dayofyear
        summary_vlissingen_new['gr_fill_days'] = summary_vlissingen_new.DOM_doy - summary_vlissingen_new.DOA
        summary_vlissingen_new['year'] = summary_vlissingen_new['DOM'].dt.year
        summary_vlissingen_new['month'] = summary_vlissingen_new['DOM'].dt.month
        summary_vlissingen_new['yp'] = summary_vlissingen_new['TWSO']/1000
        summary_vlissingen_new['hi'] = 100 * summary_vlissingen_new['TWSO']/summary_vlissingen_new['TAGP']
        # --------------------------------------------------------------------------------------------------------------
        ax1.grid(linestyle='-', zorder=0, color='gainsboro')
        # eelde
        ax1.plot(summary_eelde_new.year, summary_eelde_new.DOA, color='orangered', zorder=2)
        ax1.scatter(summary_eelde_new.year, summary_eelde_new.DOA, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        y = summary_eelde_new.DOA
        X = summary_eelde_new[["year"]].dropna()
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_eelde_new[["year"]].dropna())
        if (est2.pvalues["year"] < 0.05):
            ax1.plot(summary_eelde_new.year, linr_model.predict(summary_eelde_new[["year"]]), color="orangered", label='', linewidth=1.5, linestyle='-', zorder=5)
            ax1.text(left+0.7, bottom+0.025, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='orangered', horizontalalignment='right', verticalalignment='top', transform=ax1.transAxes, family='sans-serif', fontsize=16)
        # Central
        ax1.plot(summary_debilt_new.year, summary_debilt_new.DOA, color='darkblue', zorder=2)
        ax1.scatter(summary_debilt_new.year, summary_debilt_new.DOA, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        y = summary_debilt_new.DOA
        X = summary_debilt_new[["year"]].dropna()
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_debilt_new[["year"]].dropna())
        if (est2.pvalues["year"] < 0.05):
            ax1.plot(summary_debilt_new.year, linr_model.predict(summary_debilt_new[["year"]]), color="darkblue", label='', linewidth=1.5, linestyle='-', zorder=5)
            ax1.text(left+0.7, bottom-0.05, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='darkblue', horizontalalignment='right', verticalalignment='top', transform=ax1.transAxes, family='sans-serif', fontsize=16)
        # vlissingen
        ax1.plot(summary_vlissingen_new.year, summary_vlissingen_new.DOA, color='darkred', zorder=2)
        ax1.scatter(summary_vlissingen_new.year, summary_vlissingen_new.DOA, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        y = summary_vlissingen_new.DOA
        X = summary_vlissingen_new[["year"]].dropna()
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_vlissingen_new[["year"]].dropna())
        if (est2.pvalues["year"] < 0.05):
            ax1.plot(summary_vlissingen_new.year, linr_model.predict(summary_vlissingen_new[["year"]]), color="darkred", label='', linewidth=1.5, linestyle='-', zorder=5)
            ax1.text(left+0.7, bottom-0.125, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='darkred', horizontalalignment='right', verticalalignment='top', transform=ax1.transAxes, family='sans-serif', fontsize=16)
        # plot setup
        ax1.axhline(152, label='June 1st', linestyle='--', linewidth=1.75, color='black')
        ax1.axhline(172, label='June 21st', linestyle='-', linewidth=1.75, color='black')
        ax1.set_ylim([120, 190])
        ax1.set_xlim([1970, 2020])
        ax1.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax1.set_yticklabels([120, 130, 140, 150, 160, 170, 180, 190], fontsize=14.5)
        ax1.set_ylabel('Day of anthesis (day-of-the-year)', fontsize=16)
        ax1.set_facecolor('white')
        ax1.legend(loc='lower left', fontsize=12.5)
        ax1.set_title('A)', x=0.075, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        # year vs grain filling days
        ax2.grid(linestyle='-', zorder=0, color='gainsboro')
        # eelde
        ax2.plot(summary_eelde_new.year, summary_eelde_new.gr_fill_days, color='orangered', zorder=2)
        ax2.scatter(summary_eelde_new.year, summary_eelde_new.gr_fill_days, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        y = summary_eelde_new.gr_fill_days
        X = summary_eelde_new[["year"]].dropna()
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_eelde_new[["year"]].dropna())
        if (est2.pvalues["year"] < 0.05):
            ax2.plot(summary_eelde_new.year, linr_model.predict(summary_eelde_new[["year"]]), color="orangered", label='', linewidth=1.5, linestyle='-', zorder=5)
            ax2.text(left+0.7, bottom+0.025, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='orangered', horizontalalignment='right', verticalalignment='top', transform=ax2.transAxes, family='sans-serif', fontsize=16)
        # Central
        ax2.plot(summary_debilt_new.year, summary_debilt_new.gr_fill_days, color='darkblue', zorder=2)
        ax2.scatter(summary_debilt_new.year, summary_debilt_new.gr_fill_days, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        y = summary_debilt_new.gr_fill_days
        X = summary_debilt_new[["year"]].dropna()
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_debilt_new[["year"]].dropna())
        if (est2.pvalues["year"] < 0.05):
            ax2.plot(summary_debilt_new.year, linr_model.predict(summary_debilt_new[["year"]]), color="darkblue", label='', linewidth=1.5, linestyle='-', zorder=5)
            ax2.text(left+0.7, bottom-0.05, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='darkblue', horizontalalignment='right', verticalalignment='top', transform=ax2.transAxes, family='sans-serif', fontsize=16)
        # vlissingen
        ax2.plot(summary_vlissingen_new.year, summary_vlissingen_new.gr_fill_days, color='darkred', zorder=2)
        ax2.scatter(summary_vlissingen_new.year, summary_vlissingen_new.gr_fill_days, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        y = summary_vlissingen_new.gr_fill_days
        X = summary_vlissingen_new[["year"]].dropna()
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_vlissingen_new[["year"]].dropna())
        if (est2.pvalues["year"] < 0.05):
            ax2.plot(summary_vlissingen_new.year, linr_model.predict(summary_vlissingen_new[["year"]]), color="darkred", label='', linewidth=1.5, linestyle='-', zorder=5)
            ax2.text(left+0.7, bottom-0.125, '{value} days/yr'.format(value=linr_model.coef_[0].round(2)), color='darkred', horizontalalignment='right', verticalalignment='top', transform=ax2.transAxes, family='sans-serif', fontsize=16)
        # plot setup
        ax2.set_ylim([35, 70])
        ax2.set_xlim([1970, 2020])
        ax2.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax2.set_yticklabels([35, 40, 45, 50, 55, 60, 65, 70], fontsize=14.5)
        ax2.set_ylabel('Grain filling (number of days)', fontsize=16)
        ax2.set_facecolor('white')
        ax2.legend(loc='lower left', fontsize=12.5)
        ax2.set_title('B)', x=0.075, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        # day of anthesis vs yield
        ax3.grid(linestyle='-', zorder=0, color='gainsboro')
        ax3.axvline(152, label='June 1st', linestyle='--', linewidth=1.75, color='black')
        ax3.scatter(summary_eelde.DOA, summary_eelde.RAD_em_ant/1000000, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        X = summary_eelde[['DOA']]
        y = summary_eelde[["RAD_em_ant"]] / 1000000
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_eelde[["RAD_em_ant"]]/ 1000000)
        if (est2.pvalues["DOA"] < 0.05):
            ax3.plot(summary_eelde.DOA, linr_model.predict(summary_eelde[["DOA"]]), color="orangered", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax3.scatter(summary_debilt.DOA, summary_debilt.RAD_em_ant/1000000, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        X = summary_debilt[['DOA']]
        y = summary_debilt[["RAD_em_ant"]] / 1000000
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_debilt[["DOA"]].dropna())
        if (est2.pvalues["DOA"] < 0.05):
            ax3.plot(summary_debilt.DOA, linr_model.predict(summary_debilt[["DOA"]]), color="darkblue", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax3.scatter(summary_vlissingen.DOA, summary_vlissingen.RAD_em_ant/1000000, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        X = summary_vlissingen[['DOA']]
        y = summary_vlissingen[["RAD_em_ant"]] / 1000000
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_vlissingen[["DOA"]].dropna())
        if (est2.pvalues["DOA"] < 0.05):
            ax3.plot(summary_vlissingen.DOA, linr_model.predict(summary_vlissingen[["DOA"]]), color="darkred", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax3.axvline(172, label='June 21st', linestyle='-', linewidth=1.75, color='black')
        ax3.set_xlim([140, 190])
        ax3.set_ylim([1000, 2000])
        ax3.set_yticklabels([1000, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000], fontsize=15)
        ax3.set_xticklabels([140, 150, 160, 170, 180, 190], fontsize=15)
        ax3.set_xlabel('Day of anthesis (DOY)', fontsize=16)
        ax3.set_ylabel('Radiation emergence-anthesis (MJ/m2)', fontsize=16)
        ax3.set_facecolor('white')
        ax3.legend(loc='lower right', fontsize=12.5, ncol=2)
        ax3.set_title('C)', x=0.075, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        # grain filling days vs yield
        ax4.grid(linestyle='-', zorder=0, color='gainsboro')
        ax4.scatter(grain_fill_eelde.unique, grain_fill_eelde.RAD_ant_mat/1000000, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        X = grain_fill_eelde[['unique']]
        y = grain_fill_eelde[["RAD_ant_mat"]] / 1000000
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_eelde[["unique"]])
        if (est2.pvalues["unique"] < 0.05):
            ax4.plot(grain_fill_eelde.unique, linr_model.predict(grain_fill_eelde[["unique"]]), color="orangered", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax4.scatter(grain_fill_debilt.unique, grain_fill_debilt.RAD_ant_mat/1000000, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        X = grain_fill_debilt[['unique']]
        y = grain_fill_debilt[["RAD_ant_mat"]] / 1000000
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_debilt[["unique"]])
        if (est2.pvalues["unique"] < 0.05):
            ax4.plot(grain_fill_debilt.unique, linr_model.predict(grain_fill_debilt[["unique"]]), color="darkblue", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax4.scatter(grain_fill_vlissingen.unique, grain_fill_vlissingen.RAD_ant_mat/1000000, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        X = grain_fill_vlissingen[['unique']]
        y = grain_fill_vlissingen[["RAD_ant_mat"]] / 1000000
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(grain_fill_vlissingen[["unique"]])
        if(est2.pvalues["unique"] < 0.05):
            ax4.plot(grain_fill_vlissingen.unique, linr_model.predict(grain_fill_vlissingen[["unique"]]), color="darkred", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax4.set_xlim([45, 65])
        ax4.set_ylim([650, 1200])
        ax4.set_yticklabels([650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200], fontsize=14)
        ax4.set_xticks([45, 50, 55, 60, 65])
        ax4.set_xticklabels([45, 50, 55, 60, 65], fontsize=14)
        ax4.set_xlabel('Grain filling days (#)', fontsize=16)
        ax4.set_ylabel('Radiation anthesis-maturity (MJ/m2)', fontsize=16)
        ax4.set_facecolor('white')
        ax4.legend(loc='lower left', fontsize=12.5, ncol=1)
        ax4.set_title('D)', x=0.075, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        # anthesis date vs yp
        ax5.grid(linestyle='-', zorder=0, color='gainsboro')
        ax5.axvline(152, label='June 1st', linestyle='--', linewidth=1.75, color='black')
        ax5.scatter(summary_eelde.DOA, summary_eelde.yp, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        X = summary_eelde[['DOA']]
        y = summary_eelde[["yp"]]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_eelde[["yp"]])
        if (est2.pvalues["DOA"] < 0.05):
            ax5.plot(summary_eelde.DOA, linr_model.predict(summary_eelde[["DOA"]]), color="orangered", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax5.scatter(summary_debilt.DOA, summary_debilt.yp, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        X = summary_debilt[['DOA']]
        y = summary_debilt[["yp"]]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_debilt[["DOA"]].dropna())
        if (est2.pvalues["DOA"] < 0.05):
            ax5.plot(summary_debilt.DOA, linr_model.predict(summary_debilt[["DOA"]]), color="darkblue", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax5.scatter(summary_vlissingen.DOA, summary_vlissingen.yp, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        X = summary_vlissingen[['DOA']]
        y = summary_vlissingen[["yp"]]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(summary_vlissingen[["DOA"]].dropna())
        if (est2.pvalues["DOA"] < 0.05):
            ax5.plot(summary_vlissingen.DOA, linr_model.predict(summary_vlissingen[["DOA"]]), color="darkred", label='y = {slope}x + {int}'.format(slope=list(linr_model.coef_)[0][0].round(2), int=abs(linr_model.intercept_[0]).round(1)), linewidth=1.5, linestyle='-', zorder=5)
        ax5.axvline(172, label='June 21st', linestyle='-', linewidth=1.75, color='black')
        ax5.set_xlim([140, 190])
        ax5.set_ylim([6, 14])
        ax5.set_yticklabels([6, 7, 8, 9, 10, 11, 12, 13, 14], fontsize=15)
        ax5.set_xticklabels([140, 150, 160, 170, 180, 190], fontsize=15)
        ax5.set_xlabel('Day of anthesis (DOY)', fontsize=16)
        ax5.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax5.set_facecolor('white')
        ax5.legend(loc='lower right', fontsize=12.5, ncol=2)
        ax5.set_title('E)', x=0.075, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        # grain filling days vs yp
        ax6.grid(linestyle='-', zorder=0, color='gainsboro')
        ax6.scatter(grain_fill_eelde.unique, grain_fill_eelde.yp, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Northeast')
        all = grain_fill_eelde[['unique', 'yp']]
        all.to_csv(os.path.join(dir, "gf-vs-yield-eelde-{yld}-{soil}.csv".format(yld=yld, soil=soil)))
        x = np.arange(grain_fill_eelde.unique.min(), grain_fill_eelde.unique.max(), 0.5)
        if(yld == 'yp'):
            a = -62.29200079
            b = 2.71531029
            c = -0.02460406
            d = 55.18012
        elif(yld=='yw' and soil =='clay'):
            a = -55.00914314
            b = 2.44924701
            c = -0.02220732
            d = 55.14503
        else:
            a = -67.07848861
            b = 2.83526393
            c = -0.02530112
            d = 56.0304
        ax6.plot(x, a + b * x + c * x**2, linestyle='-', linewidth=1.5, color='orangered', zorder=3, label='Yp = {a} + {b}x - {c}*x^2'.format(a=round(a, 1), b=round(b, 1), c=round(c, 2)))
        ax6.axvline(d, linestyle='--', linewidth=1.5, color='orangered', zorder=3)
        ax6.scatter(grain_fill_debilt.unique, grain_fill_debilt.yp, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Central')
        all = grain_fill_debilt[['unique', 'yp']]
        all.to_csv(os.path.join(dir, "gf-vs-yield-debilt-{yld}-{soil}.csv".format(yld=yld, soil=soil)))
        x = np.arange(grain_fill_debilt.unique.min(), grain_fill_debilt.unique.max(), 0.5)
        if(yld == 'yp'):
            a = -70.45064750
            b = 3.09626034
            c = -0.02894219
            d = 53.49043
        elif(yld=='yw' and soil =='clay'):
            a = -90.70775224
            b = 3.77837564
            c = -0.03467425
            d = 54.48389
        else:
            a = -81.92933551
            b = 3.42118245
            c = -0.03119674
            d = 54.83238
        ax6.plot(x, a + b * x + c * x**2, linestyle='-', linewidth=1.5, color='darkblue', zorder=3, label='Yp = {a} + {b}x - {c}*x^2'.format(a=round(a, 1), b=round(b, 1), c=round(c, 2)))
        ax6.axvline(d, linestyle='--', linewidth=1.5, color='darkblue', zorder=3)
        ax6.scatter(grain_fill_vlissingen.unique, grain_fill_vlissingen.yp, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Southwest')
        all = grain_fill_vlissingen[['unique', 'yp']]
        all.to_csv(os.path.join(dir, "gf-vs-yield-vlissingen-{yld}-{soil}.csv".format(yld=yld, soil=soil)))
        x = np.arange(grain_fill_vlissingen.unique.min(), grain_fill_vlissingen.unique.max(), 0.5)
        if(yld == 'yp'):
            a = -139.47957596
            b = 5.78025877
            c = -0.05478373
            d = 52.75525
        elif(yld=='yw' and soil =='clay'):
            a = -137.52047314
            b = 5.70166178
            c = -0.05401438
            d = 52.77911
        else:
            a = -129.01307790
            b = 5.36695742
            c = -0.05078022
            d = 52.84496
        ax6.plot(x, a + b * x + c * x**2, linestyle='-', linewidth=1.5, color='darkred', zorder=3, label='Yp = {a} + {b}x - {c}*x^2'.format(a=round(a, 1), b=round(b, 1), c=round(c, 2)))
        ax6.axvline(d, linestyle='--', linewidth=1.5, color='darkred', zorder=3)
        ax6.set_xlim([45, 65])
        ax6.set_ylim([6, 14])
        ax6.set_yticklabels([6, 7, 8, 9, 10, 11, 12, 13, 14], fontsize=15)
        ax6.set_xticks([45, 50, 55, 60, 65])
        ax6.set_xticklabels([45, 50, 55, 60, 65], fontsize=14)
        ax6.set_xlabel('Grain filling days (#)', fontsize=16)
        ax6.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax6.set_facecolor('white')
        ax6.legend(loc='lower left', fontsize=11, ncol=2)
        ax6.set_title('F)', x=0.075, y=0.9, fontsize=16, fontweight='bold')
        # --------------------------------------------------------------------------------------------------------------
        if (yld == 'yp'):
            f.savefig(os.path.join(dir, f"figure3-phenology-weather-{yld}.png"), bbox_inches='tight', dpi=1000)
        else:
            f.savefig(os.path.join(dir, f"figure3-phenology-weather-{yld}-{soil}.png"), bbox_inches='tight', dpi=1000)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
