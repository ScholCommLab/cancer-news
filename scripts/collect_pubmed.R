# ##################################################
## Project: PubMed - 
## Script purpose: Main script for PubMed data pipeline
## Date: 04.10.2017
## Author: Asura Enkhbayar
####################################################

source("pubmed/fetch.R")
source("pubmed/transform.R")

# Paths
output_path = "../data/rerun/"
orig_path <- paste0(output_path, "original/")

# Get data
keywords <- "(neoplasm [mesh] OR \"neoplasm metastasis\" [mesh] OR cancer*[tiab] OR malign*[tiab] OR neoplas*[tiab] OR oncolo*[tiab] OR metasta*[tiab] OR tumor*[tiab] OR tumour*[tiab])"
filters <- "(\"research support, american recovery and reinvestment act\"[Publication Type] OR \"research support, n i h, extramural\"[Publication Type] OR \"research support, n i h, intramural\"[Publication Type] OR \"research support, non u s gov't\"[Publication Type] OR \"research support, u s gov't, non p h s\"[Publication Type] OR \"research support, u s gov't, p h s\"[Publication Type] OR \"research support, u s government\"[Publication Type])"
daterange <- "(\"2016/01/01\"[Date - Publication] : \"2016/12/31\"[Date - Publication])"
query <- paste(keywords, filters, daterange, sep = " AND ")

# Scripts
fetch_pubmed_data(query, orig_path)
transform_data(orig_path, output_path)
