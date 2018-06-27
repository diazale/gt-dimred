import numpy as np
import sklearn

from sklearn.manifold import TSNE_custom

pc_path = '/Volumes/Stockage/alex/ukbb_projections/ukbb_pca_only'

with open(pc_path) as pc:
    pca_contents = pc.readlines()

pca_data = []

for pc in pca_contents[1:]:
    pca_data.append(pc.split()[3:len(pc)])

pca_data_array = np.array(pca_data).astype(np.float)

print('Finished importing PCA data.')

p = 10

temp_proj = TSNE_custom(n_components=2,n_iter=1500).fit_transform(pca_data_array[:,0:p])
np.savetxt('ukbb_tsne_pc' + str(p) + '_plex_def_for_gif', temp_proj)
