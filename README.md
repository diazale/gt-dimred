# gt-dimred
Genotype dimension reduction research

These are the core files used in the manuscript here: https://biorxiv.org/content/early/2018/09/23/423632

The pre-print has since been published at PLOS Genetics: https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1008432

If you want a simple Python script to carry out UMAP on your PC data, see https://github.com/diazale/gt-dimred/blob/master/scripts/general_umap_script.py

Most of the code is dedicated to data management and visualization.

PC data for the UKBB was provided to me so I didn't generate it myself.
PC data for the HRS (and HRS/1KGP data) was generated in PLINK. See `HRS_exploration.ipynb` and `HRS_1000G_exploration.ipynb` for details.
A demo version of work done on the 1KGP data can be found in another repo: https://github.com/diazale/1KGP_dimred

This HRS code is quite messy - this is because we worked with several subsets of the data and had to use proxies for ethnicities. While it works, it involves bouncing around different parts of it.

The UKBB code can be run in a straightforward manner provided you already have the data.
