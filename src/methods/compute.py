# Import packages
import os
from tqdm import tqdm
import numpy as np
import pydmr
import dcmri as dc


datapath = os.path.join(os.getcwd(), 'data')
drugs = ['Asunaprevir','Bosentan','Cyclosporine','Ketoconazole',
         'Pioglitazone','Rifampicin']


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


def to_dmr(path, subj, study, pars):

    # Build data dictionary
    dmr = {
        'data': {},
        'pars': {},   
        'sdev': {},
    }
    for key, val in pars.items():
        dmr['data'][key] = [val[0], val[2], 'float']
        dmr['pars'][subj, study, key] = val[1]
        dmr['sdev'][subj, study, key] = val[3]

    # Save as dmr file
    visit = 'control' if study=='Day_1' else 'drug'
    name = subj + '_' + visit
    file = os.path.join(path, name + '.dmr')
    pydmr.write(file, dmr)
    return file


# def split_data():
#     # Temporary code - reformat data to one dmr file per drug.

#     # fetch data
#     dmrfile = miblab.zenodo_fetch(
#         'tristan_rats_healthy_six_drugs.dmr.zip',
#         datapath,
#         '15610261',
#     )
#     dmr = pydmr.read(dmrfile, 'nest')
#     pars = dmr['pars']

#     # Split into files
#     for drug in drugs + ['saline/vehicle']:
#         dmr_drug = {'data':dmr['data'], 'pars':{}, 'rois':{}}
#         for subj in pars.keys():
#             visit1 = list(pars[subj].keys())[0]
#             if pars[subj][visit1]['substance'] == drug:
#                 dmr_drug['pars'][subj] = dmr['pars'][subj]
#                 dmr_drug['rois'][subj] = dmr['rois'][subj]
#         name = drug.lower().replace('saline/vehicle','placebo')
#         path = os.path.join(datapath, f'tristan_rats_healthy_{name}')
#         pydmr.write(path, dmr_drug, 'nest')



def all_results():

    # Loop over all datasets
    for drug in tqdm(drugs + ['Placebo'], desc='Fitting..'):

        # Readt data
        name = drug.lower()
        dmrfile = os.path.join(datapath, f'tristan_rats_healthy_{name}')
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
                to_dmr(drugresults, subj, visit, rows)

                # Save plot for QC
                study = 'control' if visit=='Day_1' else 'drug'
                fig = model.plot(
                    rois[subj][visit]['time'], 
                    rois[subj][visit]['liver'],
                    fname = os.path.join(drugplots, subj + '_' + study + '.png'),
                    show=False,
                )

        # Combine dmr files per drug
        files = [os.path.join(drugresults, f) for f in os.listdir(drugresults)]
        result = os.path.join(os.getcwd(), 'build', 'tristan_rats_healthy_'+name + '_all_results')
        pydmr.concat(files, result)


if __name__=='__main__':
    all_results()