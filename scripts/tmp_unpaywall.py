# coding: utf-8
import pandas as pd
import requests
import json
import csv
import yaml

import os.path
from pathlib import Path

with open('../config.yml', 'r') as f:
    config = yaml.load(f)
    
data_folder = Path("../data/") / config['general']['project']


fu = pd.read_csv(data_folder / 'output/articles_funding_dummies.csv')
print(len(fu))
fu['covered_by_NIH_policy'] = fu[[
       "Research Support, N.I.H., Extramural",
       "Research Support, N.I.H., Intramural",
       "Research Support, U.S. Gov't, P.H.S.",
       "Research Support, U.S. Government"]].apply(lambda x: bool(x.any()), axis=1)
print("Number of articles: %s (%.1f%%)" % (fu['covered_by_NIH_policy'].sum(), fu['covered_by_NIH_policy'].sum()*100/len(fu)))

# pni = set(pd.read_csv(data_folder / 'raw/phs_not_nih_2016.csv', header=None)[0])
# print("Removing an additional %s PHS but not NIH" % len(fu[fu.pmid.isin(pni)]))
# fu['covered_by_NIH_policy'] = fu.covered_by_NIH_policy & ~fu.pmid.isin(pni)
# print()
# print("Number of articles left: %s (%.1f%%)" % (fu['covered_by_NIH_policy'].sum(), fu['covered_by_NIH_policy'].sum()*100/len(fu)))

fu = fu[fu.covered_by_NIH_policy]
print(len(fu))

meta = pd.read_csv(data_folder / 'output/articles_metadata.csv')
print(len(meta))

fu = fu.merge(meta)

# fetched from ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/PMC-ids.csv.gz
pmcids = pd.read_csv(data_folder / '../PMC-ids.csv')
pmcids = pmcids[['DOI', 'PMCID', 'PMID']]
pmcids['PMID'] = pmcids.PMID.map(lambda x: int(x) if x > 0 else None)
pmcids['DOI'] = pmcids.DOI.map(lambda x: x.lower() if x==x else None)
pmcids.dropna(subset=['PMID', 'DOI'], how='all', inplace=True)

fu = fu.merge(pmcids[['PMID', 'PMCID']].dropna(subset=['PMID']), left_on='pmid', right_on='PMID', how='left')
fu = fu.merge(pmcids[['DOI', 'PMCID']].dropna(subset=['DOI']), left_on='doi', right_on='DOI', how='left', suffixes=['_pmid', '_doi'])
del fu['DOI']
del fu['PMID']

# grab either one of the two
fu['pmcid'] = fu.apply(lambda row: row['PMCID_pmid'] if row['PMCID_doi'] else row['PMCID_x'], axis=1)

# (1-fu.pmcid.isna().sum()/len(fu))*100

# len(fu.doi.unique())

# Print iterations progress
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


def get_altmetric(doi):
    request_url = "https://api.unpaywall.org/v2/%s" % doi
    params = {'email': 'juan@alperin.ca'}
    response = requests.get(request_url, params=params)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError as ex:
            return str(type(ex))+str(ex.args)
    else:
        return response.status_code

file_path = str(data_folder / 'raw/unpaywall.csv')
error_file_path = str(data_folder / 'raw/unpaywall_errors.csv')
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    already_fetched = set(df.doi)
    del df
else:
    with open(file_path, 'w') as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(['doi', 'unpaywall_json'])
    already_fetched = set()

to_fetch = list(set(fu.doi) - already_fetched)
print("Already fetched: %s" % len(already_fetched))
print("Going after: %s" % len(to_fetch))

for i, doi in enumerate(to_fetch):
    response = get_altmetric(doi)
    if (type(response) == dict):
        with open(file_path, 'a') as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow([doi, json.dumps(response)])
    else:
        with open(error_file_path, 'a') as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow([doi, response])
    printProgressBar(i, len(to_fetch))
            
        
try: 
    errors = pd.read_csv(error_file_path)   
    print("Errors: %s" % len(errors))
except:
    print("No Errors")
