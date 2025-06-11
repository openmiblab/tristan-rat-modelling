# Import packages
import os
from tqdm import tqdm
import numpy as np
import pydmr
import dcmri as dc
import miblab


datapath = os.path.join(os.getcwd(), 'data')
if not os.path.exists(datapath):
    os.makedirs(datapath)



def tristan_rat(roi, par, **kwargs):

    # High-resolution time points for prediction
    t = np.arange(0, np.amax(roi['time'])+0.5, 0.5)

    # Standard input function
    ca = dc.aif_tristan_rat(t, BAT=par['BAT'], duration=par['duration'])

    # Liver model with population input function
    model = dc.Liver(

        # Input parameters
        t = t,
        ca = ca,

        # Acquisition parameters
        field_strength = par['field_strength'],
        TR = par['TR'],
        FA = par['FA'],
        n0 = par['n0'],

        # Configure as in the TRISTAN-rat study
        config = 'TRISTAN-rat',
    )
    return model.train(roi['time'], roi['liver'], **kwargs)


def to_dmr(path, subj, study, pars, dmr):

    # Build data dictionary
    dmr = {
        'data': dmr['data'],
        'pars': {(subj, study, key):val for key, val in dmr['pars'][subj][study].items() if key not in ['time','spleen','liver']},   
        'sdev': {},
    }
    for key, val in pars.items():
        dmr['data'][key] = [val[0], val[2], 'float']
        dmr['pars'][subj, study, key] = val[1]
        dmr['sdev'][subj, study, key] = val[3]

    # Save as dmr file
    name = subj + '_' + study
    file = os.path.join(path, name + '.dmr')
    pydmr.write(file, dmr)
    return file


def all():

    studies = [
        'study_01_chronic_rifampicin_placebo',
        'study_02_chronic_cyclosporine_placebo',
        'study_03_single_bosentan',
        'study_04_placebo_rifampicin',
        'study_05_single_asunaprevir',
        'study_06_single_pioglitazone',
        'study_07_single_ketoconazole',
        'study_08_single_cyclosporine',
        'study_09_single_placebo',
        'study_10_single_bosentan',
        'study_11_control',
        'study_12_single_rifampicin',
        'study_13_field_strength',
    ]

    # Loop over all datasets
    for name in tqdm(studies, desc='Fitting..'):

        # Readt data
        #dmrfile = os.path.join(datapath, f'tristan_rats_{name}')
        dmrfile = miblab.zenodo_fetch(f'tristan_rats_{name}.dmr.zip', datapath, '15644122')
        dmr = pydmr.read(dmrfile, 'nest')

        # To save results
        drugresults = os.path.join(os.getcwd(), 'build', name, 'Results')
        drugplots = os.path.join(os.getcwd(), 'build', name, 'Plots')
        if not os.path.exists(drugresults):
            os.makedirs(drugresults)
        if not os.path.exists(drugplots):
            os.makedirs(drugplots)

        rois, pars = dmr['rois'], dmr['pars']

        for subj in rois.keys():
            for visit in pars[subj].keys():

                roi = rois[subj][visit]
                par = pars[subj][visit]

                # Generate a trained model
                model = tristan_rat(roi, par, xtol=1e-3)

                # Save as dmr
                rows = model.export_params()
                to_dmr(drugresults, subj, visit, rows, dmr)

                # Save plot for QC
                fig = model.plot(
                    rois[subj][visit]['time'], 
                    rois[subj][visit]['liver'],
                    fname = os.path.join(drugplots, subj + '_' + visit + '.png'),
                    show=False,
                )

        # Combine dmr files per drug
        files = [os.path.join(drugresults, f) for f in os.listdir(drugresults)]
        result = os.path.join(os.getcwd(), 'build', 'tristan_rats_'+name)
        pydmr.concat(files, result)


if __name__=='__main__':
    all()