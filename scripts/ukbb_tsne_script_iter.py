import numpy as np
import sklearn

from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as mTSNE


pc_path = '/Volumes/Stockage/alex/ukbb_projections/ukbb_pca_only'

with open(pc_path) as pc:
    pca_contents = pc.readlines()

pca_data = []

for pc in pca_contents[1:]:
    pca_data.append(pc.split()[3:len(pc)])

pca_data_array = np.array(pca_data).astype(np.float)

print('Finished importing PCA data.')

p = 10
niter = 20000

#temp_proj = mTSNE(n_components=2,n_iter=niter,n_jobs=16,verbose=3).fit_transform(pca_data_array[:,0:p])
temp_proj = TSNE(n_components=2,n_iter=niter,verbose=3).fit_transform(pca_data_array[:,0:p])
np.savetxt('/Users/alex/Documents/Ethnicity/ukbb_tsne_pc' + str(p) + '_plex_iter_'+str(niter)+'_tsne_skl', temp_proj)
