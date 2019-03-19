import sqlite3
import pandas
pops = ["AFA", "AFHI", "ALL", "CAU", "HIS"]
#Populations, African-American, African american hispanic, african american hispanic caucasian, caucasian, hispanic
path = "/home/angela/MESA_dbs/"

genename_R2 = []
for pop in pops:
    conn = sqlite3.connect(path + pop + "_imputed_10_peer_3_pcs_v2.db") #connect to .db file
    c = conn.cursor()
    c.execute('SELECT (`gene` || " " || `genename` || " " || `pred.perf.r2`) FROM EXTRA;') #run search throguh python
    #Extra database stores gene by gene information 
    for row in c:
      row = row[0].split(" ") #tuple is just one element, so split into two
      genename_R2.append([row[0], row[1], row[2], pop]) #extract gene name and R2
    conn.close()
genename_R2_df = pandas.DataFrame(genename_R2, columns = ['gene', 'genename', 'R2', 'pop']) #make list of lists into df
genename_R2_df.to_csv(path + "genename_R2.txt", index = False) #print to file
