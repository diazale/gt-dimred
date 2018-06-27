import numpy as np
import sklearn

from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as mTSNE


pc_path = '/Users/alex/Documents/Ethnicity/Alex_UKBB_KGP'

with open(pc_path) as pc:
    pca_contents = pc.readlines()

pca_data = []

for pc in pca_contents[1:]:
    pca_data.append(pc.strip().split('\t')[2:-2])

pca_data_array = np.array(pca_data).astype(np.float)

print('Finished importing PCA data.')

pc_list=[5,8,10]

for p in pc_list:
    temp_proj = mTSNE(n_components=2,n_iter=15000,n_jobs=16,verbose=3).fit_transform(pca_data_array[:,0:p])
    #temp_proj = TSNE(n_components=2,n_iter=30000,verbose=3).fit_transform(pca_data_array[:,0:p])
    np.savetxt('ukbb_1000g_tsne_pc' + str(p) + '_plex_iter_15000', temp_proj)
