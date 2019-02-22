# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 16:38:44 2018

@author: Angela
"""

#pulls SNPs from sig. genes in MESA models
import sqlite3
import numpy
import pandas
tissues = ["TW_Adipose_Subcutaneous_0.5.db", "TW_Adipose_Visceral_Omentum_0.5.db", "TW_Adrenal_Gland_0.5.db", "TW_Artery_Aorta_0.5.db", "TW_Artery_Coronary_0.5.db", "TW_Artery_Tibial_0.5.db", "TW_Brain_Anterior_cingulate_cortex_BA24_0.5.db", "TW_Brain_Caudate_basal_ganglia_0.5.db", "TW_Brain_Cerebellar_Hemisphere_0.5.db", "TW_Brain_Cerebellum_0.5.db", "TW_Brain_Cortex_0.5.db", "TW_Brain_Frontal_Cortex_BA9_0.5.db", "TW_Brain_Hippocampus_0.5.db", "TW_Brain_Hypothalamus_0.5.db", "TW_Brain_Nucleus_accumbens_basal_ganglia_0.5.db", "TW_Brain_Putamen_basal_ganglia_0.5.db", "TW_Breast_Mammary_Tissue_0.5.db", "TW_Cells_EBV-transformed_lymphocytes_0.5.db", "TW_Cells_Transformed_fibroblasts_0.5.db", "TW_Colon_Sigmoid_0.5.db", "TW_Colon_Transverse_0.5.db", "TW_Esophagus_Gastroesophageal_Junction_0.5.db", "TW_Esophagus_Mucosa_0.5.db", "TW_Esophagus_Muscularis_0.5.db", "TW_Heart_Atrial_Appendage_0.5.db", "TW_Heart_Left_Ventricle_0.5.db", "TW_Liver_0.5.db", "TW_Lung_0.5.db", "TW_Muscle_Skeletal_0.5.db", "TW_Nerve_Tibial_0.5.db", "TW_Ovary_0.5.db", "TW_Pancreas_0.5.db", "TW_Pituitary_0.5.db", "TW_Prostate_0.5.db", "TW_Skin_Not_Sun_Exposed_Suprapubic_0.5.db", "TW_Skin_Sun_Exposed_Lower_leg_0.5.db", "TW_Small_Intestine_Terminal_Ileum_0.5.db", "TW_Spleen_0.5.db", "TW_Stomach_0.5.db", "TW_Testis_0.5.db", "TW_Thyroid_0.5.db", "TW_Uterus_0.5.db", "TW_Vagina_0.5.db", "TW_Whole_Blood_0.5.db"]
db_path = "/home/wheelerlab3/Data/PrediXcan_db/GTEx-V6p-HapMap-2016-09-08/"
output_path = "/home/angela/px_his_chol/MESA_compare/GTEx_WB/SNPs_n_samples/"
sig_gene = pandas.read_csv("/home/angela/px_his_chol/MESA_compare/GTEx_WB/sig_gene_HCHS.csv", engine = "python")

input_genenames = ["PRPF38B", "C1orf194", "CELSR2", "PSRC1", "SORT1", "ATXN7L2", "GSTM1", "APOB", "COX17", "SPEF2", "HMGCR", "ANXA6", "HLA-DRA", "PTGDR2", "TMEM258", "FADS1", "BEST1", "LIPC", "CETP", "NLRC5", "CCL22", "CNGB1", "CALB2", "HPR", "ICAM1", "C19orf52", "DOCK6", "TSPAN16", "DKFZP761J1410", "ELOF1", "ACP5", "ZNF433", "ATP13A1", "FBL", "PLD3", "ZNF234"]
input_genenames = set(input_genenames) #only unique names

for tiss in tissues:
  tissue = []
  #extract just the sig genes in that tiss
  tiss_df = sig_gene.loc[sig_gene['tissue'] == tiss]
  #tiss_df = sig_gene
  #input_genenames = set(tiss_df.genename.values)
  num_input = len(tiss_df.genename.values)
  for input_genename in input_genenames:
    #find gene from gene_name
    for line in open("/home/angela/px_yri_chol/PrediXcan/ChrENGene_forRenaming.txt"):
      arr = line.strip().split()
      (CHR, gene, genename) = arr[0:3]
      genename = genename.replace('"', '')
      if input_genename == genename:
        break
      
    #look for a gene and its SNPs in db
    conn = sqlite3.connect(db_path + tiss)
    c = conn.cursor()
    c.execute('select * from sample_info;')
    for row in c:
      sample_size = row[0]
    #print(sample_size)
    c.execute('select * from weights where gene = ' + gene + ';')
    for row in c:
      rs = str(row[0])
      gene = str(row[1])
      weight = str(row[2])
      tissue.append([rs, gene, input_genename, weight, sample_size, num_input, tiss])
    conn.close()
    #tissue.append(gene_output)
  print(tiss + " " + str(num_input) + " " + str(sample_size))
  tissue_output_df = pandas.DataFrame(tissue)#, columns = ['gene', 'rs', 'sample_size'])
  tissue_output_df.to_csv(output_path + tiss + "_SNPs.txt", index = False, header = False, sep = ",")

