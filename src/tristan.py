import os

from tqdm import tqdm
import miblab

from methods.compute import one_study


if __name__=='__main__':

    datapath = os.path.join(os.getcwd(), 'build', 'Inputs')
    if not os.path.exists(datapath):
        os.makedirs(datapath)

    studies = [
        'tristan_rats_study_01_rifampicin_effect_size.dmr',
        'tristan_rats_study_02_rifampicin_effect_size.dmr',
        'tristan_rats_study_03_rifampicin_effect_size.dmr',
        'tristan_rats_study_04_rifampicin_effect_size.dmr',
        'tristan_rats_study_05_single_asunaprevir.dmr',
        'tristan_rats_study_06_single_pioglitazone.dmr',
        'tristan_rats_study_07_single_ketoconazole.dmr',
        'tristan_rats_study_08_single_cyclosporine.dmr',
        'tristan_rats_study_09_single_bosentan_high.dmr',
        'tristan_rats_study_10_single_bosentan.dmr',
        'tristan_rats_study_11_chronic_bosentan_placebo.dmr',
        'tristan_rats_study_12_single_rifampicin.dmr',
        'tristan_rats_study_13_field_strength.dmr',
        'tristan_rats_study_14_chronic_rifampicin_placebo.dmr',
        'tristan_rats_study_15_chronic_cyclosporine_placebo.dmr',
    ]

    # Loop over all datasets
    for name in tqdm(studies, desc='Fitting..'):

        # Read data
        dmrfile = miblab.zenodo_fetch(f'tristan_rats_{name}.dmr.zip', datapath, '15644122')
        
        # Fit model
        one_study(dmrfile, name)

