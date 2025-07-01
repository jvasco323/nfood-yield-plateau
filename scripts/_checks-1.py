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
        # plots

        left, width = .255, .71
        bottom, height = .25, .71
        right = left + width
        top = bottom + height
        wspace = 0.25
        hspace = 0.25
        kws_points = dict(s=100, alpha=0.9, linewidth=0.7)
        # --------------------------------------------------------------------------------------------------------------
        f, ((ax3, ax4), (ax5, ax6)) = plt.subplots(2, 2, figsize=(11, 6*1.8))
        axes = plt.gca()
        f.subplots_adjust(wspace=wspace, hspace=hspace)
        # --------------------------------------------------------------------------------------------------------------
        ax3.grid(linestyle='-', zorder=0)
        ax3.plot(summary_eelde.year, summary_eelde.TAGP/1000, color='orangered', zorder=2)
        ax3.scatter(summary_eelde.year, summary_eelde.TAGP/1000, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Eelde')
        ax3.plot(summary_debilt.year, summary_debilt.TAGP/1000, color='darkblue', zorder=2)
        ax3.scatter(summary_debilt.year, summary_debilt.TAGP/1000, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='De Bilt')
        ax3.plot(summary_vlissingen.year, summary_vlissingen.TAGP/1000, color='darkred', zorder=2)
        ax3.scatter(summary_vlissingen.year, summary_vlissingen.TAGP/1000, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Vlissingen')
        ax3.set_ylim([12, 28])
        ax3.set_xlim([1970, 2020])
        ax3.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=13.5)
        ax3.set_yticks([12, 16, 20, 24, 28])
        ax3.set_yticklabels([12, 16, 20, 24, 28], fontsize=14)
        ax3.set_ylabel('Aboveground biomass (t/ha)', fontsize=15)
        ax3.set_facecolor('whitesmoke')
        ax3.legend(loc='lower right', fontsize=12)
        # --------------------------------------------------------------------------------------------------------------
        ax4.grid(linestyle='-', zorder=0)
        ax4.scatter(summary_eelde.TAGP/1000, summary_eelde.yp, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Eelde')
        ax4.scatter(summary_debilt.TAGP/1000, summary_debilt.yp, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='De Bilt')
        ax4.scatter(summary_vlissingen.TAGP/1000, summary_vlissingen.yp, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Vlissingen')
        ax4.set_ylim([6, 14])
        ax4.set_xlim([12, 28])
        ax4.set_yticks([6, 8, 10, 12, 14])
        ax4.set_yticklabels([6, 8, 10, 12, 14], fontsize=13.5)
        ax4.set_xticks([12, 16, 20, 24, 28])
        ax4.set_xticklabels([12, 16, 20, 24, 28], fontsize=14)
        ax4.set_xlabel('Aboveground biomass (t/ha)', fontsize=15)
        ax4.set_ylabel('Wheat yield (t/ha)', fontsize=15)
        ax4.set_facecolor('whitesmoke')
        ax4.legend(loc='lower right', fontsize=12)
        # --------------------------------------------------------------------------------------------------------------
        ax5.grid(linestyle='-', zorder=0)
        ax5.plot(summary_eelde.year, summary_eelde.hi, color='orangered', zorder=2)
        ax5.scatter(summary_eelde.year, summary_eelde.hi, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Eelde')
        ax5.plot(summary_debilt.year, summary_debilt.hi, color='darkblue', zorder=2)
        ax5.scatter(summary_debilt.year, summary_debilt.hi, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='De Bilt')
        ax5.plot(summary_vlissingen.year, summary_vlissingen.hi, color='darkred', zorder=2)
        ax5.scatter(summary_vlissingen.year, summary_vlissingen.hi, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Vlissingen')
        ax5.set_ylim([40, 60])
        ax5.set_xlim([1970, 2020])
        ax5.set_xticklabels([1970, 1980, 1990, 2000, 2010, 2020], fontsize=13.5)
        ax5.set_yticks([40, 44, 48, 52, 56, 60])
        ax5.set_yticklabels([40, 44, 48, 52, 56, 60], fontsize=14)
        ax5.set_ylabel('Havest index (%)', fontsize=15)
        ax5.set_facecolor('whitesmoke')
        ax5.legend(loc='lower right', fontsize=12)
        # --------------------------------------------------------------------------------------------------------------
        ax6.grid(linestyle='-', zorder=0)
        ax6.scatter(summary_eelde.hi, summary_eelde.yp, color='orange', edgecolors='orangered', alpha=1, s=80, zorder=3, label='Eelde')
        ax6.scatter(summary_debilt.hi, summary_debilt.yp, color='royalblue', edgecolors='darkblue', alpha=1, s=80, zorder=3, label='De Bilt')
        ax6.scatter(summary_vlissingen.hi, summary_vlissingen.yp, color='salmon', edgecolors='darkred', alpha=1, s=80, zorder=3, label='Vlissingen')
        ax6.set_ylim([6, 14])
        ax6.set_xlim([40, 60])
        ax6.set_yticks([6, 8, 10, 12, 14])
        ax6.set_yticklabels([6, 8, 10, 12, 14], fontsize=13.5)
        ax6.set_xticks([40, 44, 48, 52, 56, 60])
        ax6.set_xticklabels([40, 44, 48, 52, 56, 60], fontsize=14)
        ax6.set_xlabel('Harvest index (%)', fontsize=15)
        ax6.set_ylabel('Wheat yield (t/ha)', fontsize=15)
        ax6.set_facecolor('whitesmoke')
        ax6.legend(loc='lower right', fontsize=12)
        # --------------------------------------------------------------------------------------------------------------
        if (yld == 'yp'):
            f.savefig(os.path.join(dir, f"yield-vs-growth-{yld}.png"), bbox_inches='tight', dpi=1000)
        else:
            f.savefig(os.path.join(dir, f"yield-vs-growth-{yld}-{soil}.png"), bbox_inches='tight', dpi=1000)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

stations = ['DE BILT', 'EELDE', 'VLISSINGEN']
for s in stations:
    for soil in ['clay', 'sand']:
        for yld in ['yp', 'yw']:
            daily = pd.read_excel(os.path.join(dir, "{yld}-long-term-daily-{s}-co2-{soil}.xlsx".format(yld=yld, s=s, soil=soil)))
            # ----------------------------------------------------------------------------------------------------------
            left, width = .255, .71
            bottom, height = .25, .71
            right = left + width
            top = bottom + height
            wspace = 0.25
            hspace = 0.25
            kws_points = dict(s=100, alpha=0.9, linewidth=0.7)
            # ----------------------------------------------------------------------------------------------------------
            f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(13.5, 13.5))
            axes = plt.gca()
            f.subplots_adjust(wspace=wspace, hspace=hspace)
            # ----------------------------------------------------------------------------------------------------------
            ax1.grid(linestyle='-', zorder=0)
            ax1.plot(daily.DVS, daily.WLV/1000, color='darkblue', zorder=2, label='')
            ax1.scatter(daily.DVS, daily.WLV/1000, color='royalblue', edgecolors='darkblue', alpha=1, s=20, zorder=3, label='')
            ax1.set_ylim([0, 4])
            ax1.set_xlim([0, 2])
            ax1.set_xticklabels([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], fontsize=13.5)
            ax1.set_yticklabels([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4], fontsize=14)
            ax1.set_ylabel('Leaf biomass (t/ha)', fontsize=15)
            ax1.set_xlabel('Development stage (DVS, -)', fontsize=15)
            ax1.set_facecolor('whitesmoke')
            # ----------------------------------------------------------------------------------------------------------
            ax2.grid(linestyle='-', zorder=0)
            ax2.plot(daily.DVS, daily.LAI, color='darkblue', zorder=2, label='')
            ax2.scatter(daily.DVS, daily.LAI, color='royalblue', edgecolors='darkblue', alpha=1, s=20, zorder=3, label='')
            ax2.set_ylim([0, 7])
            ax2.set_xlim([0, 2])
            ax2.set_xticklabels([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], fontsize=13.5)
            ax2.set_yticklabels([0, 1, 2, 3, 4, 5, 6, 7], fontsize=14)
            ax2.set_ylabel('Leaf area index (cm2/cm2)', fontsize=15)
            ax2.set_xlabel('Development stage (DVS, -)', fontsize=15)
            ax2.set_facecolor('whitesmoke')
            # ----------------------------------------------------------------------------------------------------------
            ax3.grid(linestyle='-', zorder=0)
            ax3.plot(daily.DVS, daily.WST/1000, color='darkblue', zorder=2, label='')
            ax3.scatter(daily.DVS, daily.WST/1000, color='royalblue', edgecolors='darkblue', alpha=1, s=20, zorder=3, label='')
            ax3.set_ylim([0, 14])
            ax3.set_xlim([0, 2])
            ax3.set_xticklabels([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], fontsize=13.5)
            ax3.set_yticklabels([0, 2, 4, 6, 8, 10, 12, 14], fontsize=14)
            ax3.set_ylabel('Stem biomass (t/ha)', fontsize=15)
            ax3.set_xlabel('Development stage (DVS, -)', fontsize=15)
            ax3.set_facecolor('whitesmoke')
            # ----------------------------------------------------------------------------------------------------------
            ax4.grid(linestyle='-', zorder=0)
            ax4.plot(daily.DVS, daily.WSO/1000, color='darkblue', zorder=2, label='')
            ax4.scatter(daily.DVS, daily.WSO/1000, color='royalblue', edgecolors='darkblue', alpha=1, s=20, zorder=3, label='')
            ax4.set_ylim([0, 14])
            ax4.set_xlim([0, 2])
            ax4.set_xticklabels([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], fontsize=13.5)
            ax4.set_yticklabels([0, 2, 4, 6, 8, 10, 12, 14], fontsize=14)
            ax4.set_ylabel('Grain biomass (t/ha)', fontsize=15)
            ax4.set_xlabel('Development stage (DVS, -)', fontsize=15)
            ax4.set_facecolor('whitesmoke')
            # ----------------------------------------------------------------------------------------------------------
            if (yld == 'yp'):
                f.savefig(os.path.join(dir, f"yield-vs-biomass-dynamics-{s}-{yld}.png".format(yld=yld, s=s, soil=soil)), bbox_inches='tight', dpi=1000)
            else:
                f.savefig(os.path.join(dir, f"yield-vs-biomass-dynamics-{s}-{yld}-{soil}.png".format(yld=yld, s=s, soil=soil)), bbox_inches='tight', dpi=1000)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
