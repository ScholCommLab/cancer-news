require(dplyr)
require(readr)

merge_data = function(input_folder, output_folder){
  df <- list.files(input_folder, full.names = TRUE) %>% 
    lapply(read_csv) %>% 
    bind_rows
  
  write.csv(df, paste0(output_folder, "cancer_data.csv"), row.names = FALSE)
}