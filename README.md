# Data from: Making headlines: An analysis of US government-funded cancer research mentioned in online media

> This repository provides external input data, code, and analysis scripts to fully reproduce results.

[![DOI](https://zenodo.org/badge/108623455.svg)](https://zenodo.org/badge/latestdoi/108623455)

## Datasets

### Results

The produced dataset consists of 6 different files found in `data/results`:

- `articles_metadata.csv` - basic metadata (doi, title, journal, year)
- `articles_mesh_term_dummies.csv` - dummies for the 13 selected mesh terms
- `articles_mesh_subterm_dummies.csv` - dummies for 12 mesh subterms
- `articles_funding_dummies.csv` - dummies for 7 funding types
- `articles_news_coverage.csv` - news mention counts and dummies for the classified tiers
- `news_mentions_details.csv` - details about individual news articles (PMID, title, venue_name, venue_url, date, URL, summary, and tier)

### Plots

The folder `plots` contains figures and scripts used to create them.

### External datasets

- MeSH terms
  - q2018.bin - (available at the NIH FTP server [here](ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/asciimesh/q2018.bin))
  - d2018.bin - (available at the NIH FTP server [here](ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/asciimesh/d2018.bin))
- List of news outlets (provided by [Altmetric.com](http://altmetric.com/))

## Reproduce results

1. Clone the repository including submodules (note `--recurse-submodules`)
    `git clone --recurse-submodules git@github.com:ScholCommLab/cancer-news.git`
2. Install requirements
    - Python
    `pip install -r requirements.txt`
    - R
		- [rentrez](https://cran.r-project.org/web/packages/rentrez/index.html)
		- [jsonlite](https://cran.r-project.org/web/packages/jsonlite/index.html)
3. Copy `example_config.yml` to `config.yml` and insert your Altmetric key.
4. Run the following scripts:

	1. Collect PubMed data
	`Rscript 01_collect_pubmed.R`

	1. Collect altmetrics from Altmetric.com
	`python 02_collect_altmetrics.py`

	1. Create dummy variables and export data
	```python 03_export_data.py```

## License

<p xmlns:dct="http://purl.org/dc/terms/" xmlns:vcard="http://www.w3.org/2001/vcard-rdf/3.0#">
<a rel="license" href="http://creativecommons.org/publicdomain/zero/1.0/"> <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" /></a>

The created dataset, as specified in the description of [results](#results), is published in the public domain. No rights reserved.

### External datasets

Data provided by the National Library of Medicine (NLM) is distributed under the same conditions as specified by the NLM: [https://www.nlm.nih.gov/databases/download/terms_and_conditions.html](https://www.nlm.nih.gov/databases/download/terms_and_conditions.html)

Data provided by [Altmetric.com LLC](altmetric.com) cannot be further redistributed without their permission.
