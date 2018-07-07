# ##################################################
## Project: PubMed - 
## Script purpose: Main script for PubMed data pipeline
## Date: 04.10.2017
## Author: Asura Enkhbayar
####################################################

require(yaml)
require(jsonlite)
require(rentrez)
require(XML)

######################
#
#   Functions
#
######################


# Fetches data from PubMed
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
    if (file_count == 2) {
      return()
    }
  }
}

# Reads, transforms, and saves all input json files in the input folder
# and saves them as CSV files in the output_folder
transform_data <- function(input_folder, output_folder, verbose=FALSE) {
  
  # Read data
  file.names <- dir(input_folder, pattern ="json")
  file_index <- 1
  
  df <- data.frame(pmid=integer(),
                   doi=character(),
                   title=character(),
                   journal=character(),
                   pub_year=integer(),
                   pub_types=character(),
                   mesh_terms=character(),
                   grants=character(),
                   authors=character(),
                   author_affils=character(),
                   stringsAsFactors = FALSE)
  
  for (file in file.names) {
    records = read_json(paste0(input_folder, file))
    for (record in records) {
      # title, journal, pubdate (ArticleDate)
      pub_year <- record$MedlineCitation$Article$ArticleDate$Year
      if (is.null(pub_year)) {
        pub_year <- record$MedlineCitation$Article$Journal$JournalIssue$PubDate$Year
      }
      if (is.null(pub_year)) {
        pub_year <- substr(record$MedlineCitation$Article$Journal$JournalIssue$PubDate$MedlineDate[[1]], 1, 4)
      }
      title <- record$MedlineCitation$Article$ArticleTitle[[1]]
      journal <- record$MedlineCitation$Article$Journal$Title[[1]]
      
      # PMID & DOI
      ids <- record$PubmedData$ArticleIdList
      pmid <- ids[[match("pubmed", sapply(ids, "[[", ".attrs"))]]$text[[1]]
      doi <- ids[[match("doi", sapply(ids, "[[", ".attrs"))]]$text[[1]]
      
      # Author Information
      authors <- list()
      author_affils <- list()
      if ("AuthorList" %in% names(record$MedlineCitation$Article)) {
        if ("CollectiveName" %in% names(record$MedlineCitation$Article$AuthorList$Author)) {
          authors <- record$MedlineCitation$Article$AuthorList$Author$CollectiveName[[1]]
          author_affils <- "NA"
        } else {
          for (author in record$MedlineCitation$Article$AuthorList) {
            authors[[length(authors)+1]] <- paste(author$ForeName[[1]], author$LastName[[1]])
            affil <- author$AffiliationInfo$Affiliation[[1]]
            if (is.null(affil)) {
              affil = "NA"
            }
            author_affils[[length(author_affils)+1]] <- affil
          }
        }
      } else {
        authors <- "NA"
        author_affils <- "NA"
      }
      authors = authors
      author_affils = author_affils
      
      # MeSH terms
      mesh_desc = c()
      mesh_qual = list()
      for (mesh_item in record$MedlineCitation$MeshHeadingList) {
        mesh_desc = c(mesh_desc, mesh_item$DescriptorName$text)
        
        if (length(mesh_item) == 1) {
          mesh_qual = c(mesh_qual, "NA")
        } else {
          x = c()
          for (item in mesh_item[-1]) {
            x = c(x, item$text[[1]])
          }
          mesh_qual[[length(mesh_qual)+1]] <- x
        }
      }
      names(mesh_qual) <- mesh_desc
      mesh_object <- mesh_qual
      
      # Publicatoin
      pub_types <- sapply(record$MedlineCitation$Article$PublicationTypeList, function(x)return(x$text[[1]]))
      
      # Grants
      grants = sapply(head(record$MedlineCitation$Article$GrantList,-1), function(x)return(x$GrantID[[1]]))
      
      article = list(as.numeric(pmid),
                     toString(doi),
                     toString(title),
                     toString(journal),
                     as.numeric(pub_year),
                     toJSON(pub_types),
                     toJSON(mesh_object),
                     toJSON(grants),
                     toJSON(unlist(authors)),
                     toJSON(unlist(author_affils)))
      article = lapply(article, function(x)if (x == "[]") return("") else return(x))
      
      # Debugging output
      if (verbose) {
        print(article)
      }
      
      df[nrow(df)+1,] <- article
    }
    
    message(paste0("Processed file ", file_index, " out of ", length(file.names)))
    file_index <- file_index + 1
  }
  
  write(toJSON(df), paste0(output_folder, "/cancer_data.json"))
}

######################
#
#   Start of script
#
######################

config = yaml.load_file("../config.yml")

# Create needed dirs
data_dir <- file.path("../data/temp")
temp_dir <- file.path(data_dir, "raw/")
dir.create(data_dir, showWarnings = FALSE)
dir.create(temp_dir, showWarnings = FALSE)

# Prepare query
query <- paste(config$pubmed$query, config$pubmed$filters, config$pubmed$daterange, sep = " AND ")

# Scripts
fetch_pubmed_data(query, temp_dir, batchsize = 10)
transform_data(temp_dir, data_dir)
