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

import umap

dset = input('Specify PC dataset (UKBB/HRS/HRS_HISP/HRS_WHITE/HRS_BLACK/1000G): ')
pcs = [int(n) for n in input('Number of principal components (spaces between list elements, default 10): ').split()]
nn = int(input('Specify number of neighbours (default 15): '))
md = float(input('Specify minimum distance (default 0.1): '))
nc = int(input('Specify number of components (usually 2): '))

# PCA files
ukbb_dir = '/Volumes/Stockage/alex/ukbb_projections'
hrs_dir = '/Volumes/Stockage/alex/hrs/projections'
tg_dir = '/Volumes/Stockage/alex/1000G/projections'

ukbb_path = os.path.join(ukbb_dir,'ukbb_pca_only')
hrs_path = os.path.join(hrs_dir,'hrs_200_pc')
hrs_hisp_path = os.path.join(hrs_dir, 'plink.eigenvec_200_hispanic')
hrs_white_path = os.path.join(hrs_dir, 'plink.eigenvec_200_white')
hrs_black_path = os.path.join(hrs_dir, 'plink.eigenvec_200_black')
tg_path = os.path.join(tg_dir,'pca_1000g_100')

# Logging directory.
log_dir = '/Users/alex/Documents/Ethnicity/scripts/logs'

tstamp = ''.join([str(t) for t in time.gmtime()[0:6]])
log_file = os.path.join(log_dir,'log_general_umap_' + dset + '_UMAP_NC' + str(nc) + '_NN' + str(nn) + '_MD' + str(md) + tstamp)

#log_file = logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
with open(log_file, 'w') as f:
    sys.stdout = f

    # Print the parameters:
    print(dset + '_UMAP' + str(pcs) + '_NC' + str(nc) + '_NN' + str(nn) + '_MD' + str(md))

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
        elif dset=='HRS_HISP':
            with open(hrs_hisp_path) as pc:
                pca_contents = pc.readlines()

            pca_data = []

            for pc in pca_contents:
                pca_data.append(pc.split()[2:len(pc)])

            pca_data_array = np.array(pca_data).astype(np.float)
            out_dir = hrs_dir

            del(pca_data)
            del(pc)
            del(pca_contents)
            print('Successfully imported HRS_HISP PCA data.')
        elif dset=='HRS_WHITE':
            with open(hrs_white_path) as pc:
                pca_contents = pc.readlines()

            pca_data = []

            for pc in pca_contents:
                pca_data.append(pc.split()[2:len(pc)])

            pca_data_array = np.array(pca_data).astype(np.float)
            out_dir = hrs_dir

            del(pca_data)
            del(pc)
            del(pca_contents)
            print('Successfully imported HRS_WHITE PCA data.')
        elif dset=='HRS_BLACK':
            with open(hrs_black_path) as pc:
                pca_contents = pc.readlines()

            pca_data = []

            for pc in pca_contents:
                pca_data.append(pc.split()[2:len(pc)])

            pca_data_array = np.array(pca_data).astype(np.float)
            out_dir = hrs_dir

            del(pca_data)
            del(pc)
            del(pca_contents)
            print('Successfully imported HRS_BLACK PCA data.')
    except Exception as e:
        print(e)
        print('Could not load PC data.')
        sys.exit(1)

    # Set up a different directory when then number of dimensions > 2
    if nc > 2:
        out_dir = os.path.join(out_dir, '3d')

    # Call UMAP for each PC
    try:
        for pc in pcs:
            print('Beginning loop for PC ' + str(pc))
            fname = dset + '_UMAP_PC' + str(pc) + '_NC' + str(nc) + '_NN' + str(nn) + '_MD' + str(md)
            try:
                umap_proj = umap.UMAP(n_components=nc, n_neighbors=nn,min_dist=md).fit_transform(pca_data_array[:,:pc])
            except Exception as e:
                print(e)
                print('Error during UMAP projection.')
                sys.exit(1)

            np.savetxt(os.path.join(out_dir,fname+'_'+tstamp), umap_proj)
            print('File output to: ' + os.path.join(out_dir,fname+'_'+tstamp))
            del(umap_proj)
    except Exception as e:
        print(e)
        print('Error during PC loop.')
        sys.exit(1)
