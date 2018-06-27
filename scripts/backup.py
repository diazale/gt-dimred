# Get the indices of members of the sexes:
sex_list = ukbb_pheno_joined['sex'].values.tolist()
height_list = ukbb_pheno_joined[['Height','sex']].values.tolist()

indices_of_population_sex = defaultdict(list)

for sex in ['0','1']:
    temp_list = ukbb_pheno_joined[ukbb_pheno_joined['sex']==sex].index.values.tolist()
    indices_of_population_sex[sex] = temp_list

    # Need to create colour coding relative to each of the sexes
    temp_colours_m = []
    temp_colours_f = []
    temp_alpha_m = []
    temp_alpha_f = []

    #min_m = 140
    #max_m = 210
    #min_f = 130
    #max_f = 190
    min_m = np.percentile(np.array(temp_list_m), 1)
    max_m = np.percentile(np.array(temp_list_m), 99)
    min_f = np.percentile(np.array(temp_list_f), 1)
    max_f = np.percentile(np.array(temp_list_f), 99)

    alpha_vals=1

    # Deal with specific cases
    for h in height_list:
        no_height = False

        # Split into male/female/other (disregard unidentified sex)
        if h[1]=='0':
            # Female
            if int(h[0]) < 1:
                # Unknown height
                temp_colours_f.append(np.mean([min_f,max_f]))
                temp_alpha_f.append(0)
            elif int(h[0]) < min_f:
                # Truncated height
                temp_colours_f.append(min_f)
                temp_alpha_f.append(alpha_vals)
            elif int(h[0]) > max_f:
                # Truncated height
                temp_colours_f.append(max_f)
                temp_alpha_f.append(alpha_vals)
            else:
                # Actual height
                temp_colours_f.append(int(h[0]))
                temp_alpha_f.append(alpha_vals)
        elif h[1]=='1':
            # Male
            if int(h[0]) < 1:
                temp_colours_m.append(np.mean([min_m,max_m]))
                temp_alpha_m.append(0)
            elif int(h[0]) < min_m:
                # Truncated height
                temp_colours_m.append(min_m)
                temp_alpha_m.append(alpha_vals)
            elif int(h[0]) > max_m:
                # Truncated height
                temp_colours_m.append(max_m)
                temp_alpha_m.append(alpha_vals)
            else:
                # Actual height
                temp_colours_m.append(int(h[0]))
                temp_alpha_m.append(alpha_vals)

    norm_f = matplotlib.colors.Normalize(vmin=min_f, vmax=max_f, clip=False)
    norm_m = matplotlib.colors.Normalize(vmin=min_m, vmax=max_m, clip=False)
    mapper_f = cm.ScalarMappable(norm=norm_f, cmap=cm.coolwarm)
    mapper_m = cm.ScalarMappable(norm=norm_m, cmap=cm.coolwarm)

colours_f = []
colours_m = []

for i in range(0, len(temp_colours_f)):
    colours_f.append(mapper_f.to_rgba(temp_colours_f[i], alpha=temp_alpha_f[i]))

for i in range(0, len(temp_colours_m)):
    colours_m.append(mapper_m.to_rgba(temp_colours_m[i], alpha=temp_alpha_m[i]))

mapper_f_temp = mapper_f
mapper_m_temp = mapper_m

mapper_f_temp._A = []
mapper_m_temp._A = []

#/Volumes/Stockage/alex/ukbb_projections/UKBB_UMAP_PC10_NN15_MD0.5_2018328174511
proj_dir = '/Volumes/Stockage/alex/ukbb_projections/'
fname = 'UKBB_UMAP_PC10_NN15_MD0.5_2018328174511'
proj=np.loadtxt(os.path.join(proj_dir,fname))
size=30

# Female heights
temp_proj = proj[indices_of_population_sex['0']]

fig = plt.figure(figsize=(50,50))
ax = fig.add_subplot(111, aspect=1)

ax.scatter(temp_proj[:,0], temp_proj[:,1], c=colours_f, cmap=cm.coolwarm, s=size)

divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom',size='5%',pad=0.05)

cbar = plt.colorbar(mapper_f_temp,orientation='horizontal',cax=cax)
cbar.set_label('Height (cm)')

fig.savefig(os.path.join(out_dir, fname+'_height_f.jpeg'),format='jpeg')
plt.close()

# Male heights
temp_proj = proj[indices_of_population_sex['1']]

fig = plt.figure(figsize=(50,50))
ax = fig.add_subplot(111, aspect=1)

ax.scatter(temp_proj[:,0], temp_proj[:,1], c=colours_m, cmap=cm.coolwarm, s=size)

divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom',size='5%',pad=0.05)

cbar = plt.colorbar(mapper_m_temp,orientation='horizontal',cax=cax)
cbar.set_label('Height (cm)')

fig.savefig(os.path.join(out_dir, fname+'_height_m.jpeg'),format='jpeg')
plt.close()
