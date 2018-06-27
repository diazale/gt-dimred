import numpy as np
import os
import sklearn
import time

from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as mTSNE


pc_path = '/Volumes/Stockage/alex/ukbb_projections'
pc_file = 'ukbb_pca_only'
out_dir = '/Volumes/Stockage/alex/ukbb_projections'
niter = 5000

print('Finished importing 3D projection data.')

tstamp = ''.join([str(t) for t in time.gmtime()[0:6]])

pc_list=[10]

for p in pc_list:
    temp_proj_3d = np.loadtxt('/Volumes/Stockage/alex/ukbb_projections/ukbb_tsne_pc10_plex30_iter_1000_3d')
    temp_proj_2d = TSNE(n_components=2,verbose=3,n_iter=niter).fit_transform(temp_proj_3d)
    np.savetxt(os.path.join(out_dir,'ukbb_tsne_pc' + str(p) + '_plex30_iter_' + str(niter) + '_2d_' + str(tstamp)), temp_proj_2d)
