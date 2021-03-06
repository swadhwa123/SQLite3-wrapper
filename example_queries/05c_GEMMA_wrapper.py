#this file is an example of how to use flags and date from argparse within a Python script

#runs a GWAS loop around given phenotypes; all input except for genotypes must be already in GEMMA format
#by Angela Andaleon (aandaleon@luc.edu)
import argparse
import numpy as np
import pandas as pd
import os
pd.options.mode.chained_assignment = None

parser = argparse.ArgumentParser() #open the parser
#GWAS and pred_exp flags tell the program which "mode" to go in; if neither, throws error
parser.add_argument("--GWAS", action = "store_true", dest = "GWAS", default = False, help = "Include to perform GWAS")
parser.add_argument("--pred_exp", action = "store_true", dest = "pred_exp", default = False, help = "Include to perform linear mixed model with predicted expression")
#these following flags contain strings that are used to direct to files; the strings can be used in other wats as well
#these flags also have "default" which is used if the user does not specify an input. CAN BE VERY USEFUL IF YOU HAVE A LAZY/CLUELESS USER (aka yourself while testing).
parser.add_argument("--relatedness", type = str, action = "store", dest = "relatedness", required = False, default = "relatedness_woIID.txt", help = "Path to file containing relatedness matrix w/o IIDs for only individuals in analysis.")
parser.add_argument("--geno_prefix", type = str, action = "store", dest = "geno_prefix", default = "BIMBAM/chr", required = False, help = "Prefix of BIMBAM files Default = 'BIMBAM/chr'. If running with predicted expression, direct to converted pseudo-genotypes.")
parser.add_argument("--pheno", type = str, action = "store", dest = "pheno", required = False, default = "pheno_woIID.txt", help = "Path to file containing phenotypic information w/o IIDs for only individuals in analysis.")
parser.add_argument("--pheno_names", type = str, action = "store", dest = "pheno_names", required = False, default = "pheno_names.txt", help = "Path to file containing names of phenotypes.")
parser.add_argument("--covariates", type = str, action = "store", dest = "covariates", required = False, default = "GEMMA_covars.txt", help = "Path to file containing covariates w/o IIDs for only individuals in analysis.")
parser.add_argument("--anno", type = str, action = "store", dest = "anno", required = False, default = "anno/anno", help = "(Optional) Path to file containing the annotations, including 'anno'.")
#parser.add_argument("--output", type = str, action = "store", dest = "output", required = False, default = "", help = "Name of output file")

args = parser.parse_args() #interpret the user's input

print("Reading input files.") #following are to be used in GEMMA input
#following assigns the argument inputs to strings
GWAS = args.GWAS #if user does not input this, it's stored as False (boolean)
pred_exp = args.pred_exp
#the rest of these are storing strings, including just processing the default if the user didn't specify anytihing
if args.anno is None:
    anno = " "
else:
    anno = " -a " + args.anno
if args.covariates is None:
    covariates_file = " "
else:
    covariates_file = " -c " + args.covariates + " "
pheno_file = args.pheno
pheno_names = args.pheno_names
relatedness = args.relatedness
#if args.output is None or args.output == "":
#    output = ""
#else:
#    output = args.output
output = ""
geno_prefix = args.geno_prefix

''' sample data
anno = " -a anno/anno"
covariates_file = " -c covar_woIID.txt "
pheno_file = "pheno_woIID.txt"
pheno_names = "pheno_names.txt"
relatedness = "relatedness_woIID.txt"
geno_prefix = "BIMBAM/chr"
output = "AMR"
'''

pheno_names = list(np.loadtxt(pheno_names, dtype = "str", ndmin = 1)) #phenos as list
pheno_nums = range(1, len(pheno_names) + 1) #cause GEMMA does things by indexes

if not GWAS and not pred_exp: #if both are false
    print("Error: User did not specify --GWAS or --pred_exp. Please specify one or both options.")

if GWAS: #GWAS-specific shiz
    for pheno_num, pheno_name in zip(pheno_nums, pheno_names):  #phenotype loop; iterates through two lists simultaneously 
        print("Starting analyses on " + pheno_name + ".")
        for chr in range(1, 23): #process all chrs.
            if output == "": #this is just a weird thing involving the _ and cause it looks ugly if there's no specified output
                GEMMA_command = "gemma -g " + geno_prefix + str(chr) + ".txt.gz -p " + pheno_file + " -n " + str(pheno_num) + anno + str(chr) + ".txt -k " + relatedness + covariates_file + " -lmm 4 -o " + pheno_name + "_chr" + str(chr)
            else:
                GEMMA_command = "gemma -g " + geno_prefix + str(chr) + ".txt.gz -p " + pheno_file + " -n " + str(pheno_num) + anno + str(chr) + ".txt -k " + relatedness + covariates_file + " -lmm 4 -o " + output + "_" + pheno_name + "_chr" + str(chr)
            os.system(GEMMA_command + " >> GEMMA_log.txt") #append to file b/c doing GEMMA so much clogs up the screen
            print("Completed with chr. " + str(chr) + ".")
        print("Ending analyses on " + pheno_name + ".")
    print("Analyses in all phenotypes is complete. Have a nice day :)!")
    
if pred_exp: #tissues are GTEx V6. Change as you see fit.
    geno_prefix = "pred_exp_GEMMA/" #this used to be a user input then I learned to not trust the user
    tissues = ["AFA", "AFHI", "ALL", "CAU", "HIS", "Adipose_Subcutaneous", "Adipose_Visceral_Omentum", "Adrenal_Gland", "Artery_Aorta", "Artery_Coronary", "Artery_Tibial", "Brain_Anterior_cingulate_cortex_BA24", "Brain_Caudate_basal_ganglia", "Brain_Cerebellar_Hemisphere", "Brain_Cortex", "Brain_Frontal_Cortex_BA9", "Brain_Hippocampus", "Brain_Hypothalamus", "Brain_Nucleus_accumbens_basal_ganglia", "Brain_Putamen_basal_ganglia", "Breast_Mammary_Tissue", "Cells_EBV-transformed_lymphocytes", "Cells_Transformed_fibroblasts", "Colon_Sigmoid", "Colon_Transverse", "Esophagus_Gastroesophageal_Junction", "Esophagus_Mucosa", "Esophagus_Muscularis", "Heart_Atrial_Appendage", "Heart_Left_Ventricle", "Liver", "Lung", "Muscle_Skeletal", "Nerve_Tibial", "Ovary", "Pancreas", "Pituitary", "Prostate", "Skin_Not_Sun_Exposed_Suprapubic", "Skin_Sun_Exposed_Lower_leg", "Small_Intestine_Terminal_Ileum", "Spleen", "Stomach", "Testis", "Thyroid", "Uterus", "Vagina", "Whole_Blood"] 
    for pheno_num, pheno_name in zip(pheno_nums, pheno_names):   
        print("Starting analyses on " + pheno_name + ".")
        for tissue in tissues:
            if output == "": #running -notsnp cause these predicted expressions aren't constrained b/w 0-2
                GEMMA_command = "gemma -g " + geno_prefix + tissue + ".txt -p " + pheno_file + " -n " + str(pheno_num) + " -k " + relatedness + covariates_file + " -lmm 4 -notsnp -o " + pheno_name + "_" + tissue
            else:
                GEMMA_command = "gemma -g " + geno_prefix + tissue + ".txt -p " + pheno_file + " -n " + str(pheno_num) + " -k " + relatedness + covariates_file + " -lmm 4 -notsnp -o " + output + "_" + pheno_name + "_" + tissue
            os.system(GEMMA_command + " >> GEMMA_log.txt")
            print("Completed with " + tissue + ".")
        print("Ending analyses on " + pheno_name + ".")
    print("Analyses in all phenotypes is complete. Have a nice day :)!")
