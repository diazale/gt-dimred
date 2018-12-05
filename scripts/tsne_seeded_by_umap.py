import numpy as np
import logging
import os
import sklearn
import sys
import time

from sklearn.manifold import TSNE
from sklearn.manifold import TSNE_no_ee as cTSNE

# directory to store intermediate steps (for animations)
anim_dir = "/Volumes/Stockage/alex/animations"

# PCA files
ukbb_dir = "/Volumes/Stockage/alex/ukbb_projections"
hrs_dir = "/Volumes/Stockage/alex/hrs/projections"
tg_dir = "/Volumes/Stockage/alex/1000G/projections"

ukbb_path = os.path.join(ukbb_dir,"ukbb_pca_only")
hrs_path = os.path.join(hrs_dir,"hrs_200_pc")
tg_path = os.path.join(tg_dir,"pca_1000g_100")

print("This script uses 10 principal components.")

dset = sys.argv[1] # Dataset - must be UKBB/HRS/1000G
num_iter = int(sys.argv[2]) # Number of iterations (default 1000)
seed_dset = sys.argv[3] # Whether to seed by UMAP or just use the PCs
pcs = [10]

tstamp = ''.join([str(t) for t in time.gmtime()[0:6]])

# Directory for this particular animation
anim_path = os.path.join(anim_dir, dset + "_" + tstamp)
os.makedirs(anim_path)

# Load the PCA data and UMAP data and set the output directory
try:
    if dset=='UKBB':
        with open(ukbb_path) as pc:
            pca_contents = pc.readlines()

        pca_data = []

        for pc in pca_contents[1:]:
            pca_data.append(pc.split()[3:len(pc)])

        pca_data_array = np.array(pca_data).astype(np.float)
        del(pca_data)
        del(pc)
        del(pca_contents)
        print("Successfully imported UKBB PCA data.")

        umap_proj = np.loadtxt(os.path.join(ukbb_dir,"UKBB_UMAP_PC10_NN15_MD0.5_2018328174511"))
        print("Importing reference file: UKBB_UMAP_PC10_NN15_MD0.5_2018328174511")

        out_dir = ukbb_dir
    elif dset=='HRS':
        pca_data_array = np.loadtxt(hrs_path)
        print("Successfully imported HRS PCA data")

        umap_proj = np.loadtxt(os.path.join(hrs_dir,"HRS_UMAP_PC10_NC2_NN15_MD0.5_20181024172559"))
        print("Importing reference file: HRS_UMAP_PC10_NC2_NN15_MD0.5_20181024172559")

        out_dir = hrs_dir
    elif dset=='1000G':
        pca_data_array = np.loadtxt(tg_path)
        print("Successfully imported 1KGP PCA data")

        umap_proj = np.loadtxt(os.path.join(tg_dir,"1000G_UMAP_PC10_NC2_NN15_MD0.5_20184421291"))
        print("Importing reference file: 1000G_UMAP_PC10_NC2_NN15_MD0.5_20184421291")

        out_dir = tg_dir
except Exception as e:
    print(e)
    print('Could not load PC data.')
    sys.exit(1)

# Call TSNE for each PC
try:
    for pc in pcs:
        print('Beginning loop for PC ' + str(pc))
        fname = dset + '_TSNE_' + seed_dset + '_SEED_PC' + str(pc) + '_ITER' + str(num_iter)
        try:
            if seed_dset == "UMAP":
                print("Projecting with t-SNE based on UMAP seed.")
                temp_proj = cTSNE(n_components=2, verbose=3, random_state=None,init=umap_proj,early_exaggeration=None,n_iter=num_iter,store_dir=anim_path).fit_transform(pca_data_array[:,:pc])
            else:
                print("Projecting with t-SNE based on default values.")
                temp_proj = cTSNE(n_components=2, verbose=3,n_iter=num_iter,store_dir=anim_path).fit_transform(pca_data_array[:,:pc])
        except Exception as e:
            print(e)
            print('Error during t-SNE projection.')
            sys.exit(1)

        np.savetxt(os.path.join(out_dir,fname+'_'+tstamp), temp_proj)
        print('File output to: ' + os.path.join(out_dir,fname+'_'+tstamp))
        print("Finished projection using t-SNE.")
except Exception as e:
    print(e)
    print("Error in PC loop.")
