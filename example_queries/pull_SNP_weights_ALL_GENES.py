import sqlite3
import pandas
pops = ["AFA", "AFHI", "ALL", "CAU", "HIS"]
input_genenames = ["PRPF38B", "C1orf194", "CELSR2", "PSRC1", "SORT1", "ATXN7L2", "GSTM1", "APOB", "COX17", "SPEF2", "HMGCR", "ANXA6", "HLA-DRA", "PTGDR2", "TMEM258", "FADS1", "BEST1", "LIPC", "CETP", "NLRC5", "CCL22", "CNGB1", "CALB2", "HPR", "ICAM1", "C19orf52", "DOCK6", "TSPAN16", "DKFZP761J1410", "ELOF1", "ACP5", "ZNF433", "ATP13A1", "FBL", "PLD3", "ZNF234"]
input_genenames = set(input_genenames) #only unique names
db_path = "/home/lauren/files_for_revisions_plosgen/en_v7/dbs/"
output_path = "/home/angela/px_his_chol/MESA_compare/sig_gene_weights/"
sig_gene = pandas.read_csv("/home/angela/px_his_chol/MESA_compare/GTEx_WB/sig_gene_HCHS.csv", engine = "python")

input_genenames = ["PRPF38B", "C1orf194", "CELSR2", "PSRC1", "SORT1", "ATXN7L2", "GSTM1", "APOB", "COX17", "SPEF2", "HMGCR", "ANXA6", "HLA-DRA", "PTGDR2", "TMEM258", "FADS1", "BEST1", "LIPC", "CETP", "NLRC5", "CCL22", "CNGB1", "CALB2", "HPR", "ICAM1", "C19orf52", "DOCK6", "TSPAN16", "DKFZP761J1410", "ELOF1", "ACP5", "ZNF433", "ATP13A1", "FBL", "PLD3", "ZNF234"]
input_genenames = set(input_genenames) #only unique names

for tiss in pops:
  tissue = []
  #extract just the sig genes in that tiss
  tiss_df = sig_gene.loc[sig_gene['tissue'] == tiss]
  #tiss_df = sig_gene
  #input_genenames = set(tiss_df.genename.values)
  num_input = len(tiss_df.genename.values)
  #look for a gene and its SNPs in db
  conn = sqlite3.connect(db_path + tiss + "_imputed_10_peer_3.db")
  c = conn.cursor()
  c.execute('select * from sample_info;')
  for row in c:
    sample_size = row[0]
  #print(sample_size)
  c.execute('select * from weights;')
  for row in c:
    rs = str(row[1])
    gene = str(row[0])
    weight = str(row[5])
    tissue.append([rs, gene, weight, sample_size, num_input, tiss])
  conn.close()
  #tissue.append(gene_output)
  print(tiss + " " + str(num_input) + " " + str(sample_size))
  tissue_output_df = pandas.DataFrame(tissue)#, columns = ['gene', 'rs', 'sample_size'])
  tissue_output_df.to_csv(output_path + tiss + "_SNPs_all_genes.txt", index = False, header = False, sep = ",")
