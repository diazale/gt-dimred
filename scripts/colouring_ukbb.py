# This script is to generate plots for UKBB projections. It's fairly rough.

import matplotlib.pyplot as plt
import numpy as np
import os
import time
import matplotlib
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

import pandas as pd

from collections import defaultdict
import itertools

# Colour schemes
import bokeh
from bokeh.palettes import PRGn
from bokeh.palettes import Set1
from bokeh.palettes import Plasma256
from bokeh.palettes import Category20c
from bokeh.palettes import Category20
from bokeh.palettes import Category10
from bokeh.palettes import BuGn
from bokeh.palettes import Purples
from bokeh.palettes import YlOrBr
from bokeh.palettes import Blues
from bokeh.palettes import Spectral
from bokeh.palettes import PuBuGn
from bokeh.palettes import RdPu
from bokeh.palettes import Reds

data_dir = '/Volumes/Stockage/alex/ukbb_projections'
aux_data_dir = '/Users/alex/Documents/Ethnicity'
pc_file = 'ukbb_pca_only'
proj_dir = '/Volumes/Stockage/alex/ukbb_projections'
out_dir = '/Volumes/Stockage/alex/ukbb_images'

# Get the PC data. We won't be using it directly, but will use its ordering.
pc_path = os.path.join(data_dir, pc_file)

##### Get all of the auxiliary data
# Import the auxiliary data and reduce it to the ethnicity information and the IDs
ukbb_aux_df = pd.read_csv(os.path.join(aux_data_dir,'ukb4940.csv'))
ukbb_aux_df = ukbb_aux_df.filter(['eid','21000-0.0','21000-1.0'])

# Create a string ID to match PCA (I don't want to touch the PCA dataset as its order is more important)
ukbb_aux_df['eid_str'] = ukbb_aux_df['eid'].apply(str)
ukbb_aux_df.columns=['eid','eth1','eth2','eid_str']

# Take care of NA values
ukbb_aux_df['eth1'] = ukbb_aux_df['eth1'].fillna(-9).astype(int)
ukbb_aux_df.loc[(ukbb_aux_df['eth2'].isnull()==True), 'eth2'] = ukbb_aux_df.loc[(ukbb_aux_df['eth2'].isnull()==True), 'eth1']
ukbb_aux_df['eth2'] = ukbb_aux_df['eth2'].fillna(-9).astype(int)

# Convert ethnicities to strings (digits represent categories)
ukbb_aux_df['eth1_str'] = ukbb_aux_df['eth1'].astype(str)
ukbb_aux_df['eth2_str'] = ukbb_aux_df['eth2'].astype(str)

##### Get the geographic data
geo_file = 'eid_df22006_df129north_df130east.mer'

ukbb_geo_df = pd.read_csv(os.path.join(aux_data_dir,geo_file))
ukbb_geo_df.columns=['eid','genetic_grouping','northing','easting']
ukbb_geo_df['northing_orig']=ukbb_geo_df['northing']
ukbb_geo_df['easting_orig']=ukbb_geo_df['easting']


mask = ukbb_geo_df.northing.isnull()
col_name = 'northing'
ukbb_geo_df.loc[mask, col_name] = 0

mask = ukbb_geo_df.easting.isnull()
col_name = 'easting'
ukbb_geo_df.loc[mask, col_name] = 0

mask = ukbb_geo_df.northing < 0
col_name = 'northing'
ukbb_geo_df.loc[mask, col_name] = 0

mask = ukbb_geo_df.easting < 0
col_name = 'easting'
ukbb_geo_df.loc[mask, col_name] = 0

ukbb_geo_df['northing']=ukbb_geo_df['northing']/max(ukbb_geo_df['northing'])
ukbb_geo_df['easting']=ukbb_geo_df['easting']/max(ukbb_geo_df['easting'])
ukbb_geo_df['eid_str_geo'] = ukbb_geo_df['eid'].astype(str)

# Deal with invalid or empty values
ukbb_geo_df['northing_filled'] = ukbb_geo_df['northing_orig'].fillna(0)
ukbb_geo_df['easting_filled'] = ukbb_geo_df['easting_orig'].fillna(0)

northing_orig = ukbb_geo_df['northing_orig'].values
northing_orig = northing_orig[np.isnan(northing_orig)==False]
easting_orig = ukbb_geo_df['easting_orig'].values
easting_orig = easting_orig[np.isnan(easting_orig)==False]

# Get the aux data lined up with the PC data
for pc in pca_contents[1:]:
    pca_data_aux.append(pc.split()[0:2])

ukbb_pca_df = pd.DataFrame.from_records(pca_data_aux)
ukbb_pca_df.columns = ['FID','IID']

ukbb_df_joined = ukbb_pca_df.merge(ukbb_aux_df, left_on='IID', right_on='eid_str', how='left')
ukbb_df_joined2 = ukbb_df_joined.merge(ukbb_geo_df, left_on='IID', right_on='eid_str_geo', how='left')

# Some weird missing values still around
ukbb_df_joined2['easting_filled'] = ukbb_df_joined2['easting_filled'].fillna(0)
ukbb_df_joined2['northing_filled'] = ukbb_df_joined2['northing_filled'].fillna(0)

ukbb_geo_colours = ukbb_df_joined2[['northing','easting']]
# Fix rare NaNs (where there was no data for individuals)
ukbb_geo_colours['northing'] = ukbb_geo_colours['northing'].fillna(0).astype(float)
ukbb_geo_colours['easting'] = ukbb_geo_colours['easting'].fillna(0).astype(float)

ukbb_geo_colours = ukbb_geo_colours.values.tolist()

# Create a list of the original values too
ukbb_geo_colours_orig = ukbb_df_joined2[['northing_filled','easting_filled']].values.tolist()

##### Define our dictionaries of colours and ethnicities
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
    '3':'Asian or Asian British',
    '4':'Black or Black British',
    '5':'Chinese',
    '6':'Other ethnic group',
    '-':'NA'
}

markers_dict = {
    'White':'o',
    'Mixed':'*',
    'Asian or Asian British':'P',
    'Black or Black British':'P',
    'Chinese':'^',
    'Other ethnic group':'s',
    'NA':'X'
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

# Prepare the indices by category
population_by_individual = defaultdict(int)
individual_by_population = defaultdict(list)
indices_of_population_members = defaultdict(list)

for k in ukbb_eth_dict.keys():
    temp_list = ukbb_df_joined[ukbb_df_joined['eth1_str']==k].index.values.tolist()
    indices_of_population_members[ukbb_eth_dict[k]] = temp_list

# PARENT - Child colours
# WHITE - British, Irish, Other
# MIXED - W&B Caribbean, W&B African, W&Asian, Other
# ASIAN/ASIAN BRITISH - Indian, Pakistani, Bangladeshi, Other
# CHINESE
# OTHER
# DK, NO ANSWER, N/A

color_list = Category20b[20]+Spectral[11]

counter = 0
# Set up the colours (matplotlib tab20c)
color_dict_ukbb = {}

for pop in ukbb_eth_dict_parent:
    counter=0

    # White population is blue (or not, sitll choosing whatevs)
    if pop=='White':
        color_dict_ukbb[pop]=PuBuGn[9][counter]
        counter+=1
        for subpop in ukbb_eth_dict_parent[pop]:
            color_dict_ukbb[subpop] = PuBuGn[9][counter*2]
            counter+=1
    # Mixed population is green
    elif pop=='Mixed':
        color_dict_ukbb[pop]=BuGn[9][counter]
        color_dict_ukbb['White and Black Caribbean']=Category10[3][-2] # Orange
        color_dict_ukbb['White and Black African']=Category10[4][-1] # Red
        color_dict_ukbb['White and Asian']=Category10[5][-1] # Purple
        color_dict_ukbb['Any other mixed background']=Category10[3][-1] # Green
    elif pop in ['Asian or Asian British']:
        color_dict_ukbb[pop]=Purples[9][0] # Dark purple
        color_dict_ukbb['Indian']=RdPu[9][0] # Dark red-purple
        color_dict_ukbb['Pakistani']=RdPu[9][2] # More pinkish dark red-purple
        color_dict_ukbb['Bangladeshi']=RdPu[9][4] # Even more pinkish dark red-purple
        color_dict_ukbb['Any other Asian background']=RdPu[9][-3] # Lighter red-purple
    elif pop in ['Chinese']:
        color_dict_ukbb[pop]=Category20[13][-1]
        counter+=1
    # Black population is yellow/orange/brown
    elif pop=='Black or Black British':
        color_dict_ukbb['Black or Black British']=YlOrBr[9][4] # Hazy orange
        color_dict_ukbb['Caribbean']=Reds[9][4] # Hazy red
        color_dict_ukbb['African']=Reds[9][0] # Deep red
        color_dict_ukbb['Any other Black background']=YlOrBr[9][-4] # Lighter Hazy orange
    # Other ethnic groups are some variety of grey
    elif pop=='Other ethnic group':
        for subpop in ukbb_eth_dict_parent[pop]:
            color_dict_ukbb[subpop] = Category20c[20][16+counter]
            counter+=1
    elif pop=='NA':
        for subpop in ukbb_eth_dict_parent[pop]:
            color_dict_ukbb[subpop] = Category20c[20][17+counter]
            counter+=1

# Geographic colourseasting_mean = np.mean(easting_orig)
easting_mean = np.mean(easting_orig)
northing_mean = np.mean(northing_orig)

# We'd like two colour maps: Northing (index 0) and Easting (index 1)
# Create a list of colour values and map them using the warm-to-cold colour map
# Looking at histograms, most individuals are below the 0.8 mark for north and above 0.2 for east
## so we normalize with respect to those (otherwise the colour scale is really uninformative)

# Those with zero values are invalid, so we make them invisible (alpha value of zero)
temp_colours_ns = []
temp_colours_ew = []
temp_alpha = []

ns_min = 100000
ns_max = 700000
ew_min = 200000
ew_max = 600000
alpha_vals = 0.6

# Deal with specific cases
for u in ukbb_geo_colours_orig:
    no_geo = False
    # Set alpha to zero for unknown geo values
    if u[0]<=0 or u[1]<=0:
        no_geo = True
        temp_alpha.append(np.float(0))
        temp_colours_ns.append(northing_mean)
        temp_colours_ew.append(easting_mean)

    if no_geo==False:
        if u[0] < ns_min:
            temp_colours_ns.append(ns_min)
        elif u[0] > ns_max:
            temp_colours_ns.append(ns_max)
        else:
            temp_colours_ns.append(u[0])

        if u[1] < ew_min:
            temp_colours_ew.append(ew_min)
        elif u[1] > ew_max:
            temp_colours_ew.append(ew_max)
        else:
            temp_colours_ew.append(u[1])

        temp_alpha.append(np.float(alpha_vals))

norm_ns = matplotlib.colors.Normalize(vmin=ns_min, vmax=ns_max, clip=False)
norm_ew = matplotlib.colors.Normalize(vmin=ew_min, vmax=ew_max, clip=False)
mapper_ns = cm.ScalarMappable(norm=norm_ns, cmap=cm.coolwarm_r)
mapper_ew = cm.ScalarMappable(norm=norm_ew, cmap=cm.spring)

colours_ns = []
colours_ew = []

for i in range(0, len(temp_colours_ns)):
    colours_ns.append(mapper_ns.to_rgba(temp_colours_ns[i], alpha=temp_alpha[i]))
    colours_ew.append(mapper_ew.to_rgba(temp_colours_ew[i], alpha=temp_alpha[i]))

# Not totally sure why I have to do this but I have wasted too much time on this stupid color bar
mapper_ns_temp = mapper_ns
mapper_ew_temp = mapper_ew

mapper_ns_temp._A = []
mapper_ew_temp._A = []

# Things to add:
# -Formalize list of all expected types of images to generate (eg. geo, colour scheme, subsets, etc)
# -Create 3d plots (give cube-side views)

# Generate images for all UKBB UMAP projections
for fname in os.listdir(proj_dir):
    if os.path.isdir(os.path.join(proj_dir,fname)):
        continue

    # Only do this for UMAP projections (TSNE added later, because ~*~I lie~*~)
    if 'UMAP' not in fname and 'TSNE' not in fname:
        continue

    # Don't do this for 3D projections
    if 'NC3' in fname:
        continue

    umap_proj = np.loadtxt(os.path.join(proj_dir, fname))

    x_coords = umap_proj[:,0]
    y_coords = umap_proj[:,1]

    # North-South colouring
    if not os.path.exists(os.path.join(out_dir, fname+'_ns.jpeg')):
        fig = plt.figure(figsize=(50,50))
        ax = fig.add_subplot(111, aspect=1)

        ax.scatter(x_coords, y_coords, c=colours_ns, cmap=cm.coolwarm_r, s=5)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('bottom',size='5%',pad=0.05)

        cbar = plt.colorbar(mapper_ns_temp,orientation='horizontal',cax=cax)
        cbar.set_label('SOUTH<---->NORTH')

        fig.savefig(os.path.join(out_dir, fname+'_ns.jpeg'),format='jpeg')
        plt.close()

    # East-West colouring
    if not os.path.exists(os.path.join(out_dir, fname+'_ew.jpeg')):
        fig = plt.figure(figsize=(50,50))
        ax = fig.add_subplot(111, aspect=1)

        ax.scatter(x_coords, y_coords, c=colours_ew, cmap=cm.spring, s=5)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes('bottom',size='5%',pad=0.05)

        cbar = plt.colorbar(mapper_ew_temp,orientation='horizontal',cax=cax)
        cbar.set_label('WEST<---->EAST')

        fig.savefig(os.path.join(out_dir, fname + '_ew.jpeg'),format='jpeg')
        plt.close()

    # Colouring by ethnicity
    if not os.path.exists(os.path.join(out_dir, fname+'_eth.jpeg')):
        fig = plt.figure(figsize=(50,50))
        ax = fig.add_subplot(111, aspect=1)

        for pop in ukbb_eth_dict_parent:
            if pop in ['White','Mixed','Asian or Asian British','Black or Black British']:
                temp_proj = umap_proj[indices_of_population_members[pop],:]
                ax.scatter(temp_proj[:,0], temp_proj[:,1],label=pop,color=color_dict_ukbb[pop],alpha=0.6)

            for subpop in ukbb_eth_dict_parent[pop]:
                temp_proj = umap_proj[indices_of_population_members[subpop],:]
                if subpop in ['Other ethnic group','Do not know']:
                    ax.scatter(temp_proj[:,0], temp_proj[:,1],marker=markers_dict[pop],label=subpop,facecolors='none',
                            edgecolors=color_dict_ukbb[subpop],alpha=0.6)
                else:
                    ax.scatter(temp_proj[:,0], temp_proj[:,1],marker=markers_dict[pop],label=subpop,color=color_dict_ukbb[subpop],alpha=0.6)

        ax.legend(ncol=4,loc='lower center', bbox_to_anchor=(0.4,-0.12), fontsize=40,markerscale=10)

        fig.savefig(os.path.join(out_dir, fname+'_eth.jpeg'),format='jpeg')
        plt.close()
