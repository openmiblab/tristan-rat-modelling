import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pydmr
import miblab

resultspath = os.path.join(os.getcwd(), 'build')
datapath = os.path.join(resultspath, 'output_data')
figpath = os.path.join(resultspath, 'figures')
if not os.path.exists(figpath):
    os.makedirs(figpath)
tablespath = os.path.join(resultspath, 'tables')



def pick_color(n, k):
    """
    Pick a distinctive color for matplotlib plotting.
    
    Parameters
    ----------
    n : int
        Total number of colors needed.
    k : int
        Index of the desired color (0 <= k < n).
    
    Returns
    -------
    tuple
        RGB tuple usable in matplotlib.
    
    Example
    -------
    import matplotlib.pyplot as plt
    
    n = 10
    for k in range(n):
        plt.plot(range(10), np.random.rand(10) + k, 
                 color=pick_color(n, k), linewidth=3)
    plt.show()
    """
    if not (0 <= k < n):
        raise ValueError("k must be in range [0, n-1]")

    # Evenly spaced hues in HSV
    hues = np.linspace(0, 1, n, endpoint=False)
    hsv_color = (hues[k], 0.75, 0.9)  # hue, saturation, value
    return mcolors.hsv_to_rgb(hsv_color)



def six_compound_data():

    studies = [
        'study_05_single_asunaprevir',
        'study_06_single_pioglitazone',
        'study_07_single_ketoconazole',
        'study_08_single_cyclosporine',
        'study_10_single_bosentan',
        'study_12_single_rifampicin',
    ]

    # Set up the figure
    clr = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
        'tab:brown']
    fs = 10
    fig, ax = plt.subplots(2, len(studies), figsize=(len(studies)*1.5, 8))
    fig.subplots_adjust(wspace=0.2, hspace=0.1)

    for i, study in enumerate(studies):

        drug = study[16:]

        # Set up subfigures for the study
        ax[0,i].set_title(drug, fontsize=fs, pad=10)
        ax[0,i].set_ylim(0, 150)
        ax[0,i].set_xticklabels([])
        ax[1,i].set_ylim(0, 40)
        ax[1,i].set_xticklabels([])
        if i==0:
            ax[0,i].set_ylabel('Ktrans (mL/min/100cm3)', fontsize=fs)
            ax[0,i].tick_params(axis='y', labelsize=fs)
            ax[1,i].set_ylabel('kbh (mL/min/100cm3)', fontsize=fs)
            ax[1,i].tick_params(axis='y', labelsize=fs)
        else:
            ax[0,i].set_yticklabels([])
            ax[1,i].set_yticklabels([])

        file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')
        dmr = pydmr.read(file, 'nest')

        # Plot the rate constants in units of mL/min/100mL
        for s in dmr['pars'].keys():
            studies = list(dmr['pars'][s].keys())
            x = [1]
            khe = [6000*dmr['pars'][s][studies[0]]['Ktrans']]
            kbh = [6000*dmr['pars'][s][studies[0]]['kbh']] 
            if len(studies)==2:
                x += [2]
                khe += [6000*dmr['pars'][s][studies[1]]['Ktrans']]
                kbh += [6000*dmr['pars'][s][studies[1]]['kbh']] 
            color = clr[int(s[-2:])-1]
            ax[0,i].plot(x, khe, '-', label=s, marker='o', markersize=6, 
                        color=color)
            ax[1,i].plot(x, kbh, '-', label=s, marker='o', markersize=6, 
                        color=color)

    plt.savefig(fname=os.path.join(figpath, 'data_05-08_10_12_six_compounds'))


def six_compound_effect_sizes():

    studies = [
        'study_05_single_asunaprevir',
        'study_06_single_pioglitazone',
        'study_07_single_ketoconazole',
        'study_08_single_cyclosporine',
        'study_10_single_bosentan',
        'study_12_single_rifampicin',
    ]

    # Set up figure
    fs = 10
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(len(studies), 5))
    fig.subplots_adjust(left=0.3, right=0.7, wspace=0.25)

    ax0.set_title('Ktrans effect (%)', fontsize=fs, pad=10)
    ax1.set_title('kbh effect (%)', fontsize=fs, pad=10)
    ax0.set_xlim(-100, 50)
    ax1.set_xlim(-100, 50)
    ax0.grid(which='major', axis='x', linestyle='-')
    ax1.grid(which='major', axis='x', linestyle='-')
    ax1.set_yticklabels([])

    # Loop over all studies
    for i, study in enumerate(studies):

        drug = study[16:]

        stats = pd.read_csv(os.path.join(tablespath, f'{study}_effect_sizes.csv'))
        stats = stats.set_index('parameter')

        # Calculate mean effect sizes and 59% CI on the mean.
        khe_eff = stats.at['mean','Ktrans']
        kbh_eff = stats.at['mean','kbh']
        khe_eff_err = 1.96*stats.at['std','Ktrans']/np.sqrt(stats.at['count','Ktrans'])
        kbh_eff_err = 1.96*stats.at['std','kbh']/np.sqrt(stats.at['count','kbh'])

        # Plot mean effect size for khe along with 95% CI
        # Choose color based on magnitude of effect
        if khe_eff + khe_eff_err < -20:
            clr = 'tab:red'
        elif khe_eff + khe_eff_err < 0:
            clr = 'tab:orange'
        else:
            clr = 'tab:green'
        ax0.errorbar(khe_eff, drug, xerr=khe_eff_err, fmt='o', color=clr)

        # Plot mean effect size for kbh along with 95% CI
        # Choose color based on magnitude of effect
        if kbh_eff + kbh_eff_err < -20:
            clr = 'tab:red'
        elif kbh_eff + kbh_eff_err < 0:
            clr = 'tab:orange'
        else:
            clr = 'tab:green'
        ax1.errorbar(kbh_eff, drug, xerr=kbh_eff_err, fmt='o', color=clr)

    # Plot dummy values out of range to show a legend
    ax1.errorbar(-200, drug, 
                marker='o', 
                color='tab:red', 
                label='inhibition > 20%')
    ax1.errorbar(-200, drug, 
                marker='o', 
                color='tab:orange', 
                label='inhibition')
    ax1.errorbar(-200, drug, 
                marker='o', 
                color='tab:green', 
                label='no inhibition')
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.savefig(fname=os.path.join(figpath, 'six_compounds_effect_sizes'))




def chronic_cyclosporine():

    fs = 10
    fig, ax = plt.subplots(2, 2, figsize=(2*2.5, 2*2.5))
    fig.subplots_adjust(wspace=0.25, hspace=0.25)

    # high dose khe
    arms = ['Cyclosporine (clinical dose)', 'Placebo']
    clr = {arms[0]:'b', arms[1]:'g'}
    for j, arm in enumerate(arms):
        ax[0,j].set_title(arm, fontsize=fs, pad=10)
        ax[1,j].set_xlabel('Day')
    for i, parameter in enumerate(['Ktrans', 'kbh']):
        ax[i,0].set_ylabel(parameter + ' (mL/min/100cm3)')
    #ylim = {'khe': (0,0.02), 'kbh':(0,0.003)}
    ylim = {'Ktrans': (0,150), 'kbh':(0,40)}
    for i, parameter in enumerate(['Ktrans', 'kbh']):
        for j, arm in enumerate(arms):
            df = pd.read_csv(os.path.join(tablespath, f'study_15_{arm}.csv'))
            avr = df[f'{parameter} avr']
            err = df[f'{parameter} err']
            days = range(len(avr))
            ax[i,j].set_xticks(days)
            ax[i,j].set_ylim(ylim[parameter])
            ax[i,j].plot(days, 6000*avr, '-', label=arm, 
                         marker='o', markersize=6, color=clr[arm])
            ax[i,j].errorbar(days, 6000*avr, yerr=6000*err, fmt='o', color=clr[arm])

    plt.savefig(fname=os.path.join(figpath, 'data_15_chronic_cyclosporine'))


def chronic_rifampicin():

    fs = 10
    fig, ax = plt.subplots(2, 3, figsize=(3*2.5, 2*2.5))
    fig.subplots_adjust(wspace=0.25, hspace=0.25)

    # high dose khe
    groups = ['Rifampicin (high dose)', 'Rifampicin (clinical dose)', 'Rifampicin (placebo)']
    clr = {groups[0]:'r', groups[1]:'b', groups[2]:'g'}
    for j, group in enumerate(groups):
        ax[0,j].set_title(group, fontsize=fs, pad=10)
        ax[1,j].set_xlabel('Day')
    for i, parameter in enumerate(['Ktrans', 'kbh']):
        ax[i,0].set_ylabel(parameter + ' (mL/min/100cm3)')
    #ylim = {'khe': (0,0.02), 'kbh':(0,0.003)}
    ylim = {'Ktrans': (0,150), 'kbh': (0,40)}
    for i, parameter in enumerate(['Ktrans', 'kbh']):
        for j, group in enumerate(groups):
            df = pd.read_csv(os.path.join(tablespath, f'study_14_{group}.csv'))
            avr = df[f'{parameter} avr']
            err = df[f'{parameter} err']
            days = range(len(avr))
            ax[i,j].set_xticks(days)
            ax[i,j].set_ylim(ylim[parameter])
            ax[i,j].plot(days, 6000*avr, '-', label=group, 
                         marker='o', markersize=6, color=clr[group])
            ax[i,j].errorbar(days, 6000*avr, yerr=6000*err, fmt='o', color=clr[group])

    plt.savefig(fname=os.path.join(figpath, 'data_14_chronic_rifampicin'))



def reproducibility():

    df = pd.read_csv(os.path.join(tablespath, 'reproducibility.csv'))

    fs = 10
    fig, ax = plt.subplots(2, 2, figsize=(2*4, 2*3))
    fig.subplots_adjust(wspace=0.25, hspace=0.25, bottom=0.2)
    studies = 1 + np.arange(len(df))

    it = [
        (0, 0, 'Ktrans', 'mL/min/100cm3', (0,150)), 
        (1, 0, 'khe', 'mL/min/100cm3', (0,1000)), 
        (0, 1, 'kbh', 'mL/min/100cm3', (0,40)), 
        (1, 1, 'E', '%', (0,100)),
    ]
    for i, j, parameter, unit, ylim in it:
        avr = df[f'{parameter} avr']
        err = df[f'{parameter} err']
        avr_mean = np.mean(avr)
        avr_err = 1.96*np.std(avr)/np.sqrt(len(studies))
        ax[i,j].plot(studies, 0*studies + avr_mean, linestyle='-', color='k')
        ax[i,j].plot(studies, 0*studies + avr_mean - avr_err, linestyle='--', color='grey')
        ax[i,j].plot(studies, 0*studies + avr_mean + avr_err, linestyle='--', color='grey')
        ax[i,j].set_xticks(studies)
        ax[i,j].set_ylim(ylim)
        ax[i,j].errorbar(studies, avr, yerr=err, fmt='o', color='r', markersize=4)
        ax[i,j].set_xlabel('Study')
        ax[i,j].set_ylabel(f"{parameter} ({unit})")

    plt.savefig(fname=os.path.join(figpath, 'reproducibility'))


def bosentan_data():

    studies = [
        'study_10_single_bosentan',
        'study_09_single_bosentan_high',
        'study_11_chronic_bosentan_placebo',
    ]
    plot_title = {
        0: 'clinical dose',
        1: 'high dose',
        2: 'chronic dose',
    }

    # Set up the figure
    clr = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
            'tab:brown']
    fs = 10
    fig, ax = plt.subplots(2, len(studies), figsize=(len(studies)*1.5, 8))
    fig.subplots_adjust(wspace=0.2, hspace=0.1)

    for i, study in enumerate(studies):

        drug = plot_title[i]

        # Set up subfigures for the study
        ax[0,i].set_title(drug, fontsize=fs, pad=10)
        ax[0,i].set_ylim(0, 150)
        ax[0,i].set_xticklabels([])
        ax[1,i].set_ylim(0, 40)
        ax[1,i].set_xticklabels([])
        if i==0:
            ax[0,i].set_ylabel('Ktrans (mL/min/100cm3)', fontsize=fs)
            ax[0,i].tick_params(axis='y', labelsize=fs)
            ax[1,i].set_ylabel('kbh (mL/min/100cm3)', fontsize=fs)
            ax[1,i].tick_params(axis='y', labelsize=fs)
        else:
            ax[0,i].set_yticklabels([])
            ax[1,i].set_yticklabels([])

        file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')
        dmr = pydmr.read(file, 'nest')

        # Plot the rate constants in units of mL/min/100mL
        for s in dmr['pars'].keys():
            x = [1]
            khe = [6000*dmr['pars'][s]['Day_1']['Ktrans']]
            kbh = [6000*dmr['pars'][s]['Day_1']['kbh']] 
            if 'Day_2' in dmr['pars'][s]:
                x += [2]
                khe += [6000*dmr['pars'][s]['Day_2']['Ktrans']]
                kbh += [6000*dmr['pars'][s]['Day_2']['kbh']] 
            color = clr[int(s[-2:])-1]
            ax[0,i].plot(x, khe, '-', label=s, marker='o', markersize=6, 
                        color=color)
            ax[1,i].plot(x, kbh, '-', label=s, marker='o', markersize=6, 
                        color=color)

    plt.savefig(fname=os.path.join(figpath, 'data_09-11_bosentan'))


def rifampicin_data():

    studies = [
        'study_01_rifampicin_effect_size',
        'study_02_rifampicin_effect_size',
        'study_03_rifampicin_effect_size',
        'study_04_rifampicin_effect_size',
    ]

    # Set up the figure
    clr = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
            'tab:brown']
    fs = 10
    fig, ax = plt.subplots(2, 2, figsize=(4, 8))
    fig.subplots_adjust(wspace=0.2, hspace=0.1, right=0.95, left=0.2)

    # Set up subfigures for the study
    title = {0:'placebo', 1:'rifampicin'}
    for i in [0,1]:
        ax[0,i].set_title(title[i], fontsize=fs, pad=10)
        ax[0,i].set_ylim(0, 150)
        ax[0,i].set_xticklabels([])
        ax[1,i].set_ylim(0, 40)
        ax[1,i].set_xticklabels([])
    ax[0,0].set_ylabel('Ktrans (mL/min/100cm3)', fontsize=fs)
    ax[0,0].tick_params(axis='y', labelsize=fs)
    ax[1,0].set_ylabel('kbh (mL/min/100cm3)', fontsize=fs)
    ax[1,0].tick_params(axis='y', labelsize=fs)
    ax[0,1].set_yticklabels([])
    ax[1,1].set_yticklabels([])

    cnt = 0
    for study in studies:

        file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')
        dmr = pydmr.read(file, 'nest')

        # Plot the rate constants in units of mL/min/100mL
        for rat in dmr['pars'].keys():
            x = [1]
            khe = [6000*dmr['pars'][rat]['Day_1']['Ktrans']]
            kbh = [6000*dmr['pars'][rat]['Day_1']['kbh']] 
            if 'Day_2' in dmr['pars'][rat]:
                x += [2]
                khe += [6000*dmr['pars'][rat]['Day_2']['Ktrans']]
                kbh += [6000*dmr['pars'][rat]['Day_2']['kbh']] 
            i=1 if dmr['pars'][rat]['Day_2']['substance'] == 'Rifampicin' else 0
            color = pick_color(32, cnt)
            ax[0,i].plot(x, khe, '-', label=rat, marker='o', markersize=6, 
                        color=color)
            ax[1,i].plot(x, kbh, '-', label=rat, marker='o', markersize=6, 
                        color=color)
            cnt+=1

    plt.savefig(fname=os.path.join(figpath, 'data_01-04_rifampicin'))


def field_strength_data():

    study = 'study_13_field_strength'

    # Set up the figure
    clr = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
            'tab:brown']
    fs = 10
    fig, ax = plt.subplots(2, 1, figsize=(2, 8))
    fig.subplots_adjust(wspace=0.2, hspace=0.1, right=0.90, left=0.3)

    # Set up subfigures for the study
    ax[0].set_title('Placebo', fontsize=fs, pad=10)
    ax[0].set_ylim(0, 150)
    ax[0].set_xticklabels([])
    ax[1].set_ylim(0, 40)
    # ax[1].set_xticklabels([])
    ax[1].set_xlabel('field strength (T)', fontsize=fs)
    ax[0].set_ylabel('Ktrans (mL/min/100cm3)', fontsize=fs)
    ax[0].tick_params(axis='y', labelsize=fs)
    ax[1].set_ylabel('kbh (mL/min/100cm3)', fontsize=fs)
    ax[1].tick_params(axis='y', labelsize=fs)

    file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')
    dmr = pydmr.read(file, 'nest')

    # Plot the rate constants in units of mL/min/100mL
    for rat in dmr['pars'].keys():
        x = [dmr['pars'][rat]['Day_1']['field_strength']]
        khe = [6000*dmr['pars'][rat]['Day_1']['Ktrans']]
        kbh = [6000*dmr['pars'][rat]['Day_1']['kbh']] 
        if 'Day_2' in dmr['pars'][rat]:
            x += [dmr['pars'][rat]['Day_2']['field_strength']]
            khe += [6000*dmr['pars'][rat]['Day_2']['Ktrans']]
            kbh += [6000*dmr['pars'][rat]['Day_2']['kbh']] 
        
        color = clr[int(rat[-2:])-1]
        ax[0].plot(x, khe, '-', label=rat, marker='o', markersize=6, 
                    color=color)
        ax[1].plot(x, kbh, '-', label=rat, marker='o', markersize=6, 
                    color=color)

    plt.savefig(fname=os.path.join(figpath, 'data_13_field_strength'))