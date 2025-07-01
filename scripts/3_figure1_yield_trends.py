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
var_dir = r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\1-calibration-jsilva-files\Data Input\Variety Trials"
cbs_dir = r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\1-calibration-jsilva-files\Data Input\CBS Statistics"
emmeans_var = r"D:\# Jvasco\# Portfolio\Curriculum\6. CIMMYT Scientist\_WUR PPS Wheat Trials\4-hberghuijs-model--final\output"

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

ya_flevoland = pd.read_csv(os.path.join(yp_dir, 'Akkerbouwgewassen__productie_29112022_071405.csv'), sep=';')
ya_flevoland = ya_flevoland[ya_flevoland.Gewassen == 'Tarwe (totaal)'].dropna()
ya_flevoland = ya_flevoland[['Gewassen', 'Perioden', "Regio's", 'Bruto opbrengst per ha (1 000 kg)']]
ya_flevoland = ya_flevoland.rename(columns={'Bruto opbrengst per ha (1 000 kg)': 'yield_tha', "Regio's": 'Region'})
ya_flevoland['Perioden'] = pd.to_numeric(ya_flevoland.Perioden)
ya_flevoland['yield_tha'] = pd.to_numeric(ya_flevoland.yield_tha)
ya_flevoland = ya_flevoland[ya_flevoland.Perioden < 2020]

ya_groningen = pd.read_csv(os.path.join(yp_dir, 'Akkerbouwgewassen__productie_29112022_071349.csv'), sep=';')
ya_groningen = ya_groningen[ya_groningen.Gewassen == 'Tarwe (totaal)'].dropna()
ya_groningen = ya_groningen[['Gewassen', 'Perioden', "Regio's", 'Bruto opbrengst per ha (1 000 kg)']]
ya_groningen = ya_groningen.rename(columns={'Bruto opbrengst per ha (1 000 kg)': 'yield_tha'})
ya_groningen['Perioden'] = pd.to_numeric(ya_groningen.Perioden)
ya_groningen['yield_tha'] = pd.to_numeric(ya_groningen.yield_tha)
ya_groningen = ya_groningen[ya_groningen.Perioden < 2020]

ya_zuidholland = pd.read_csv(os.path.join(yp_dir, 'Akkerbouwgewassen__productie_29112022_071427.csv'), sep=';')
ya_zuidholland = ya_zuidholland[ya_zuidholland.Gewassen == 'Tarwe (totaal)'].dropna()
ya_zuidholland = ya_zuidholland[['Gewassen', 'Perioden', "Regio's", 'Bruto opbrengst per ha (1 000 kg)']]
ya_zuidholland = ya_zuidholland.rename(columns={'Bruto opbrengst per ha (1 000 kg)': 'yield_tha'})
ya_zuidholland['Perioden'] = pd.to_numeric(ya_zuidholland.Perioden)
ya_zuidholland['yield_tha'] = pd.to_numeric(ya_zuidholland.yield_tha)
ya_zuidholland = ya_zuidholland[ya_zuidholland.Perioden < 2020]

# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------

for soil in ['clay', 'sand']:
    for yld in ['yp', 'yw']:

        # plot data
        left, width = .255, .71
        bottom, height = .25, .71
        right = left + width
        top = bottom + height
        wspace = 0.25
        hspace = 0.25
        kws_points = dict(s=100, alpha=0.9, linewidth=0.7)
        f, ((ax1, ax3), (ax5, ax)) = plt.subplots(2, 2, figsize=(6.5*2, 6.5*2))
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
        # simulated yw
        path = os.path.join(yp_dir, f".\yw-long-term-summary-{s}-co2-{soil}.xlsx")
        yw = pd.read_excel(path)
        yw['DOM'] = pd.to_datetime(yw['DOM'])
        yw['year'] = yw['DOM'].dt.year
        yw['yieldw_tha'] = yw['TWSO'] / 1000
        both = pd.merge(yp, yw, on='year', how='left')
        # genetic progress
        emmeans_eelde = pd.read_csv(os.path.join(emmeans_var, '# yp_emmeans_eelde.csv'))
        emmeans_eelde = emmeans_eelde.rename(columns={'yr_release': 'year'})
        both_sel = both[['yield_tha', 'year']].drop_duplicates()
        emmeans_eelde = pd.merge(emmeans_eelde, both_sel, on='year', how='left')
        # actual yield
        path = os.path.join(cbs_dir, r".\Wheat yields 1850-2021 for Joao.csv")
        ya = pd.read_csv(path)
        both = pd.merge(both, ya, on='year', how='left')
        both['ya_perc'] = 100 * both['ya'] / both['yield_tha']
        # --------------------------------------------------------------------------------------------------------------
        ax1.grid(linestyle='-', zorder=0, color='gainsboro')
        if(yld == 'yp'):
            y = both.yield_tha
            ax1.plot(both.year, both.yield_tha, color='darkblue', zorder=2)
            ax1.scatter(both.year, both.yield_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yp (crop model)')
            label = 'Yp (variety trials)'
        else:
            y = both.yieldw_tha
            ax1.plot(both.year, both.yieldw_tha, color='darkblue', zorder=2)
            ax1.scatter(both.year, both.yieldw_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yw (crop model)')
            label = 'Yw (variety trials)'
        X = both[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(both[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(both[["year"]].dropna()))
        slope_yp_eelde = linr_model.coef_[0].round(3)
        ax1.plot(both.year, linr_model.predict(both[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='--', zorder=5)
        new = emmeans_eelde[['year', 'emmean']].dropna()
        new = new.sort_values(by='year')
        new = new[new.year > 1970]
        y = new.emmean
        X = new[["year"]]
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(new[["year"]])
        r2 = r2_score(y_true=new.emmean, y_pred=linr_model.predict(new[["year"]].dropna()))
        slope_yexp_eelde = linr_model.coef_[0].round(3)
        ax1.plot(new.year, new.emmean, color='orangered', zorder=3)
        ax1.scatter(new.year, new.emmean, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=4, label=label)
        ax1.plot(new.year, linr_model.predict(new[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yexp_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='-.', zorder=5)
        new = ya_groningen[['Perioden', 'yield_tha']].dropna()
        new = new.sort_values(by='Perioden')
        y = new.yield_tha
        X = new[["Perioden"]]
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(new[["Perioden"]])
        ax1.plot(ya_groningen.Perioden, ya_groningen.yield_tha, color='darkred', zorder=6)
        ax1.scatter(ya_groningen.Perioden, ya_groningen.yield_tha, color='red', edgecolors='darkred', alpha=1, s=80, zorder=7, label='Ya (province stats)')
        slope_ya_eelde = linr_model.coef_[0].round(3)
        ax1.plot(new.Perioden, linr_model.predict(new[["Perioden"]]), color="darkred", label='y = {slope}x - {int}'.format(slope=slope_ya_eelde, int=abs(linr_model.intercept_).round(1)), linestyle='-', zorder=7)
        x = np.arange(1972, 2017, 1)
        a = round(66.8262045, 0)
        b = round(0.1285414, 2)
        c = round(1930.4643078, 0)
        ax1.plot(x, np.where(x < a+c, (x-c)*b, a*b), linestyle='-', linewidth=1, color='tomato', zorder=5, label=r'y = {b}x - {bc}, x < {ac}'.format(b=b, bc=round(b*c, 1), ac=int(a+c)) + '\n' + r'y = {ab}, x > {ac}'.format(ab=round(a*b, 1), ac=int(a+c)))
        ax1.scatter(both.year, both.ya, color='salmon', edgecolors='salmon', alpha=1, s=80, zorder=4, label='Ya (national stats)')
        ax1.set_ylim([0, 14])
        ax1.set_xlim([1970, 2020])
        ax1.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax1.set_yticklabels([0, 2, 4, 6, 8, 10, 12, 14], fontsize=14.5)
        ax1.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax1.set_facecolor('white')
        ax1.legend(loc='lower right', ncol=1, fontsize=11)
        ax1.set_title('A) Northeast', x=0.22, y=0.9, fontsize=16, fontweight='bold')

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        s = 'DE BILT'
        # simulated yp
        path = os.path.join(yp_dir, f".\yp-long-term-summary-{s}-co2-{soil}.xlsx")
        yp = pd.read_excel(path)
        yp['DOM'] = pd.to_datetime(yp['DOM'])
        yp['year'] = yp['DOM'].dt.year
        yp['yield_tha'] = yp['TWSO'] / 1000
        # simulated yw
        path = os.path.join(yp_dir, f".\yw-long-term-summary-{s}-co2-{soil}.xlsx")
        yw = pd.read_excel(path)
        yw['DOM'] = pd.to_datetime(yw['DOM'])
        yw['year'] = yw['DOM'].dt.year
        yw['yieldw_tha'] = yw['TWSO'] / 1000
        both = pd.merge(yp, yw, on='year', how='left')
        # genetic progress
        emmeans_debilt = pd.read_csv(os.path.join(emmeans_var, '# yp_emmeans_debilt.csv'))
        emmeans_debilt = emmeans_debilt.rename(columns={'yr_release': 'year'})
        both_sel = both[['yield_tha', 'year']].drop_duplicates()
        emmeans_debilt = pd.merge(emmeans_debilt, both_sel, on='year', how='left')
        # actual yield
        path = os.path.join(cbs_dir, r".\Wheat yields 1850-2021 for Joao.csv")
        ya = pd.read_csv(path)
        both = pd.merge(both, ya, on='year', how='left')
        both['ya_perc'] = 100 * both['ya'] / both['yield_tha']
        # --------------------------------------------------------------------------------------------------------------
        ax3.grid(linestyle='-', zorder=0, color='gainsboro')
        if (yld == 'yp'):
            y = both.yield_tha
            ax3.plot(both.year, both.yield_tha, color='darkblue', zorder=2)
            ax3.scatter(both.year, both.yield_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yp (crop model)')
            label = 'Yp (variety trials)'
        else:
            y = both.yieldw_tha
            ax3.plot(both.year, both.yieldw_tha, color='darkblue', zorder=2)
            ax3.scatter(both.year, both.yieldw_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yw (crop model)')
            label = 'Yw (variety trials)'
        X = both[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(both[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(both[["year"]].dropna()))
        slope_yp_debilt = linr_model.coef_[0].round(3)
        ax3.plot(both.year, linr_model.predict(both[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_debilt, int=abs(linr_model.intercept_).round(1)), linestyle='--', zorder=5)
        new = emmeans_debilt[['year', 'emmean']].dropna()
        new = new.sort_values(by='year')
        new = new[new.year > 1970]
        y = new.emmean
        X = new[["year"]]
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(new[["year"]])
        r2 = r2_score(y_true=new.emmean, y_pred=linr_model.predict(new[["year"]].dropna()))
        slope_yexp_debilt = linr_model.coef_[0].round(3)
        ax3.plot(new.year, new.emmean, color='orangered', zorder=3)
        ax3.scatter(new.year, new.emmean, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=4, label=label)
        ax3.plot(new.year, linr_model.predict(new[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yexp_debilt, int=abs(linr_model.intercept_).round(1)), linestyle='-.', zorder=5)
        new = ya_flevoland[['Perioden', 'yield_tha']].dropna()
        new = new.sort_values(by='Perioden')
        y = new.yield_tha
        X = new[["Perioden"]]
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(new[["Perioden"]])
        ax3.plot(ya_flevoland.Perioden, ya_flevoland.yield_tha, color='darkred', zorder=6)
        ax3.scatter(ya_flevoland.Perioden, ya_flevoland.yield_tha, color='red', edgecolors='darkred', alpha=1, s=80, zorder=7, label='Ya (province stats)')
        slope_ya_debilt = linr_model.coef_[0].round(3)
        ax3.plot(new.Perioden, linr_model.predict(new[["Perioden"]]), color="darkred", label='y = {slope}x - {int}'.format(slope=slope_ya_debilt, int=abs(linr_model.intercept_).round(1)), linestyle='-', zorder=7)
        x = np.arange(1972, 2017, 1)
        a = round(66.8262045, 0)
        b = round(0.1285414, 2)
        c = round(1930.4643078, 0)
        ax3.plot(x, np.where(x < a+c, (x-c)*b, a*b), linestyle='-', linewidth=1, color='tomato', zorder=5, label=r'y = {b}x - {bc}, x < {ac}'.format(b=b, bc=round(b*c, 1), ac=int(a+c)) + '\n' + r'y = {ab}, x > {ac}'.format(ab=round(a*b, 1), ac=int(a+c)))
        ax3.scatter(both.year, both.ya, color='salmon', edgecolors='salmon', alpha=1, s=80, zorder=4, label='Ya (national stats)')
        ax3.set_ylim([0, 14])
        ax3.set_xlim([1970, 2020])
        ax3.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax3.set_yticklabels([0, 2, 4, 6, 8, 10, 12, 14], fontsize=14.5)
        ax3.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax3.set_facecolor('white')
        ax3.legend(loc='lower right', ncol=1, fontsize=11)
        ax3.set_title('B) Central', x=0.18, y=0.9, fontsize=16, fontweight='bold')

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        s = 'VLISSINGEN'
        # simulated yp
        path = os.path.join(yp_dir, f".\yp-long-term-summary-{s}-co2-{soil}.xlsx")
        yp = pd.read_excel(path)
        yp['DOM'] = pd.to_datetime(yp['DOM'])
        yp['year'] = yp['DOM'].dt.year
        yp['yield_tha'] = yp['TWSO'] / 1000
        # simulated yw
        path = os.path.join(yp_dir, f".\yw-long-term-summary-{s}-co2-{soil}.xlsx")
        yw = pd.read_excel(path)
        yw['DOM'] = pd.to_datetime(yw['DOM'])
        yw['year'] = yw['DOM'].dt.year
        yw['yieldw_tha'] = yw['TWSO'] / 1000
        both = pd.merge(yp, yw, on='year', how='left')
        # genetic progress
        emmeans_vlissingen = pd.read_csv(os.path.join(emmeans_var, '# yp_emmeans_vlissingen.csv'))
        emmeans_vlissingen = emmeans_vlissingen.rename(columns={'yr_release': 'year'})
        both_sel = both[['yield_tha', 'year']].drop_duplicates()
        emmeans_vlissingen = pd.merge(emmeans_vlissingen, both_sel, on='year', how='left')
        # actual yield
        path = os.path.join(cbs_dir, r".\Wheat yields 1850-2021 for Joao.csv")
        ya = pd.read_csv(path)
        both = pd.merge(both, ya, on='year', how='left')
        both['ya_perc'] = 100 * both['ya'] / both['yield_tha']
        # --------------------------------------------------------------------------------------------------------------
        ax5.grid(linestyle='-', zorder=0, color='gainsboro')
        if (yld == 'yp'):
            y = both.yield_tha
            ax5.plot(both.year, both.yield_tha, color='darkblue', zorder=2)
            ax5.scatter(both.year, both.yield_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yp (crop model)')
            label = 'Yp (variety trials)'
        else:
            y = both.yieldw_tha
            ax5.plot(both.year, both.yieldw_tha, color='darkblue', zorder=2)
            ax5.scatter(both.year, both.yieldw_tha, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='Yw (crop model)')
            label = 'Yw (variety trials)'
        X = both[["year"]].dropna()
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(both[["year"]].dropna())
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        r2 = r2_score(y_true=y, y_pred=linr_model.predict(both[["year"]].dropna()))
        slope_yp_vlissingen = linr_model.coef_[0].round(3)
        ax5.plot(both.year, linr_model.predict(both[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yp_vlissingen, int=abs(linr_model.intercept_).round(1)), linestyle='--', zorder=5)
        new = emmeans_vlissingen[['year', 'emmean']].dropna()
        new = new.sort_values(by='year')
        new = new[new.year > 1970]
        y = new.emmean
        X = new[["year"]]
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(new[["year"]])
        r2 = r2_score(y_true=new.emmean, y_pred=linr_model.predict(new[["year"]].dropna()))
        slope_yexp_vlissingen = linr_model.coef_[0].round(3)
        ax5.plot(new.year, new.emmean, color='orangered', zorder=3)
        ax5.scatter(new.year, new.emmean, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=4, label=label)
        ax5.plot(new.year, linr_model.predict(new[["year"]]), color="black", label='y = {slope}x - {int}'.format(slope=slope_yexp_vlissingen, int=abs(linr_model.intercept_).round(1)), linestyle='-.', zorder=5)
        new = ya_zuidholland[['Perioden', 'yield_tha']].dropna()
        new = new.sort_values(by='Perioden')
        y = new.yield_tha
        X = new[["Perioden"]]
        linr_model = LinearRegression().fit(X, y)
        linr_model.coef_
        linr_model.intercept_
        linr_model.predict(new[["Perioden"]])
        ax5.plot(ya_zuidholland.Perioden, ya_zuidholland.yield_tha, color='darkred', zorder=6)
        ax5.scatter(ya_zuidholland.Perioden, ya_zuidholland.yield_tha, color='red', edgecolors='darkred', alpha=1, s=80, zorder=7, label='Ya (province stats)')
        slope_ya_vlissingen = linr_model.coef_[0].round(3)
        ax5.plot(new.Perioden, linr_model.predict(new[["Perioden"]]), color="darkred", label='y = {slope}x - {int}'.format(slope=slope_ya_vlissingen, int=abs(linr_model.intercept_).round(1)), linestyle='-', zorder=7)
        x = np.arange(1972, 2017, 1)
        a = round(66.8262045, 0)
        b = round(0.1285414, 2)
        c = round(1930.4643078, 0)
        ax5.plot(x, np.where(x < a+c, (x-c)*b, a*b), linestyle='-', linewidth=1, color='tomato', zorder=5, label=r'y = {b}x - {bc}, x < {ac}'.format(b=b, bc=round(b*c, 1), ac=int(a+c)) + '\n' + r'y = {ab}, x > {ac}'.format(ab=round(a*b, 1), ac=int(a+c)))
        ax5.scatter(both.year, both.ya, color='salmon', edgecolors='salmon', alpha=1, s=80, zorder=4, label='Ya (national stats)')
        ax5.set_ylim([0, 14])
        ax5.set_xlim([1970, 2020])
        ax5.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=15, rotation=45)
        ax5.set_yticklabels([0, 2, 4, 6, 8, 10, 12, 14], fontsize=14.5)
        ax5.set_ylabel('Wheat yield (t/ha)', fontsize=16)
        ax5.set_facecolor('white')
        ax5.legend(loc='lower right', ncol=1, fontsize=11)
        ax5.set_title('C) Southwest', x=0.23, y=0.9, fontsize=16, fontweight='bold')

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        x = ['Northeast', 'Central', 'Southwest']
        ### slopes were obtained from the regressions fitted in R for the 1994-2016 period
        current = [51.58, 45.26, -7.12]
        genetic = [73.81, 83.76, 81.24]
        climate = [44.78, 59.96, 25.94]
        agronomy = [(current[0] - genetic[0] - climate[0]), (current[1] - genetic[1] - climate[1]), (current[2] - genetic[2] - climate[2])]
        c_and_g = [(current[0] + genetic[0]), (current[1] + genetic[1]), (0 + genetic[2])]
        ### directly from the regressions fitted in earlier sections of this script
        # current = [slope_ya_eelde*1000, slope_ya_debilt*1000, slope_ya_vlissingen*1000]
        # genetic = [slope_yexp_eelde*1000, slope_yexp_debilt*1000, slope_yexp_vlissingen*1000]
        # climate = [slope_yp_eelde*1000, slope_yp_debilt*1000, slope_yp_vlissingen*1000]
        # agronomy = [(slope_ya_eelde-slope_yexp_eelde-slope_yp_eelde)*1000, (slope_ya_debilt-slope_yexp_debilt-slope_yp_debilt)*1000, (slope_ya_vlissingen-slope_yexp_vlissingen-slope_yp_vlissingen)*1000]
        # c_and_g = [(slope_ya_eelde+slope_yexp_eelde)*1000, (slope_ya_debilt+slope_yexp_debilt)*1000, (slope_ya_vlissingen+slope_yexp_vlissingen)*1000]
        ax.grid(linestyle='-', zorder=0, color='gainsboro')
        ax.bar(x, current, color='red', edgecolor='black', label='Farm yields', zorder=3)
        ax.bar(x, genetic, bottom=[51.58, 45.26, 0], color='orange', edgecolor='black', label='Genetics', zorder=3)
        ax.bar(x, climate, bottom=c_and_g, color='royalblue', edgecolor='black', label='Climate', zorder=3)
        ax.bar(x, agronomy, bottom=[0, 0, current[2]], color='forestgreen', edgecolor='black', label='Agronomy', zorder=3)
        ax.set_ylim([-150, 250])
        ax.axhline(0, color='black', zorder=6)
        ax.set_ylabel('Yield gains (kg/ha/yr)', family='sans-serif', fontsize=17, color='black')
        ax.set_yticklabels([-150, -100, -50, 0, 50, 100, 150, 200, 250], family='sans-serif', fontsize=16, color='black')
        ax.set_xticklabels(['Northeast', 'Central', 'Southwest'], family='sans-serif', fontsize=16, color='black')
        ax.set_facecolor('white')
        # =====
        ax.text(-0.1, 10, round(current[0], 1), fontsize=15)
        ax.text(-0.1, 70, round(genetic[0], 1), fontsize=15)
        ax.text(-0.1, 140, round(climate[0], 1), fontsize=15)
        ax.text(-0.175, -50, round((current[0]-genetic[0]-climate[0]), 1), fontsize=15)
        # ax.text(-0.1, 20, slope_ya_eelde * 1000, fontsize=15)
        # ax.text(-0.1, 100, slope_yexp_eelde * 1000, fontsize=15)
        # ax.text(-0.1, 167, slope_yp_eelde * 1000, fontsize=15)
        # ax.text(-0.175, -58, round((slope_ya_eelde - slope_yexp_eelde - slope_yp_eelde) * 1000, 1), fontsize=15)
        # =====
        ax.text(0.9, 10, round(current[1], 1), fontsize=15)
        ax.text(0.9, 70, round(genetic[1], 1), fontsize=15)
        ax.text(0.9, 140, round(climate[1], 1), fontsize=15)
        ax.text(0.85, -50, round((current[1]-genetic[1]-climate[1]), 1), fontsize=15)
        # ax.text(0.9, 20, slope_ya_debilt*1000, fontsize=15)
        # ax.text(0.9, 92, slope_yexp_debilt*1000, fontsize=15)
        # ax.text(0.9, 167, slope_yp_debilt*1000, fontsize=15)
        # ax.text(0.85, -58, round((slope_ya_debilt-slope_yexp_debilt-slope_yp_debilt)*1000, 1), fontsize=15)
        # =====
        ax.text(0.9+1.05, -9, round(current[2], 1), fontsize=15)
        ax.text(0.9+1, 40, round(genetic[2], 1), fontsize=15)
        ax.text(0.9+1, 87, round(climate[2], 1), fontsize=15)
        ax.text(0.77+1, -50, round((current[2]-genetic[2]-climate[2]), 1), fontsize=15)
        # ax.text(0.9+1.02, 0, slope_ya_vlissingen*1000, fontsize=15)
        # ax.text(0.9+1, 45, slope_yexp_vlissingen*1000, fontsize=15)
        # ax.text(0.9+1, 107, slope_yp_vlissingen*1000, fontsize=15)
        # ax.text(0.825+1, -67, round((slope_ya_vlissingen-slope_yexp_vlissingen-slope_yp_vlissingen)*1000, 1), fontsize=15)
        # =====
        ax.legend(loc='upper right', fontsize=12, ncol=1)
        ax.set_title('D)', x=0.075, y=0.9, fontsize=16, fontweight='bold')

        # ------------------------------------------------------------------------------------------------------------------
        if(yld == 'yp'):
            f.savefig(os.path.join(yp_dir, f"figure1-wheat-trends-{yld}.png"), bbox_inches='tight', dpi=1000)
        else:
            f.savefig(os.path.join(yp_dir, f"figure1-wheat-trends-{yld}-{soil}.png"), bbox_inches='tight', dpi=1000)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
