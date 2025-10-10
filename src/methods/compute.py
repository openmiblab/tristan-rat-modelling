# Import packages
import os


import numpy as np
import pydmr
import dcmri as dc


def tristan_rat(roi, par, **kwargs):

    # High-resolution time points for prediction
    t = np.arange(0, np.amax(roi['time'])+0.5, 0.5)

    # Standard input function
    ca = dc.aif_tristan_rat(t, BAT=par['BAT'], duration=par['duration'])

    # Liver model with population input function
    model = dc.Liver(

        kinetics = '1I-IC',
        non_stationary = None,
        sequence = 'SS',

        # Input parameters
        t = t,
        ca = ca,

        # Parameters
        field_strength = par['field_strength'],
        TR = par['TR'],
        FA = par['FA'],
        agent = 'gadoxetate',
        R10 = 1/dc.T1(par['field_strength'], 'liver'),
        H = 0.418,         # Cremer et al, J Cereb Blood Flow Metab 3, 254-256 (1983)
        ve = 0.23,         # mL/cm3
        Fp = 0.022019,     # mL/sec/cm3
                           # Fp = (1-H)*Fb, where Fb=2.27 mL/min/mL
                           # calculated from Table S2 in 
                           # doi: 10.1021/acs.molpharmaceut.1c00206

        free = {
            'E': [0.0, 0.9], 
            'Th': [0, np.inf],
        },
    )

    return model.train(roi['time'], roi['liver'], n0=par['n0'], **kwargs)


def to_dmr(path, subj, study, pars, dmr):

    # Build data dictionary
    dmr = {
        'data': dmr['data'],
        'pars': {(subj, study, key):val for key, val in dmr['pars'][subj][study].items() if key not in ['time','spleen','liver']},   
        'sdev': {},
    }
    for key, val in pars.items():
        if isinstance(val[1], str):
            par_type = 'str'
        else:
            par_type = 'float'
        dmr['data'][key] = [val[0], val[2], par_type]
        dmr['pars'][subj, study, key] = val[1]
        dmr['sdev'][subj, study, key] = val[3]

    # Save as dmr file
    name = subj + '_' + study
    file = os.path.join(path, name + '.dmr')
    pydmr.write(file, dmr)
    return file


def one_study(dmrfile, name):

    dmr = pydmr.read(dmrfile, 'nest')

    # To save results
    drugresults = os.path.join(os.getcwd(), 'build', 'per_subject_results', name, 'Values')
    drugplots = os.path.join(os.getcwd(), 'build', 'per_subject_results', name, 'Plots')
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
    result = os.path.join(os.getcwd(), 'build', 'output_data', 'tristan_rats_'+name)
    pydmr.concat(files, result)