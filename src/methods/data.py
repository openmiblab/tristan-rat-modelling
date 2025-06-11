"""
This module has been used to convert data into a harmonized format 
for inclusion in the TRISTAN kinetics database. The datasets 
computed by this script have been uploaded to Zenodo so the script 
itself is no longer necessary and just retained for future reference.
"""
import os

import pydmr
import dcmri as dc

# Repro: 1,2,3, -4- ,5,6,7,8,9,10, -11- ,12, -13-
# Six_drugs: 5,6.7,8,9,10,12
# M_dosing: 1,2,3


datapath = os.path.join(os.getcwd(), 'data')


def split_repro():

    # Missing info to be added
    substance = {
        'S04-01': 'Placebo',
        'S04-02': 'Placebo',
        'S04-03': 'Placebo',
        'S04-04': 'Placebo',
        'S04-05': 'Rifampicin',
        'S04-06': 'Rifampicin',
        'S04-07': 'Rifampicin',
        'S04-08': 'Rifampicin',
        'S11-01': 'Placebo',
        'S11-02': 'Placebo',
        'S11-03': 'Placebo',
        'S11-04': 'Placebo',
        'S11-05': 'Placebo',
        'S11-06': 'Placebo',
        'S13-01': 'Placebo',
        'S13-02': 'Placebo',
        'S13-03': 'Placebo',
        'S13-04': 'Placebo',
        'S13-05': 'Placebo',
        'S13-06': 'Placebo',
    }

    # fetch data
    dmrfile = dc.fetch('tristan_rats_healthy_reproducibility')
    dmr = pydmr.read(dmrfile, 'nest')
    pars = dmr['pars']

    # Split into files
    for study in [4,11,13]:
        dmr_drug = {'data':dmr['data'], 'pars':{}, 'rois':{}}
        dmr_drug['data']['substance'] = ['What was injected, eg. saline, vehicle or drug name','','str']
        for subj in pars.keys():
            visit1 = list(pars[subj].keys())[0]
            if pars[subj][visit1]['study'] == study:
                dmr_drug['pars'][subj] = dmr['pars'][subj]
                dmr_drug['rois'][subj] = dmr['rois'][subj]
                for visit in pars[subj].keys():
                    dmr_drug['pars'][subj][visit]['substance'] = substance[subj]
        name = 'study_' + str(study).zfill(2) 
        if study==13:
            name += '_field_strength'
        elif study==11:
            name += '_control'
        elif study==4:
            name += '_placebo_rifampicin'
        path = os.path.join(datapath, f'tristan_rats_{name}')
        pydmr.write(path, dmr_drug, 'nest')


def split_repeat_dose():

    study_name = {
        1: 'chronic_rifampicin_placebo',
        2: 'chronic_cyclosporine_placebo',
        3: 'single_bosentan',
    }
    # Missing info to be added
    substance = {
        'S01-03': 'Placebo',
        'S01-06': 'Placebo',
        'S01-09': 'Placebo',
        'S01-12': 'Placebo',
        'S01-01': 'Rifampicin (clinical dose)',
        'S01-04': 'Rifampicin (clinical dose)',
        'S01-07': 'Rifampicin (clinical dose)',
        'S01-10': 'Rifampicin (clinical dose)',
        'S01-02': 'Rifampicin (high dose)',
        'S01-05': 'Rifampicin (high dose)',
        'S01-08': 'Rifampicin (high dose)',
        'S01-11': 'Rifampicin (high dose)',
        'S02-01': 'Cyclosporine (clinical dose)',
        'S02-02': 'Cyclosporine (clinical dose)',
        'S02-07': 'Cyclosporine (clinical dose)',
        'S02-08': 'Cyclosporine (clinical dose)',
        'S02-11': 'Cyclosporine (clinical dose)',
        'S02-12': 'Cyclosporine (clinical dose)',
        'S02-13': 'Cyclosporine (clinical dose)',
        'S02-03': 'Placebo',
        'S02-04': 'Placebo',
        'S02-05': 'Placebo',
        'S02-06': 'Placebo',
        'S02-09': 'Placebo',
        'S02-10': 'Placebo',
        'S03-01': 'Bosentan (clinical dose)',
        'S03-02': 'Bosentan (clinical dose)',
        'S03-03': 'Bosentan (clinical dose)',
        'S03-04': 'Bosentan (clinical dose)',
        'S03-05': 'Bosentan (clinical dose)',
        'S03-06': 'Bosentan (clinical dose)',
    }

    # fetch data
    dmrfile = dc.fetch('tristan_rats_healthy_multiple_dosing')
    dmr = pydmr.read(dmrfile, 'nest')
    pars = dmr['pars']

    # Split into files
    for study in [1,2,3]:
        dmr_drug = {'data':dmr['data'], 'pars':{}, 'rois':{}}
        dmr_drug['data']['substance'] = ['What was injected, eg. saline, vehicle or drug name','','str']
        for subj in pars.keys():
            visit1 = list(pars[subj].keys())[0]
            if pars[subj][visit1]['study'] == study:
                dmr_drug['pars'][subj] = dmr['pars'][subj]
                dmr_drug['rois'][subj] = dmr['rois'][subj]
                study = pars[subj][visit1]['study']
                for visit in pars[subj].keys():
                    dmr_drug['pars'][subj][visit]['substance'] = substance[subj]
        name = 'study_' + str(study).zfill(2) + '_' + study_name[study]
        path = os.path.join(datapath, f'tristan_rats_{name}')
        pydmr.write(path, dmr_drug, 'nest')



def split_six_compound():
    # Temporary code - reformat data to one dmr file per drug.

    drugs = ['Asunaprevir','Bosentan','Cyclosporine','Ketoconazole',
         'Pioglitazone','Rifampicin']
    
    dmrfile = dc.fetch('tristan_rats_healthy_six_drugs')
    dmr = pydmr.read(dmrfile, 'nest')
    pars = dmr['pars']

    # Split into files
    for drug in drugs + ['saline/vehicle']:
        dmr_drug = {'data':dmr['data'], 'pars':{}, 'rois':{}}
        for subj in pars.keys():
            visit1 = list(pars[subj].keys())[0]
            if pars[subj][visit1]['substance'] == drug:
                dmr_drug['pars'][subj] = dmr['pars'][subj]
                dmr_drug['rois'][subj] = dmr['rois'][subj]
                study = pars[subj][visit1]['study']
                if drug=='saline/vehicle':
                    for visit in pars[subj].keys():
                        dmr_drug['pars'][subj][visit]['substance']='Placebo'
        name = drug.lower().replace('saline/vehicle','placebo')
        name = 'study_' + str(study).zfill(2) + '_single_' + name
        path = os.path.join(datapath, f'tristan_rats_{name}')
        pydmr.write(path, dmr_drug, 'nest')


if __name__=='__main__':
    split_six_compound()
    split_repeat_dose()
    split_repro()