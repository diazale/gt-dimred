import sys
import matplotlib.pyplot as plt
import collections
import gzip
import numpy as np
import os
import phate
import time

import pandas as pd
import pickle as pk

from collections import defaultdict
import itertools

# Interactive HTML tools
from ipywidgets import interact
import bokeh
import bokeh.io
from bokeh.io import push_notebook
from bokeh.plotting import figure, show, save, output_notebook, output_file
from bokeh.palettes import Category20b
from bokeh.palettes import Category20
from bokeh.palettes import Category10
from bokeh.palettes import PRGn
from bokeh.palettes import Set1

# Machine-learning and dimensionality reduction tools
import sklearn
from sklearn import decomposition
from sklearn.decomposition import PCA as PCA # We'll use this to check our implementation
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import MDS

sys.settrace

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

# Import the auxiliary data and reduce it to the ethnicity information and the IDs
ukbb_aux_df = pd.read_csv(os.path.join(data_dir,'ukb4940.csv'))
ukbb_aux_df = ukbb_aux_df.filter(['eid','21000-0.0','21000-1.0'])

# Create a string ID to match PCA (I don't want to touch the PCA dataset as its order is more important)
ukbb_aux_df['eid_str'] = ukbb_aux_df['eid'].apply(str)
ukbb_aux_df.columns=['eid','eth1','eth2','eid_str']
#ukbb_aux_df['eth1'] = ukbb_aux_df['eth1'].apply(int)

# Take care of NA values
ukbb_aux_df['eth1'] = ukbb_aux_df['eth1'].fillna(-9).astype(int)
ukbb_aux_df.loc[(ukbb_aux_df['eth2'].isnull()==True), 'eth2'] = ukbb_aux_df.loc[(ukbb_aux_df['eth2'].isnull()==True), 'eth1']
ukbb_aux_df['eth2'] = ukbb_aux_df['eth2'].fillna(-9).astype(int)

# Convert ethnicities to strings (digits represent categories)
ukbb_aux_df['eth1_str'] = ukbb_aux_df['eth1'].astype(str)
ukbb_aux_df['eth2_str'] = ukbb_aux_df['eth2'].astype(str)

# Read in the PCA IDs as a pandas data frame
with open(pc_path) as pc:
    pca_contents = pc.readlines()

pca_data_aux = []

for pc in pca_contents[1:]:
    pca_data_aux.append(pc.split()[0:2])

ukbb_pca_df = pd.DataFrame.from_records(pca_data_aux)
ukbb_pca_df.columns = ['FID','IID']

# Join the ethnicities to the PCA IDs
ukbb_df_joined = ukbb_pca_df.merge(ukbb_aux_df, left_on='IID', right_on='eid_str', how='left')

# Put together a dict of values
# Taken from: http://biobank.ctsu.ox.ac.uk/crystal/coding.cgi?id=1001
# Primary dict covers all values
ukbb_eth_dict = {
    '1':'White',
    '1001':'British',
    '1002':'Irish',
    '1003':'Any other white background',
    '2':'Mixed',
    '2001':'White and Black Caribbean',
    '2002':'White and Black African',
    '2003':'White and Asian',
    '2004':'Any other mixed background',
    '3':'Asian or Asian British',
    '3001':'Indian',
    '3002':'Pakistani',
    '3003':'Bangladeshi',
    '3004':'Any other Asian background',
    '4':'Black or Black British',
    '4001':'Caribbean',
    '4002':'African',
    '4003':'Any other Black background',
    '5':'Chinese',
    '6':'Other ethnic group',
    '-1':'Do not know',
    '-3':'Prefer not to answer',
    '-9':'Not available'
}

ukbb_dict_child = {
    '1001':'British',
    '1002':'Irish',
    '1003':'Any other white background',
    '2001':'White and Black Caribbean',
    '2002':'White and Black African',
    '2003':'White and Asian',
    '2004':'Any other mixed background',
    '3001':'Indian',
    '3002':'Pakistani',
    '3003':'Bangladeshi',
    '3004':'Any other Asian background',
    '4001':'Caribbean',
    '4002':'African',
    '4003':'Any other Black background',
    '5':'Chinese',
    '6':'Other ethnic group',
    '-1':'Do not know',
    '-3':'Prefer not to answer',
    '-9':'Not available'
}

# Parent categories of ethnicities
ukbb_dict_parent = {
    '1':'White',
    '2':'Mixed',
    '3':'Asian',
    '4':'Black',
    '5':'Chinese',
    '6':'Other',
    '-':'NA'
}

# Secondary relationship between parent-child ethnicities
ukbb_eth_dict_parent = defaultdict(list)

for key,value in ukbb_eth_dict.items():
    parent = key[0]

    if key not in ['1','2','3','4']:
        try:
            ukbb_eth_dict_parent[ukbb_dict_parent[parent]].append(value)
        except KeyError:
            ukbb_eth_dict_parent[ukbb_dict_parent[parent]] = value

# Reversed dictionaries
ukbb_dict_child_rev = dict()

for key, value in ukbb_dict_child.items():
    ukbb_dict_child_rev.update({value: key})

population_by_individual = defaultdict(int)
individual_by_population = defaultdict(list)
indices_of_population_members = defaultdict(list)

for k in ukbb_eth_dict.keys():
    temp_list = ukbb_df_joined[ukbb_df_joined['eth1_str']==k].index.values.tolist()
    indices_of_population_members[ukbb_eth_dict[k]] = temp_list

from bokeh.palettes import Plasma256
from bokeh.palettes import Category20c
from bokeh.palettes import BuGn
from bokeh.palettes import Purples
from bokeh.palettes import YlOrBr
from bokeh.palettes import Blues

# PARENT - Child colours
# WHITE - British, Irish, Other
# MIXED - W&B Caribbean, W&B African, W&Asian, Other
# ASIAN/ASIAN BRITISH - Indian, Pakistani, Bangladeshi, Other
# CHINESE
# OTHER
# DK, NO ANSWER, N/A

counter = 0
# Set up the colours (matplotlib tab20c)
color_dict_ukbb = {}

#for pop in ukbb_eth_dict_parent:
#    color_dict_ukbb[pop]=Plasma256[counter*10]
#    counter+=1
#
#    for subpop in ukbb_eth_dict_parent[pop]:
#        color_dict_ukbb[subpop]=Plasma256[counter*10]
#        counter+=1

for pop in ukbb_eth_dict_parent:
    counter=0
    print(pop)
    # White population is blue
    if pop=='White':
        #color_dict_ukbb[pop]=Category20c[20][counter]
        color_dict_ukbb[pop]=Blues[9][counter*2]
        counter+=1
        for subpop in ukbb_eth_dict_parent[pop]:
            #color_dict_ukbb[subpop] = Category20c[20][counter]
            color_dict_ukbb[subpop] = Blues[9][counter*2]
            counter+=1
    # Mixed population is green
    elif pop=='Mixed':
        color_dict_ukbb[pop]=BuGn[9][counter*2]
        counter+=1
        for subpop in ukbb_eth_dict_parent[pop]:
            color_dict_ukbb[subpop] = BuGn[9][counter*2]
            counter+=1
    # Asian population is Purple
    elif pop in ['Asian','Chinese']:
        color_dict_ukbb[pop]=Purples[9][counter*2]
        counter+=1
        for subpop in ukbb_eth_dict_parent[pop]:
            color_dict_ukbb[subpop] = Purples[9][counter*2]
            counter+=1
    # Black population is yellow/orange/brown
    elif pop=='Black':
        color_dict_ukbb[pop]=YlOrBr[9][counter*2]
        counter+=1
        for subpop in ukbb_eth_dict_parent[pop]:
            color_dict_ukbb[subpop] = YlOrBr[9][counter*2]
            counter+=1
    # Other ethnic groups are some variety of grey
    elif pop=='Other':
        for subpop in ukbb_eth_dict_parent[pop]:
            color_dict_ukbb[subpop] = Category20c[20][16+counter]
            counter+=1
    elif pop=='NA':
        for subpop in ukbb_eth_dict_parent[pop]:
            color_dict_ukbb[subpop] = Category20c[20][17+counter]
            counter+=1

pc_list = [r for r in range(2,11)] + [20,30,40]
print('Preparing to plot')

# Load and colour in some tSNE
for pc in pc_list:
    tsne_proj = np.loadtxt('/Users/alex/Documents/Ethnicity/UKBB_TSNE_'+str(pc)+'PCs_DefaultPerplexity')

    fig = plt.figure(figsize=(40,40))
    ax = fig.add_subplot(111, aspect=1)

    for pop in ukbb_eth_dict_parent:
        #print(pop)
        for subpop in ukbb_eth_dict_parent[pop]:
            temp_proj = tsne_proj[indices_of_population_members[subpop],:]
            #ax.plot(temp_proj[:,0], temp_proj[:,1],'.',label=subpop)
            ax.plot(temp_proj[:,0], temp_proj[:,1],'.',label=subpop,color=color_dict_ukbb[subpop])

    ax.legend(ncol=1,loc='center left', bbox_to_anchor=(1,0.5))

    #plt.savefig('UKBB_TSNE_PC' + str(pc) + '_PLEX_DEFAULT_LABELLED.svg', format='svg',dpi=1000)
    plt.savefig('UKBB_TSNE_PC' + str(pc) + '_PLEX_DEFAULT_LABELLED.jpeg', format='jpeg')
