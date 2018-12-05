#!/bin/bash

# Define a timestamp function
timestamp() {
  date +"%Y%m%d_HHMMSS%H%M%S"
}

# do something...
#timestamp # print timestamp

# acceptable values are HRS, 1000G, and UKBB
DSET=${1?Error: no dataset given}

NITER=${2:-1000}
SEED=${3:-UMAP}
TSTAMP=$(timestamp)

echo "Seeding t-SNE with ${SEED} for ${DSET} dataset with ${NITER} iterations."
# Note - using $@ calls all declared variables (doesn't use defaults)

python tsne_seeded_by_umap.py $DSET $NITER $SEED> logs/tsne_seeded_by_umap_${DSET}_${NITER}_${TSTAMP}.txt
