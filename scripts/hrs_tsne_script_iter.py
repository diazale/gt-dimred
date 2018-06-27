import numpy as np
import sklearn

from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as mTSNE
from sklearn.manifold import TSNE_custom as cTSNE

pc_path = '/Users/alex/Documents/Ethnicity/HRS/plink.eigenvec_200'

with open(pc_path) as pc:
    pca_contents = pc.readlines()

pca_data = []

for pc in pca_contents:
    pca_data.append(pc.split()[2:len(pc)])

pca_data_array = np.array(pca_data).astype(np.float)

print('Finished importing PCA data.')

#p=10
#temp_proj = cTSNE(n_components=2,n_iter=10000).fit_transform(pca_data_array[:,0:p])

for p in [10,20,30,50,100]:
    temp_proj = mTSNE(n_components=2,n_iter=10000,n_jobs=8,verbose=1).fit_transform(pca_data_array[:,0:p])
    np.savetxt('hrs_tsne_pc' + str(p) + '_plex_iter_10000_rep4', temp_proj)
    print('Saved and projected for PC: ' + str(p))
