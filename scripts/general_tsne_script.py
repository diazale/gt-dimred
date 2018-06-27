# Python script to carry out t-SNE a bit more quickly.
# Inputs:
# Dataset to use (currently HRS or UKBB)
# Number of PCs
# Implementation of t-SNE (multicore is faster)
# Number of cores (only matters for multicore)

import numpy as np
import logging
import os
import sklearn
import sys
import time

from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as mTSNE

dset = input('Specify PC dataset (UKBB/HRS/1000G): ')
pcs = [int(n) for n in input('Number of principal components (spaces between list elements, default 10): ').split()]
num_iter = int(input('Number of iterations (default 1000): '))
imp = input('Specify t-SNE implementation (SKL/MC) (default SKL):')
cores = int(input('Specify number of cores for MC implementation (default 1): '))
plex = float(input('Specify perplexity (default 30): '))
lr = float(input('Specify learning rate (default 200): '))
ee = float(input('Specify early exaggeration rate (default 12.0): '))

# PCA files
ukbb_dir = '/Volumes/Stockage/alex/ukbb_projections'
hrs_dir = '/Volumes/Stockage/alex/hrs/projections'
tg_dir = '/Volumes/Stockage/alex/1000G/projections'

ukbb_path = os.path.join(ukbb_dir,'ukbb_pca_only')
hrs_path = os.path.join(hrs_dir,'hrs_200_pc')
tg_path = os.path.join(tg_dir,'pca_1000g_100')

# Logging directory.
log_dir = '/Users/alex/Documents/Ethnicity/scripts/logs'

tstamp = ''.join([str(t) for t in time.gmtime()[0:6]])
log_file = os.path.join(log_dir,'log_general_tsne_' + dset + '_' + tstamp)

#log_file = logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
with open(log_file, 'w') as f:
    sys.stdout = f

    # Print the parameters:
    print(dset + '_TSNE' + str(pcs) + '_PLEX' + str(plex) + '_LR' + str(lr) + '_ITER' + str(num_iter) + '_EE' + str(ee))

    # Load the PCA data and set the output directory
    try:
        if dset=='UKBB':
            with open(ukbb_path) as pc:
                pca_contents = pc.readlines()

            pca_data = []

            for pc in pca_contents[1:]:
                pca_data.append(pc.split()[3:len(pc)])

            pca_data_array = np.array(pca_data).astype(np.float)
            del(pca_data)
            del(pc)
            del(pca_contents)
            print('Successfully imported UKBB PCA data.')

            out_dir = ukbb_dir
        elif dset=='HRS':
            pca_data_array = np.loadtxt(hrs_path)

            out_dir = hrs_dir
        elif dset=='1000G':
            pca_data_array = np.loadtxt(tg_path)

            out_dir = tg_dir
    except Exception as e:
        print(e)
        print('Could not load PC data.')
        sys.exit(1)

    # Call TSNE for each PC
    try:
        for pc in pcs:
            print('Beginning loop for PC ' + str(pc))
            fname = dset + '_TSNE_PC' + str(pc) + '_PLEX' + str(plex) + '_LR' + str(lr) + '_ITER' + str(num_iter) + '_EE' + str(ee)
            try:
                if imp=='SKL':
                    tsne_proj = TSNE(n_components=2,early_exaggeration=ee,n_iter=num_iter,perplexity=plex,learning_rate=lr,verbose=3).fit_transform(pca_data_array[:,:pc])
                elif imp=='MC':
                    tsne_proj = mTSNE(n_jobs=cores,n_components=2,n_iter=num_iter,perplexity=plex,learning_rate=lr,verbose=2).fit_transform(pca_data_array[:,:pc])
            except Exception as e:
                print(e)
                print('Error during t-SNE projection.')
                sys.exit(1)

            np.savetxt(os.path.join(out_dir,fname+'_'+imp +'_'+tstamp), tsne_proj)
            print('File output to: ' + os.path.join(out_dir,fname+'_'+imp +'_'+tstamp))
    except Exception as e:
        print(e)
        print('Error during PC loop.')
        sys.exit(1)
