# Python script to carry out UMAP on PC data

import argparse
from argparse import RawTextHelpFormatter
import numpy as np
import logging
import os
import sys
import time
import timeit

import umap

# Desired inputs with argparse
# -in (filename)
# -pc (# PCs)
# -nn 
# -md
# -nc
# -dist
# -outdir 

# define a str2bool function to intake the -head argument
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# example text for usage
example_text = '''
Requires the following packages: argparse, numpy, logging, os, sys, time, timeit, umap

EXAMPLE USAGE

Dataset: my_pcs.txt
Run UMAP on the top 15 PCs, using 10 neighbours, a minimum distance of 0.001,
reducing to 3D, assuming the first row of the file my_pcs.txt contains headers

python general_umap_script.py \\ 
-dset ~/Documents/my_umap_project/my_pcs.txt \\ 
-pc 15 \\ 
-nn 10 \\ 
-md 0.001 \\ 
-nc 3 \\ 
-outdir ~/Documents/my_umap_project/umap_projections \\ 
-head T \\ 
-log ~/Documents/my_umap_project/logs
'''

parser = argparse.ArgumentParser(description='Runs UMAP on specified datasets.',
    epilog=example_text, formatter_class=RawTextHelpFormatter)

parser.add_argument('-dset', type=str,
    help='Input dataset. This script assumes the data has already been reduced to PCs.')
parser.add_argument('-pc', type=int,
    default='10',
    help='Integer. Number of top PCs to use (default 10)')
parser.add_argument('-nn', type=int,
    default=15,
    help='Integer. Number of neighbours for UMAP')
parser.add_argument('-md', type=float,
    default=0.1,
    help='Float. Minimum distance for UMAP (default 0.1)')
parser.add_argument('-nc', type=int,
    default=2,
    help='Integer. Low dimensional components to project to (default 2D)')
parser.add_argument('-met', type=str,
    default='euclidean',
    help='String. Type of distance metric to use (default euclidean)')
parser.add_argument('-outdir', type=str,
    help='String. Output directory')
parser.add_argument('-head', type=str2bool,
    help='Boolean. Indicate whether the file has headers')
parser.add_argument('-log', type=str,
    help='String. Log directory')

args = parser.parse_args()
tstamp = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))

# Import arguments
dset = args.dset
pcs = args.pc
nn = args.nn
md = args.md
nc = args.nc
met = args.met.lower()
out_dir = args.outdir
has_headers = args.head
log_dir = args.log

# Check if important parameters have been left empty
if dset is None:
    print('ERROR: No input dataset specified.')
    sys.exit(1)
elif out_dir is None:
    print('ERROR: No output directory specified.')
    sys.exit(1)
elif has_headers is None:
    print('ERROR: Headers in file not specified.')
    sys.exit(1)

# Make sure the number of components is >= the number of PCs
if pcs < nc:
    print('ERROR: Number of PCs is less than request dimensions.')
    sys.exit(1)

# Print the parameters
param_str = dset.split('/')[-1].split('.txt')[0] + '_UMAP_PC' + str(pcs) + '_NC' + str(nc) + '_NN' \
+ str(nn) + '_MD' + str(md) + '_' + met

log_file = os.path.join(log_dir, 'log_umap_' + param_str + '_' + tstamp + '.txt')

print('Beginning import of data')
print('Parameters: ', '\n PCs:', str(pcs), '\n NC:', str(nc), '\n NN:', str(nn), '\n MD:', str(md),
    '\n Metric:', met, '\n Has headers:', str(has_headers))

# set up logging
orig_stdout = sys.stdout # print() statements
orig_stderr = sys.stderr # terminal statements
f = open(log_file, 'w')
sys.stdout = f
sys.stderr = f

print('Parameters: ', '\n PCs:', str(pcs), '\n NC:', str(nc), '\n NN:', str(nn), '\n MD:', str(md),
    '\n Metric:', met, '\n Has headers:', str(has_headers))

try:
    with open(dset) as data:
        data_contents = data.readlines()

        pca_data = []

        # import top PCs
        if has_headers==True:
            for pc in data_contents[1:]:
                pca_data.append(pc.split()[2:len(pc)])
        else:
            for pc in data_contents:
                pca_data.append(pc.split()[2:len(pc)])

        pca_data_array = np.array(pca_data).astype(np.float)

        print(pca_data_array.shape)
        
        del(pca_data)
        del(pc)
        del(data_contents)
except Exception as e:
    print(e)
    print('Error during data import')

    f.close()
    print('Error during data import')

    sys.exit(1)

#fname = dset.split('.txt')[0] + '_UMAP_PC' + str(pcs) + '_NC' + str(nc) + '_NN' + str(nn) + '_MD' + str(md) + '_' \
#+ met + "_" + tstamp + ".txt"
fname = param_str + '_' + tstamp + '.txt'

# preamble for log
print()
print("Using UMAP version: " + umap.__version__)
print("Reducing to " + str(nc) + " components")
print("Using " + str(nn) + " neighbours")
print("Using minimum distance of " + str(md))
print("Using metric: " + met)
print("Using " + str(pcs) + " PCs")
print()
print("Input data shape: ", pca_data_array.shape)

try:
    # Carry out UMAP
    start = timeit.default_timer()
    umap_proj = umap.UMAP(n_components=nc, n_neighbors=nn,min_dist=md,metric=met,
        verbose=True).fit_transform(pca_data_array[:,:pcs])
    stop = timeit.default_timer()
except Exception as e:
    print(e)
    print('Error during UMAP')

    f.close()
    print('Error during UMAP')
    sys.exit(1)

print()
print("UMAP runtime: ", stop - start)

out_file = os.path.join(out_dir,fname)

print()
print("Output file:", out_file)
print("Output data shape:", umap_proj.shape)

np.savetxt(out_file, umap_proj)

del(umap_proj)
del(pca_data_array)

# restore print statements to terminal
sys.stdout = orig_stdout
sys.stderr = orig_stderr
f.close()

# print runtime to terminal.
print("Finished successfully! UMAP runtime: ", stop - start)
