# ##################################################
## Project: PubMed - 
## Script purpose: Crawl pubmed results
## Date: 04.10.2017
## Author: Asura Enkhbayar
##################################################

require(rentrez)
require(XML)
require(plyr)
require(jsonlite)

# Fetches
fetch_pubmed_data <- function(query, output_folder) {
	# Perform entrez search with web_history to retrieve web_history object
	res <- entrez_search(db="pubmed", term=query, use_history=TRUE)
	print(paste0("Found ", res$count, " results"))

	batch_size <- 1000
	max_seq <- res$count
	file_count <- 0
	number_loops <- ceiling(max_seq / batch_size)

	for(seq_start in seq(file_count*batch_size, max_seq, batch_size)){
	  recs <- entrez_fetch(db="pubmed", web_history=res$web_history, rettype="XML", retmax=batch_size, retstart=0)
	  json <- toJSON(xmlToList(xmlParse(recs)))
	  write(json, file=paste0(output_folder, "records_",file_count,".json"))
	  print(paste0("Batch ", file_count, " out of ", number_loops))
	  file_count <- file_count + 1
	}

}
