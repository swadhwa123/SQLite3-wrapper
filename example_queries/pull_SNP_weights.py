#this script pulls the gene IDs (ensembl IDs) and the names and weights of the SNPs in the model for that gene

import sqlite3
import pandas
pops = ["AFA", "AFHI", "ALL", "CAU", "HIS"] #iterate through all MESA models
input_genenames = ["PRPF38B", "C1orf194", "CELSR2", "PSRC1", "SORT1", "ATXN7L2", "GSTM1", "APOB", "COX17", "SPEF2", "HMGCR", "ANXA6", "HLA-DRA", "PTGDR2", "TMEM258", "FADS1", "BEST1", "LIPC", "CETP", "NLRC5", "CCL22", "CNGB1", "CALB2", "HPR", "ICAM1", "C19orf52", "DOCK6", "TSPAN16", "DKFZP761J1410", "ELOF1", "ACP5", "ZNF433", "ATP13A1", "FBL", "PLD3", "ZNF234"] #don't ask how I got these gene names just run with it
input_genenames = set(input_genenames) #only unique names
db_path = "/home/lauren/files_for_revisions_plosgen/en_v7/dbs/" #a few paths of where some files are
output_path = "/home/angela/px_his_chol/MESA_compare/sig_gene_weights/"
sig_gene = pandas.read_csv("/home/angela/px_his_chol/MESA_compare/GTEx_WB/sig_gene_HCHS.csv", engine = "python") #don't worry about it
input_genenames = set(input_genenames) #only unique names

for tiss in pops:
  tissue = []
  ''' dont worry about it
  #extract just the sig genes in that tiss
  tiss_df = sig_gene.loc[sig_gene['tissue'] == tiss]
  #tiss_df = sig_gene
  #input_genenames = set(tiss_df.genename.values)
  num_input = len(tiss_df.genename.values)
  '''
  for input_genename in input_genenames:
    for line in open("/home/angela/px_yri_chol/PrediXcan/ChrENGene_forRenaming.txt"): #find gene from gene_name
      arr = line.strip().split()
      (CHR, gene, genename) = arr[0:3]
      genename = genename.replace('"', '')
      if input_genename == genename: #found the right gene/ENSG!
        break
      
    #look for a gene and its SNPs in db
    conn = sqlite3.connect(db_path + tiss + "_imputed_10_peer_3_filtered.db") #see previous examples
    c = conn.cursor()
    c.execute('select * from sample_info;') #new table: sample_info
    for row in c:
      sample_size = row[0] #sample size of the model is first in the tuple
    #print(sample_size)
    c.execute('select * from weights where gene = ' + gene + ';') #query information of the gene we're looking at
    for row in c:
      rs = str(row[1])
      gene = str(row[0])
      weight = str(row[5])
      tissue.append([rs, gene, input_genename, weight, sample_size, num_input, tiss]) #create list of lists including rs of snps in gene model, ensembl id, gene name, weight of SNP in the gene expression model, sample size of model, don't worry about it, and the model queried from
    conn.close() #https://www.youtube.com/watch?v=PVWpgmiIbas
    #tissue.append(gene_output)
#  print(tiss + " " + str(num_input) + " " + str(sample_size))
  tissue_output_df = pandas.DataFrame(tissue) #create dataframe from list of lists
  tissue_output_df.to_csv(output_path + tiss + "_SNPs.txt", index = False, header = False, sep = ",") #write to file
