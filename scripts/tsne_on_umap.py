# Do TSNE on UMAP projections

import numpy as np
import logging
import os
import sklearn
import sys
import time

from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as mTSNE
from sklearn.manifold import TSNE_custom

proj_dir = '/Volumes/Stockage/alex/ukbb_projections'
proj_name = 'UKBB_UMAP_PC10_NN15_MD0.5_2018329175935'

in_proj = np.loadtxt(os.path.join(proj_dir, proj_name))

#out_proj = mTSNE(perplexity=50,n_jobs=4).fit_transform(in_proj)
out_proj = TSNE_custom(perplexity=50).fit_transform(in_proj)

np.savetxt(os.path.join(proj_dir, proj_name + '_TSNE_custom_PLEX50'), out_proj)
