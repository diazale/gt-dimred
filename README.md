# Genotype dimension reduction with UMAP

This is the code used in [Diaz-Papkovich et al (2019)](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1008432): 

```
@article{diaz2019umap,
  title={UMAP reveals cryptic population structure and phenotype heterogeneity in large genomic cohorts},
  author={Diaz-Papkovich, Alex and Anderson-Trocm{\'e}, Luke and Ben-Eghan, Chief and Gravel, Simon},
  journal={PLoS genetics},
  volume={15},
  number={11},
  pages={e1008432},
  year={2019},
  publisher={Public Library of Science San Francisco, CA USA}
}
```

If you are interested in clustering (with updated versions of our scripts), see [Diaz-Papkovich et al @ PLoS Genetics (2026)](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1012068) with the associated repo: https://github.com/diazale/topstrat

If you want a simple Python script to carry out UMAP on your PC data, see https://github.com/diazale/gt-dimred/blob/main/scripts/general_umap_script.py

Most of the code is dedicated to data management and visualization.

PCA data for the UKBB was provided by the UKBB.
PC data for the HRS (and HRS/1KGP data) was generated in PLINK. See `HRS_exploration.ipynb` and `HRS_1000G_exploration.ipynb` for details.
A demo version of work done on the 1KGP data can be found in another repo: https://github.com/diazale/1KGP_dimred

This HRS code is quite messy - this is because we worked with several subsets of the data and had to use proxies for ethnicities. While it works, it involves bouncing around different parts of it.

The UKBB code can be run in a straightforward manner provided you already have the data.
