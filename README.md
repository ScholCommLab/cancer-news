# Cancer News Study

Scripts needed to reproduce results and download data.

## Requirements

- R
- Python 3.5
- Jupyter Notebook

## Overview of repository

### Download your own dataset
While the lates dataset that was used to run analyses is checked in the repository, you will still need to run the download scripts yourself to reproduce the full pipeline + intermediate results.

PubMed API is accessed using the *rentrez* package from [rOpenSci](https://ropensci.org/tutorials/rentrez_tutorial/). Head over to `get_pubmed/` and have a look at `main.R`. Data acquisition runs in three steps:

- Fetching data from PubMed and store original dump as JSON
- Transform data and save as CSV (still containing some JSON fields)
- Merge files

### Notebooks
Further analyses were conducted in Jupyter Notebooks:

- [`overview.ipynb`](notebooks/overview.ipynb)

    Reading in the dump from R and run some scripts. A few plots & thoughts. Will eventually be used for anything related to the initial dataset

- [`export_data.ipynb`](notebooks/export_data.ipynb)

    This notebook produces whichever data format is used for the actual statistical analyses. Will probably be tweaked over time according to needs
    
## Available data (follow links to download)

- [data/full_cancer_data.csv](data/full_cancer_data.csv) is the dataset that was acquired from PubMed incl. some transformations. Contains 2012-2017
- [data/news_outlets.csv](data/news_outlets.csv) classification of news outlets on Altmetric.com
- [data/output/](data/output) contains datasets produced by Jupyter Notebooks
    - [2016_cancer_data.csv](data/output/2016_cancer_data.csv) identical to `full_cancer_data`. restricted to 2016
    - [2016_mesh_descriptors.csv](data/output/2016_mesh_descriptors.csv) MeSH headings and their occurances in the year 2016
    - [2016_mesh_qualifiers.csv](data/output/2016_mesh_qualifiers.csv) MeSH qualifiers and their occurances in the year 2016
    - [2016_with_dummies.csv](data/output/2016_with_dummies.csv) contains selected combinations of MeSH headings and qualifiers coded as dummy variables for the year 2016
    
## To-Do

- Be more specific about requirements
