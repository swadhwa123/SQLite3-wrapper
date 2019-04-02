#this script pulls the gene IDs (ensembl IDs) and the names and weights of the SNPs in the model for that gene
import sqlite3
import pandas as pd

NA_genes = pd.read_csv("dissonant_assocs.csv")
weights = []
for assoc in NA_genes.iterrows():
    (genename, model, pheno) = assoc[1] #this .csv is organized like the tuples described
    if model in ["AFA", "AFHI", "ALL", "CAU", "HIS"]: #if MESA
        conn = sqlite3.connect("/home/lauren/files_for_revisions_plosgen/en_v7/dbs/" + model + "_imputed_10_peer_3_filtered.db")
    else: #if GTEx
        conn = sqlite3.connect("/home/wheelerlab3/Data/PrediXcan_db/GTEx-V6p-HapMap-2016-09-08/TW_" + model + "_0.5.db")
    c = conn.cursor()
    c.execute("select gene from extra where genename = '" + genename + "';") #find ensembl id from gene name
    for row in c: #should be one row
        gene = row[0] #got ensembl id
    c.execute("select rsid,weight from weights where gene = '" + gene + "';") #query information of the gene we're looking at
    for row in c: #all we want are rsids and weights
        rs = str(row[0])
        weight = str(row[1])
        weights.append([genename, rs, weight, model, pheno]) #add all to results table
    conn.close()
weights_df = pd.DataFrame(weights) #create dataframe from list of lists
weights_df.columns = ["genename", "rsid", "weight", "model", "pheno"]
weights_df.to_csv("dissonant_assocs_weights.csv", index = False, sep = ",") #write to file
print("Done writing .csv. Have a nice day :).")

