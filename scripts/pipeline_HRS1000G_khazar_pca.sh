#!/bin/bash

#PBS -q sw
#PBS -l nodes=1:ppn=4

#PBS -l walltime=2:00:00
#PBS -N pipeline_merge_HRS1000G_khazar_pca

cd /home/adiazpop/Ethnicity/HRS/data

plink --bfile khazar3_1-22_maf0.01mind0.035geno0.005 --maf 0.05 --mind 0.1 --geno 0.1 --hwe 1e-6 --make-bed --out khazar

sort khazar.bim > khazar_sorted.bim
sort merged_1000G_HRS.bim > merged_1000G_HRS_sorted.bim

comm -12 merged_1000G_HRS_sorted.bim khazar_sorted.bim > common_snps_HRS_1000G_khazar.txt

plink --bfile merged_1000G_HRS --extract common_snps_HRS_1000G_khazar.txt --make-bed --out merged_1000G_HRS_khazar_common
plink --bfile khazar --extract common_snps_HRS_1000G_khazar.txt --make-bed --out khazar_common
plink --bfile merged_1000G_HRS_khazar_common --bmerge khazar_common --make-bed --out merged_1000G_HRS_khazar

plink --bfile merged_1000G_HRS_khazar --pca 50 --out merged_1000G_HRS_khazar_pca

exit