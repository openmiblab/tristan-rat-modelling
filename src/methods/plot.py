import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydmr


resultspath = os.path.join(os.getcwd(), 'build')
figpath = os.path.join(resultspath, 'Figs')
if not os.path.exists(figpath):
    os.makedirs(figpath)


# Loop over all studies
drugs = ['Asunaprevir','Bosentan','Cyclosporine','Ketoconazole',
        'Pioglitazone','Rifampicin','Placebo']


def lines():

    # Set up the figure
    clr = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
        'tab:brown']
    fs = 10
    fig, ax = plt.subplots(2, len(drugs), figsize=(len(drugs)*1.5, 8))
    fig.subplots_adjust(wspace=0.2, hspace=0.1)

    for i, drug in enumerate(drugs):

        # Set up subfigures for the study
        ax[0,i].set_title(drug, fontsize=fs, pad=10)
        ax[0,i].set_ylim(0, 300)
        ax[0,i].set_xticklabels([])
        ax[1,i].set_ylim(0, 30)
        ax[1,i].set_xticklabels([])
        if i==0:
            ax[0,i].set_ylabel('khe (mL/min/100mL)', fontsize=fs)
            ax[0,i].tick_params(axis='y', labelsize=fs)
            ax[1,i].set_ylabel('kbh (mL/min/100mL)', fontsize=fs)
            ax[1,i].tick_params(axis='y', labelsize=fs)
        else:
            ax[0,i].set_yticklabels([])
            ax[1,i].set_yticklabels([])

        file = os.path.join(resultspath, f'tristan_rats_healthy_{drug.lower()}_all_results')
        dmr = pydmr.read(file, 'nest')

        # Plot the rate constants in units of mL/min/100mL
        for s in dmr['pars'].keys():
            studies = list(dmr['pars'][s].keys())
            x = [1]
            khe = [6000*dmr['pars'][s][studies[0]]['khe']]
            kbh = [6000*dmr['pars'][s][studies[0]]['kbh']] 
            if len(studies)==2:
                x += [2]
                khe += [6000*dmr['pars'][s][studies[1]]['khe']]
                kbh += [6000*dmr['pars'][s][studies[1]]['kbh']] 
            color = clr[int(s[-2:])-1]
            ax[0,i].plot(x, khe, '-', label=s, marker='o', markersize=6, 
                        color=color)
            ax[1,i].plot(x, kbh, '-', label=s, marker='o', markersize=6, 
                        color=color)

    plt.savefig(fname=os.path.join(figpath, 'six_compounds_lineplot'))



def averages():

    # Set up figure
    fs = 10
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(len(drugs), 5))
    fig.subplots_adjust(left=0.3, right=0.7, wspace=0.25)

    ax0.set_title('khe effect (%)', fontsize=fs, pad=10)
    ax1.set_title('kbh effect (%)', fontsize=fs, pad=10)
    ax0.set_xlim(-100, 50)
    ax1.set_xlim(-100, 50)
    ax0.grid(which='major', axis='x', linestyle='-')
    ax1.grid(which='major', axis='x', linestyle='-')
    ax1.set_yticklabels([])

    # Loop over all studies
    for i, drug in enumerate(drugs):

        file = os.path.join(resultspath, f'tristan_rats_healthy_{drug.lower()}_all_results')

        # Pivot data for both visits of the study for easy access:
        dmr = pydmr.read(file, 'pandas', study='Day_1')
        v1 = pd.pivot_table(dmr['pars'], values='value', 
                            columns='parameter', index='subject')
        dmr = pydmr.read(file, 'pandas', study='Day_2')
        v2 = pd.pivot_table(dmr['pars'], values='value', 
                            columns='parameter', index='subject')
        
        # Calculate effect size for the drug in %
        effect = 100*(v2-v1)/v1

        # Get descriptive statistics
        stats = effect.describe()

        # Calculate mean effect sizes and 59% CI on the mean.
        khe_eff = stats.at['mean','khe']
        kbh_eff = stats.at['mean','kbh']
        khe_eff_err = 1.96*stats.at['std','khe']/np.sqrt(stats.at['count','khe'])
        kbh_eff_err = 1.96*stats.at['std','kbh']/np.sqrt(stats.at['count','kbh'])

        # Plot mean effect size for khe along with 95% CI
        # Choose color based on magnitude of effect
        if khe_eff + khe_eff_err < -20:
            clr = 'tab:red'
        elif khe_eff + khe_eff_err < 0:
            clr = 'tab:orange'
        else:
            clr = 'tab:green'
        ax0.errorbar(khe_eff, drugs[i], xerr=khe_eff_err, fmt='o', color=clr)

        # Plot mean effect size for kbh along with 95% CI
        # Choose color based on magnitude of effect
        if kbh_eff + kbh_eff_err < -20:
            clr = 'tab:red'
        elif kbh_eff + kbh_eff_err < 0:
            clr = 'tab:orange'
        else:
            clr = 'tab:green'
        ax1.errorbar(kbh_eff, drugs[i], xerr=kbh_eff_err, fmt='o', color=clr)

    # Plot dummy values out of range to show a legend
    ax1.errorbar(-200, drugs[0], 
                marker='o', 
                color='tab:red', 
                label='inhibition > 20%')
    ax1.errorbar(-200, drugs[0], 
                marker='o', 
                color='tab:orange', 
                label='inhibition')
    ax1.errorbar(-200, drugs[0], 
                marker='o', 
                color='tab:green', 
                label='no inhibition')
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.savefig(fname=os.path.join(figpath, 'six_compounds_averages'))




if __name__ == '__main__':
    lines()
    averages()
