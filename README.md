# Cancer News Study

Code and analyses needed to reproduce and re-download data

## Requirements
- R
- Python 3.5
- Jupyter Notebook

## Overview of repository

**Download your own dataset**
While the lates dataset that was used to run analyses is checked in the repository, you will still need to run the download scripts yourself to reproduce the full pipeline + intermediate results.

PubMed API is accessed using the *rentrez* package from [rOpenSci](https://ropensci.org/tutorials/rentrez_tutorial/). Head over to `get_pubmed/` and have a look at `main.R`. Data acquisition runs in three steps:

- Fetching data from PubMed and store original dump as JSON
- Transform data and save as CSV (still containing some JSON fields)
- Merge files

**Work in Progress**
Further analyses were conducted in Jupyter Notebooks:

- [`overview.ipynb`](notebooks/overview.ipynb)

    Reading in the dump from R and run some scripts. A few plots & thoughts. Will eventually be used for anything related to the initial dataset

- [`export_data.ipynb`](notebooks/export_data.ipynb)

    This notebook produces whichever data format is used for the actual statistical analyses. Will probably be tweaked over time according to needs
    
## To-Do

- Be more specific about requirements
