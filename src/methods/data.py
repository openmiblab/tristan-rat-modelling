"""
This module has been used to convert data into a harmonized format 
for inclusion in the TRISTAN kinetics database. The datasets 
computed by this script have been uploaded to Zenodo so the script 
itself is no longer necessary and just retained for future reference.
"""
import os

import pydmr
import dcmri as dc

# Repro: 1,2,3,4,13
# Six_drugs: 5,6,7,8,9,10,12
# M_dosing: 11,14,15

# Study naming conventions
# tristan_rats_study_01_rifampicin_effect_size
# tristan_rats_study_02_rifampicin_effect_size
# tristan_rats_study_03_rifampicin_effect_size
# tristan_rats_study_04_rifampicin_effect_size
# tristan_rats_study_05_single_asunaprevir
# tristan_rats_study_06_single_pioglitazone
# tristan_rats_study_07_single_ketoconazole
# tristan_rats_study_08_single_cyclosporine
# tristan_rats_study_09_single_bosentan_high
# tristan_rats_study_10_single_bosentan
# tristan_rats_study_11_chronic_bosentan_placebo
# tristan_rats_study_12_single_rifampicin
# tristan_rats_study_13_field_strength
# tristan_rats_study_14_chronic_rifampicin_placebo
# tristan_rats_study_15_chronic_cyclosporine_placebo

# HELPER FUNCTION
def rename_keys(old_dict, replacements):
    # Create a new dictionary with the corrected keys
    new_dict = {}
    for key, value in old_dict.items():
        new_key = key
        for old_substring, new_substring in replacements.items():
            if old_substring in new_key:
                new_key = new_key.replace(old_substring, new_substring)
                new_dict[new_key] = value
                
    return new_dict

datapath = os.path.join(os.getcwd(), 'input_data')


def split_repro():

    # Missing info to be added
    substance = {
        'S01-01': 'Placebo',
        'S01-02': 'Placebo',
        'S01-03': 'Placebo',
        'S01-04': 'Rifampicin',
        'S01-05': 'Rifampicin',
        'S01-06': 'Rifampicin',
        'S02-01': 'Placebo',
        'S02-02': 'Placebo',
        'S02-03': 'Placebo',
        'S02-04': 'Rifampicin',
        'S02-05': 'Rifampicin',
        'S02-06': 'Rifampicin',
        'S03-01': 'Placebo',
        'S03-02': 'Placebo',
        'S03-03': 'Placebo',
        'S03-04': 'Rifampicin',
        'S03-05': 'Rifampicin',
        'S03-06': 'Rifampicin',
        'S04-01': 'Placebo',
        'S04-02': 'Placebo',
        'S04-03': 'Placebo',
        'S04-04': 'Placebo',
        'S04-05': 'Rifampicin',
        'S04-06': 'Rifampicin',
        'S04-07': 'Rifampicin',
        'S04-08': 'Rifampicin',
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
    for study in [1,2,3,4,13]:
        dmr_drug = {'data':dmr['data'], 'pars':{}, 'rois':{}}
        dmr_drug['data']['substance'] = ['What was injected, eg. saline, vehicle or drug name','','str']
        for subj in pars.keys():
            if pars[subj]['Day_1']['study'] == study:
                dmr_drug['pars'][subj] = dmr['pars'][subj]
                dmr_drug['rois'][subj] = dmr['rois'][subj]
                dmr_drug['pars'][subj]['Day_1']['substance']='Placebo'
                dmr_drug['pars'][subj]['Day_2']['substance'] = substance[subj]
        name = 'study_' + str(study).zfill(2) 
        if study==13:
            name += '_field_strength'
        else:
            name += '_rifampicin_effect_size'
        path = os.path.join(datapath, f'tristan_rats_{name}')
        pydmr.write(path, dmr_drug, 'nest')


def split_repeat_dose():

    study_name = {
        11: 'chronic_bosentan_placebo', # replace all S03 with S11
        14: 'chronic_rifampicin_placebo', # replace all S01 with S14
        15: 'chronic_cyclosporine_placebo' # replace all S02 with S15
    }
    # Missing info to be added
    group = {
        'S14-03': 'Placebo',
        'S14-06': 'Placebo',
        'S14-09': 'Placebo',
        'S14-12': 'Placebo',
        'S14-01': 'Rifampicin (clinical dose)',
        'S14-04': 'Rifampicin (clinical dose)',
        'S14-07': 'Rifampicin (clinical dose)',
        'S14-10': 'Rifampicin (clinical dose)',
        'S14-02': 'Rifampicin (high dose)',
        'S14-05': 'Rifampicin (high dose)',
        'S14-08': 'Rifampicin (high dose)',
        'S14-11': 'Rifampicin (high dose)',
        'S15-01': 'Cyclosporine (clinical dose)',
        'S15-02': 'Cyclosporine (clinical dose)',
        'S15-07': 'Cyclosporine (clinical dose)',
        'S15-08': 'Cyclosporine (clinical dose)',
        'S15-11': 'Cyclosporine (clinical dose)',
        'S15-12': 'Cyclosporine (clinical dose)',
        'S15-13': 'Cyclosporine (clinical dose)',
        'S15-03': 'Placebo',
        'S15-04': 'Placebo',
        'S15-05': 'Placebo',
        'S15-06': 'Placebo',
        'S15-09': 'Placebo',
        'S15-10': 'Placebo',
        'S11-01': 'Bosentan (clinical dose)',
        'S11-02': 'Bosentan (clinical dose)',
        'S11-03': 'Bosentan (clinical dose)',
        'S11-04': 'Bosentan (clinical dose)',
        'S11-05': 'Bosentan (clinical dose)',
        'S11-06': 'Bosentan (clinical dose)',
    }

    # fetch data
    dmrfile = dc.fetch('tristan_rats_healthy_multiple_dosing')
    dmr = pydmr.read(dmrfile, 'nest')
    pars = dmr['pars']
    rois = dmr['rois']

    # Define mapping of study number substrings to replace
    replacements = {
        'S01': 'S14',
        'S02': 'S15',
        'S03': 'S11'
    }

    pars_updated = rename_keys(pars, replacements)
    rois_updated = rename_keys(rois, replacements)

    # Split into files
    for study in [11,14,15]:
        dmr_drug = {'data':dmr['data'], 'pars':{}, 'rois':{}}
        dmr_drug['data']['substance'] = ['What was injected, eg. saline, vehicle or drug name','','str']
        dmr_drug['data']['study arm'] = ['Which study arm the subject was in (e.g. control or treatment)','','str']
        for subj in pars_updated.keys():
            # update study field to correct study number
            for visit in pars_updated[subj].keys():

                # Substitute correct study numbers
                if pars_updated[subj][visit]['study'] == 3:
                    pars_updated[subj][visit]['study'] = 11
                elif pars_updated[subj][visit]['study'] == 1:
                    pars_updated[subj][visit]['study'] = 14
                if pars_updated[subj][visit]['study'] == 2:
                    pars_updated[subj][visit]['study'] = 15

                # Add study and substance information
                if pars_updated[subj][visit]['study'] == study:
                    pars_updated[subj][visit]['study arm'] = group[subj]
                    if visit == 'Day_1':
                        pars_updated[subj][visit]['substance'] = 'Placebo'
                    else:
                        pars_updated[subj][visit]['substance'] = group[subj]

            if pars_updated[subj][visit]['study'] == study:
                dmr_drug['pars'][subj] = pars_updated[subj]
                dmr_drug['rois'][subj] = rois_updated[subj]


        name = 'study_' + str(study).zfill(2) + '_' + study_name[study]
        path = os.path.join(datapath, f'tristan_rats_{name}')
        pydmr.write(path, dmr_drug, 'nest')



def split_six_compound():
    # Temporary code - reformat data to one dmr file per drug.

    study_name = {
        5: 'single_asunaprevir',
        6: 'single_pioglitazone',
        7: 'single_ketoconazole',
        8: 'single_cyclosporine',
        9: 'single_bosentan_high',
        10: 'single_bosentan',
        12: 'single_rifampicin',
    }

    dmrfile = dc.fetch('tristan_rats_healthy_six_drugs')
    dmr = pydmr.read(dmrfile, 'nest')
    pars = dmr['pars']

    # Split into files
    for study in [5,6,7,8,9,10,12]:
        dmr_drug = {'data':dmr['data'], 'pars':{}, 'rois':{}}
        dmr_drug['data']['substance'] = ['What was injected, eg. saline, vehicle or drug name','','str']
        for subj in pars.keys():
            if pars[subj]['Day_1']['study'] == study:
                dmr_drug['pars'][subj] = dmr['pars'][subj]
                dmr_drug['rois'][subj] = dmr['rois'][subj]
                dmr_drug['pars'][subj]['Day_1']['substance']='Placebo'
                if study==9:
                    dmr_drug['pars'][subj]['Day_2']['substance']='Bosentan (high dose)'

        name = 'study_' + str(study).zfill(2) + '_' + study_name[study]
        path = os.path.join(datapath, f'tristan_rats_{name}')
        pydmr.write(path, dmr_drug, 'nest')


if __name__=='__main__':
    split_six_compound()
    split_repeat_dose()
    split_repro()
