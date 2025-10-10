import os

from tqdm import tqdm
import miblab

from methods.compute import one_study
from methods import plot, analysis


STUDIES = [
    'study_01_rifampicin_effect_size',
    'study_02_rifampicin_effect_size',
    'study_03_rifampicin_effect_size',
    'study_04_rifampicin_effect_size',
    'study_05_single_asunaprevir',
    'study_06_single_pioglitazone',
    'study_07_single_ketoconazole',
    'study_08_single_cyclosporine',
    'study_09_single_bosentan_high',
    'study_10_single_bosentan',
    'study_11_chronic_bosentan_placebo',
    'study_12_single_rifampicin',
    'study_13_field_strength',
    'study_14_chronic_rifampicin_placebo',
    'study_15_chronic_cyclosporine_placebo',
]


if __name__=='__main__':

    datapath = os.path.join(os.getcwd(), 'input_data')
    if not os.path.exists(datapath):
        os.makedirs(datapath)

    # Compute all results
    for name in tqdm(STUDIES, desc='Fitting..'):
        dmrfile = miblab.zenodo_fetch(f'tristan_rats_{name}.dmr.zip', datapath, '15644122')
        one_study(dmrfile, name)

    # Make summary figures
    analysis.six_compound_effect_sizes()
    plot.six_compound_data()
    plot.six_compound_effect_sizes()

    analysis.reproducibility()
    plot.reproducibility()

    analysis.chronic_cyclosporine()
    plot.chronic_cyclosporine()

    analysis.chronic_rifampicin()
    plot.chronic_rifampicin()

    plot.bosentan_data()
    plot.rifampicin_data()
    plot.field_strength_data()