* Encoding: UTF-8.
DATASET ACTIVATE DataSet1.
SAVE OUTFILE='\newsmention_study_10_2020_dataset1.sav'
  /COMPRESSED.

* Check total number of unique PMIDs - the first two columns from this output table (PMID and frequency) from the code below 
were exported into a second dataset (with one unique PMID per row) in order to calculate the mean, median, and mode f
or the 213 unique PMIDs in the data. 

FREQUENCIES VARIABLES=PMID
  /NTILES=4
  /ORDER=ANALYSIS.

* Copy column 1 (PMID) and column 2 (frequency) into second dataset 
    
SAVE OUTFILE='\newsmention_study_10_2020_dataset2.sav' 
  /COMPRESSED. 
DATASET ACTIVATE DataSet2.
FREQUENCIES VARIABLES=PMID 
  /ORDER=ANALYSIS.

* Code above is run on dataset2 to confirm that there are 213 unique PMIDs (journal articles) with news mentions
    
FREQUENCIES VARIABLES=frequency 
  /STATISTICS=RANGE MINIMUM MAXIMUM MEAN MEDIAN MODE SKEWNESS SESKEW KURTOSIS SEKURT 
  /ORDER=ANALYSIS.

* Code above generates mean, median, mode, and range for the number of news mentions across all 213 articles 
   
DATASET ACTIVATE DataSet1.
FREQUENCIES VARIABLES=UrinaryBladderNeoplasms BreastNeoplasms ColorectalNeoplasms 
    EndometrialNeoplasms KidneyNeoplasms Leukemia LiverNeoplasms LungNeoplasms Melanoma 
    LymphomaNonHodgkin PancreaticNeoplasms ProstaticNeoplasms ThyroidNeoplasms totalcancer anycancer 
  /NTILES=4 
  /ORDER=ANALYSIS
  
* Code above provides frequencies for common cancer types included across 642 news mentions (included in Table 2)
    
FREQUENCIES VARIABLES=NewsOutlet newstype 
  /NTILES=4 
  /ORDER=ANALYSIS.

* Code above provides frequencies for types of news outlets and frequencies of mentions for each individual news outlet
    (see Table 3 and Table 4). 

CROSSTABS 
  /TABLES=newstype BY anycancer 
  /FORMAT=AVALUE TABLES 
  /STATISTICS=CHISQ CORR 
  /CELLS=COUNT 
  /COUNT ROUND CELL.

* Above code provides Chi squared test of common cancer mention (0/1) across news types. 

* Note: A simple ratio for estimated annual deaths (from NCI mortality data, Table 2) to news mentions was calculated in Excel for
each common cancer type and reported in Figure 1. 


