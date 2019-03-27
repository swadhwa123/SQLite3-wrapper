#this file can be run to take user input and pass it to the querying file

#if the python script is run without any flags, just output genenames, cv_R2_avg, rsid, and weights (most common things we use)
parser = argparse.ArgumentParser()

#string inputs
#if none, query all available
parser.add_argument("--db", type = str, action = "store", dest = "db", required = False, help = ".db you want to query.") #"db/gtex_v7_Whole_Blood_imputed_europeans_tw_0.5_signif.db"
parser.add_argument("--genes", type = str, action = "store", dest = "genes", required = False, help = "File containing genes (Ensembl IDs).") #"practice_python_queries/genenames.txt"
parser.add_argument("--genenames", type = str, action = "store", dest = "genenames", required = False, help = "File containing gene names.") #"practice_python_queries/genenames.txt"

#boolean inputs
#EXTRA
parser.add_argument("--n.snps.in.model", action = "store_true", dest = "n_snps_in_model", default = False, help = "Include to output the number of SNPs within the cis window that have non-zero weights, as found by elastic-net.")
parser.add_argument("--test_R2_avg", action = "store_true", dest = "test_R2_avg", default = False, help = "Include to output the average coefficient of determination when predicting values of the hold out fold during nested cross validation.")
parser.add_argument("--cv_R2_avg", action = "store_true", dest = "cv_R2_avg", default = False, help = "Include to output the average coefficient of determination for each of the hold out folds when cross-validation was performed on the entire data set.")
parser.add_argument("--rho_avg", action = "store_true", dest = "rho_avg", default = False, help = "Include to output the average correlation between predicted and observed on the hold out folds when doing nested cross-validation.")
parser.add_argument("--rho_zscore", action = "store_true", dest = "rho_zscore", default = False, help = "Include to output the transformation of rho_avg into a z-score using Stouffer's Method.")
parser.add_argument("--pred.perf.R2", action = "store_true", dest = "pred_perf_R2", default = False, help = "Include to output the rho_avg squared.")
parser.add_argument("--pred.perf.pval", action = "store_true", dest = "pred_perf_pval", default = False, help = "Include to output the p-value for rho_zscore.")

#WEIGHTS (this table depends on the EXTRA table)
parser.add_argument("--rsid", action = "store_true", dest = "rsid", default = False, help = "Include to output the rsids in the models of queried genes.")
parser.add_argument("--varID", action = "store_true", dest = "varID", default = False, help = "Include to output the variant IDs in the models of queried genes. These are string labels of the format chromosome_position_allele1_allele2_build. All varIDs are from build 37 of the HUman Reference Genome.")
parser.add_argument("--ref_allele", action = "store_true", dest = "ref_allele", default = False, help = "Include to output the reference alleles of the SNPs in the models of the queried genes.")
parser.add_argument("--eff_allele", action = "store_true", dest = "eff_allele", default = False, help = "Include to output the effect alleles of the SNPs in the models of the queried genes.")
parser.add_argument("--weight", action = "store_true", dest = "weight", default = False, help = "Include to output the weights for the SNPs that are used to calculate predicted expression for the gene. In predicting the expression for the gene, the weight is multiplied by the count, or estimated count, of the effect allele in individual. This value is added to all other weighted SNPs in the model.")

#SAMPLE INFO
parser.add_argument("--n_samples", action = "store_true", dest = "n_samples", default = False, help = "Include to output the number of samples used the make the .db file.")
parser.add_argument("--population", action = "store_true", dest = "population", default = False, help = "Include to output the population studied.")
parser.add_argument("--tissue", action = "store_true", dest = "tissue", default = False, help = "Include to output the tissue or MESA population from which RNA was sequenced.")

args = parser.parse_args()

#then pass these arguments to further things

#for db/, have the user direct to a FOLDER of db files
  #OR have two db flags - one that iterates through a folder of .dbs and one that is for a specific .db file
    #if ends w/ .db, it's a db (make a list of one)
    #else find all the .dbs in that folder
#iterate through each db file
  #db file will be a column name in final output
#everything is encased in one big loop around a list of db files to parse

#if user did pass genes or genenames
  #store list in genes or genenames variable
#else
  #select gene from extra
  #make all genes into a list

#if the user chose any general flags (anything from EXTRA, WEIGHTS, or SAMPLE INFO)
#if chose anything from extra
#select * from extra
  #it'll output a tuple
  #throw all of this into a list of lists
    #KNOW WHAT EACH INDEX CORRESPONDS TO (see .schema)

#if user chooses any weights flags

#NOTE: we'll probably just query EVERYTHING (aka use *) in SQL b/c I'm more comfortable parsing in pandas than in SQL
