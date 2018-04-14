# Cancer News Study

Scripts needed to download dat and reproduce results.

## Requirements

- R
  - rentrez
  - jsonlite
- Python 3.5
  - See `requirements.txt`

## Overview of repository

### Reproduce results

In order to reproduce the data you need to copy `example_config.yml` to `config.yml` and insert your Altmetric key.

**1. Collect PubMed data**

```Rscript a.R```

**2. Collect altmetrics from Altmetric.com**

```python 02_collect_altmetrics.py```

**3. Create dummy variables and export data**

```python 03_export_data.py```
