# ##################################################
## Project: PubMed - 
## Script purpose: Transform PubMed Data
## Date: 04.10.2017
## Author: Asura Enkhbayar
##################################################

require(jsonlite)

# Reads, transforms, and saves all input json files in the input folder
# and saves them as CSV files in the output_folder
transform_data <- function(input_folder, output_folder) {
  
  # Read data
  file.names <- dir(input_folder, pattern ="json")
  file_index <- 1
  
  for (file in file.names) {
    records = read_json(paste0(input_folder, file))

    # init data frame
    column_names <- c("pmid", "doi", "title", "journal", "pub_year", "pub_types", "mesh_terms", "grants", "authors", "author_affils")
    df <- data.frame(matrix(ncol = length(column_names), nrow = length(records)))
    colnames(df) <- column_names
    
    # iterate over records and read out needed data
    row_index = 1
    for (record in records) {
      # title, journal, pubdate (ArticleDate)
      pub_year <- record$MedlineCitation$DateCreated$Year[[1]]
      title <- record$MedlineCitation$Article$ArticleTitle[[1]]
      journal <- record$MedlineCitation$Article$Journal$Title[[1]]

      # PMID & DOI
      ids <- record$PubmedData$ArticleIdList
      pmid <- ids[[match("pubmed", sapply(ids, "[[", ".attrs"))]]$text[[1]]
      doi <- ids[[match("doi", sapply(ids, "[[", ".attrs"))]]$text[[1]]
      if (is.null(doi)) {
        doi <- "NA"
      }
      
      # Author Information
      authors <- list()
      author_affils <- list()
      if ("AuthorList" %in% names(record$MedlineCitation$Article)) {
        if ("CollectiveName" %in% names(record$MedlineCitation$Article$AuthorList$Author)) {
          authors <- record$MedlineCitation$Article$AuthorList$Author$CollectiveName[[1]]
          author_affils <- "NA"
        } else {
          for (author in record$MedlineCitation$Article$AuthorList) {
            authors <- c(authors, paste(author$ForeName[[1]], author$LastName[[1]]))
            affil <- author$AffiliationInfo$Affiliation[[1]]
            affil <- if(is.null(affil)) "NA" else affil
            author_affils <- c(author_affils, affil)
          }
        }
      } else {
        authors <- "NA"
        author_affils <- "NA"
      }
      authors = toJSON(unlist(authors))
      author_affils = toJSON(unlist(author_affils))
      
      # MeSH terms
      mesh_desc = c()
      mesh_qual = list()
      for (mesh_item in record$MedlineCitation$MeshHeadingList) {
        mesh_desc = c(mesh_desc, tolower(mesh_item$DescriptorName$text))
        
        if (length(mesh_item) == 1) {
          mesh_qual = c(mesh_qual, "NA")
        } else {
          x = c()
          for (item in mesh_item[-1]) {
            x = c(x, tolower(item$text[[1]]))
          }
          mesh_qual[[length(mesh_qual)+1]] <- x
        }
      }
      names(mesh_qual) <- mesh_desc
      mesh_object <- toJSON(mesh_qual)
      
      # Publicatoin
      pub_types <- toJSON(unlist(sapply(record$MedlineCitation$Article$PublicationTypeList, "[[", "text")))

      # Grants
      grants <- toJSON(unlist(sapply(head(record$MedlineCitation$Article$GrantList,-1), function(x)return(x$GrantID[[1]]))))
      
      # Debugging output and problematic rows
      # print(paste0("==== RECORD ", row_index, " ===="))
      # print(pmid)
      # print(doi)
      # print(title)
      # print(journal)
      # print(pub_year)
      # print(pub_types)
      # print(mesh_object)
      # print(grants)
      # print(authors)
      # print(author_affils)
      
      article = list(pmid, doi, title, journal, pub_year, pub_types, mesh_object, grants, authors, author_affils)
      df[row_index, ] <- article
      
      row_index <- row_index + 1
    }
    
    write.csv(df, paste0(output_folder, "/records_", file_index, ".csv"), row.names=FALSE)
    message(paste0("Processed file ", file_index, " out of ", length(file.names)))
    file_index <- file_index + 1
  }
}