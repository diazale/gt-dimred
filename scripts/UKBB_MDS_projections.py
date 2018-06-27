import matplotlib.pyplot as plt
import collections
import gzip
import numpy as np
import logging
import os
import phate
import time
import sys

import pandas as pd
import pickle as pk

from collections import defaultdict
import itertools
# Machine-learning and dimensionality reduction tools
import sklearn
from sklearn import decomposition
from sklearn.decomposition import PCA as PCA # We'll use this to check our implementation
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import MDS

data_dir = '/Users/alex/Documents/Ethnicity'

# Define the files we'll be using
pc_file = 'ukbb_pca_only'

#aux_path = os.path.join(hrs_data_dir, aux_file)
pc_path = os.path.join(data_dir, pc_file)

print('Preparing to import PCA data')
# Import PC data. This data must be converted to an array.
with open(pc_path) as pc:
    pca_contents = pc.readlines()

pca_data = []

print('Preparing to convert PCA data to array')
for pc in pca_contents[1:]:
    pca_data.append(pc.split()[3:len(pc)])

# Purely numeric values of PCA
pca_data_array = np.array(pca_data).astype(np.float)
#pc_list = [r for r in range(2,11)] + [20,30]
pc_list = [2,5,10,20]

# for p in pc_list:
#     logging.basicConfig(filename='UKBB_MDS_log'+str(p),level=logging.DEBUG)
#
#     try:
#         print('Preparing to project from PCA with dimension ' + str(p))
#         t0 = time.time()
#         temp_proj = MDS(n_components=2).fit_transform(pca_data_array[:,0:p])
#         t1 = time.time()
#         logging.debug('Time to project from PCs with dimension ' + str(p) + ' is ' + str(t1-t0))
#         np.savetxt('UKBB_MDS_'+str(p)+'PCs',temp_proj)
#         print('Saved projection array for dimension ' + str(p))
#     except Exception as e:
#         logging.exception(e)
#         sys.exit(0)

# Haven't done tSNE on all 40 PCs yet
print('Preparing to do tSNE projection for 40 PCs')

logging.basicConfig(filename='UKBB_tSNE_log_40PC',level=logging.DEBUG)

p = 40

try:
    t0 = time.time()
    temp_proj = TSNE(n_components=2).fit_transform(pca_data_array)
    print('Projection complete')
    t1 = time.time()
    logging.debug('Time to project from PCs with dimension ' + str(p) + ' is ' + str(t1-t0))
    np.savetxt('UKBB_TSNE_40PCs',temp_proj)
    print('Projection saved')
except Exception as e:
    logging.exception(e)
    print('Error in projection/saving projection')
    sys.exit(0)
