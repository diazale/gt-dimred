import numpy as np
import os
import sklearn

from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as mTSNE


pc_path = '/Volumes/Stockage/alex/ukbb_projections'
pc_file = 'ukbb_pca_only'
out_dir = '/Volumes/Stockage/alex/ukbb_projections'

with open(os.path.join(pc_path,pc_file)) as pc:
    pca_contents = pc.readlines()

pca_data = []

for pc in pca_contents[1:]:
    pca_data.append(pc.strip().split()[3:])

pca_data_array = np.array(pca_data).astype(np.float)

print(pca_contents[1])
print(pca_data[0])
print(pca_data_array[0])
print('PCA dimensions: ' + str(pca_data_array.shape))
print('Finished importing PCA data.')

pc_list=[10]

for p in pc_list:
    temp_proj = TSNE(n_components=3,n_iter=5000,verbose=3).fit_transform(pca_data_array[:,:p])
    np.savetxt(os.path.join(out_dir,'ukbb_tsne_pc' + str(p) + '_plex30_iter_5000_3d'), temp_proj)
    temp_proj_2d = TSNE(n_components=2,verbose=3).fit_transform(temp_proj)
    np.savetxt(os.path.join(out_dir,'ukbb_tsne_pc' + str(p) + '_plex30_iter_1000_2d'), temp_proj)
