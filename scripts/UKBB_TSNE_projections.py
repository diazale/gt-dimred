import matplotlib.pyplot as plt
import collections
import gzip
import numpy as np
import logging
import os
import phate
import time

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

# Import PC data. This data must be converted to an array.
with open(pc_path) as pc:
    pca_contents = pc.readlines()

pca_data = []

for pc in pca_contents[1:]:
    pca_data.append(pc.split()[3:len(pc)])

# Purely numeric values of PCA
pca_data_array = np.array(pca_data).astype(np.float)
pc_list = [r for r in range(2,11)] + [20,30]

for p in pc_list:
    logging.basicConfig(filename='UKBB_TSNE_log'+str(p)+'_rep_1',level=logging.DEBUG)
    t0 = time.time()
    temp_proj = TSNE(n_components=2).fit_transform(pca_data_array[:,0:p])
    t1 = time.time()
    logging.debug('Time to project from PCs with dimension ' + str(p) + ' is ' + str(t1-t0))
    np.savetxt('UKBB_TSNE_'+str(p)+'PCs_DefaultPerplexity_rep_1',temp_proj)
