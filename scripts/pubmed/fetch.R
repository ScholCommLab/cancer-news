# ##################################################
## Project: PubMed - 
## Script purpose: Crawl pubmed results
## Date: 04.10.2017
## Author: Asura Enkhbayar
##################################################

require(rentrez)
require(XML)
require(jsonlite)

# Fetches
fetch_pubmed_data <- function(query, output_folder, batchsize) {
  # Perform entrez search with web_history to retrieve web_history object
	res <- entrez_search(db="pubmed", term=query, use_history=TRUE)
	print(paste0("Found ", res$count, " results"))

	number_loops <- ceiling(res$count / batchsize)
	
	file_count <- 0
	for(seq_start in seq(file_count*batchsize, res$count, batchsize)){
	  print(paste0("Starting batch ", file_count, " out of ", number_loops))
	  recs <- entrez_fetch(db="pubmed", web_history=res$web_history, rettype="XML", retmax=batchsize, retstart=seq_start)
	  json <- toJSON(xmlToList(xmlParse(recs)))
	  write(json, file=paste0(output_folder, "records_",file_count,".json"))
	  file_count <- file_count + 1
	}
}
