# SQLite3-wrapper
Developing a Python wrapper for SQLite3 to take in parameters from the user and automate the queries to the database, producing .csv files ready for parsing

Summary: https://docs.google.com/presentation/d/1Xarn0oowpogUH9NmHpkTC-sKIEeIR__ac2_Azgp5Ilo/edit?usp=sharing

PrediXcan paper (see methods): https://www.nature.com/articles/ng.3367

GTEx about: https://gtexportal.org/home/documentationPage

GTEx portal: http://science.sciencemag.org/content/348/6235/648

Description of layout of .db files: https://s3.amazonaws.com/predictdb2/contributed/MESA-2018-05-v2/MESAdb_2018-05-28_updated_README.txt

# 1)	REQUIREMENT’S:
    -Documentation (Angela)
    -SQL querying (Carlee)
    -CSV parsing (Shreya)
# 2)	WHO IS OUR USER?
    The Wheeler Lab
# 3)	WHAT IS OUR GOAL?
    To take parameters(gene id, gene name, # of SNPs in the model, 
    test r^2 average, cross validation of r^2 average, etc.) from 
    the user and query databases from PredictDB.org to gather info 
    about geneotype, gene expression, and associations. This info 
    will be placed in a .csv file for the user to parse/use. 
# 4)  SOFTWARE NEEDED:
    SQL, Pandas, .db files(input)
# 5)	PLAN OF ACTION
