# ##################################################
## Project: PubMed - 
## Script purpose: Main script for PubMed data pipeline
## Date: 04.10.2017
## Author: Asura Enkhbayar
####################################################

library("yaml")

source("pubmed/fetch.R")
source("pubmed/transform.R")

config = yaml.load_file("../config.yml")

# Create needed dirs
output_dir = file.path("../data", config$general$project)
raw_data <- file.path(output_dir, "raw/")
dir.create(output_dir, showWarnings = FALSE)
dir.create(raw_data, showWarnings = FALSE)

# Prepare query
query <- paste(config$pubmed$query, config$pubmed$filters, config$pubmed$daterange, sep = " AND ")

# Scripts
fetch_pubmed_data(query, raw_data, batchsize = 1000)
transform_data(raw_data, output_dir)
