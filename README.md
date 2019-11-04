# gt-dimred
Genotype dimension reduction research

These are the core files used in the manuscript here: https://biorxiv.org/content/early/2018/09/23/423632

The pre-print has since been published at PLOS Genetics: https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1008432

If you want a simple Python script to carry out UMAP on your PC data, see scripts/general_umap_script.py.

Most of the code is dedicated to data management and visualization. There's a python script that runs UMAP based on existing PC data.
PC data for the UKBB was provided to me so I didn't generate it myself.
PC data for the HRS (and HRS/1KGP data) was generated in PLINK.
Work done on the 1KGP data can be found in another repo: https://github.com/diazale/1KGP_dimred

This HRS code is quite messy - this is because we worked with several subsets of the data and had to use proxies for ethnicities. While it works, it involves bouncing around different parts of it.

The UKBB code can be run in a straightforward manner provided you already have the data.

The code for generating UMAP projections is in /scripts.
