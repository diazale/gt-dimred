import matplotlib.pyplot as plt
import collections
import gzip
import numpy as np
import os
import time

# Machine-learning and dimensionality reduction tools
import sklearn
from sklearn import decomposition
from sklearn.decomposition import PCA as PCA # We'll use this to check our implementation
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import MDS

import umap

data_dir = '/Volumes/Stockage/alex/Genizon'
pc_file = 'Genizon_AllSamples_PCA.eigenvec'

pc_path = os.path.join(data_dir, pc_file)

# Import PC data. This data must be converted to an array.
with open(pc_path) as pc:
    pca_contents = pc.readlines()

pca_data = []

for pc in pca_contents:
    pca_data.append(pc.split()[2:len(pc)])

pca_data_array = np.array(pca_data).astype(np.float)

proj_dir = '/Volumes/Stockage/alex/Genizon/projections'

tstamp_log = ''.join([str(t) for t in time.gmtime()[0:6]])
nn_vals = [5,10,15,50]
md_vals = [0.001, 0.01, 0.1, 0.5]
pc_vals = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
nc_vals = [2,3]

for nc in nc_vals:
    for pc in pc_vals:
        for nn in nn_vals:
            for md in md_vals:
                proj = umap.UMAP(n_components=nc, n_neighbors=nn, min_dist=md).fit_transform(pca_data_array[:,:pc])
                fname = 'GENIZON_UMAP_PC'+str(pc)+'_NC'+str(nc)+'_NN'+str(nn)+'_MD'+str(md)+'_'+tstamp_log
                np.savetxt(os.path.join(proj_dir, fname), proj)
