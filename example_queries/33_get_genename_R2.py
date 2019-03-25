#this script iterates through the five MESA populations and pulls genes, gene names, and predictive performance R^2 for all models into one total dataframe

import sqlite3
import pandas
pops = ["AFA", "AFHI", "ALL", "CAU", "HIS"] #Populations, African-American, African american hispanic, african american hispanic caucasian, caucasian, hispanic
path = "/home/angela/MESA_dbs/"

genename_R2 = [] #list to store all data in
for pop in pops: #iterate through all pops
    conn = sqlite3.connect(path + pop + "_imputed_10_peer_3_pcs_v2.db") #connect to .db file
    c = conn.cursor() #create cursor to put queries through (? I don't know exact terminology)
    c.execute('SELECT (`gene` || " " || `genename` || " " || `pred.perf.r2`) FROM EXTRA;') #run search through python; "extra" database stores gene by gene information 
    for row in c: #iterate through the output of the query
      row = row[0].split(" ") #tuple is just one element, so split into two; happens b/c of the ` || " " || ` in the query
      genename_R2.append([row[0], row[1], row[2], pop]) #extract gene, gene name, and R2 from the row tuple and make into list to append to list of lists
    conn.close() #close everything you open
genename_R2_df = pandas.DataFrame(genename_R2, columns = ['gene', 'genename', 'R2', 'pop']) #make list of lists into df
genename_R2_df.to_csv(path + "genename_R2.txt", index = False) #print to file
