import json, re, os
import yaml
import pandas as pd
import numpy as np

from dateutil.parser import parse
from pathlib import Path
from tqdm import tqdm

mesh_top13 = ["Urinary Bladder Neoplasms",
              "Breast Neoplasms",
              "Colorectal Neoplasms",
              "Endometrial Neoplasms",
              "Kidney Neoplasms",
              "Leukemia",
              "Liver Neoplasms",
              "Lung Neoplasms",
              "Melanoma",
              "Lymphoma, Non-Hodgkin",
              "Pancreatic Neoplasms",
              "Prostatic Neoplasms",
              "Thyroid Neoplasms"]

mesh_qual = ["diagnosis",
             "diagnostic imaging",
             "mortality",
             "therapy",
             "diet therapy",
             "drug therapy",
             "nursing",
             "prevention & control",
             "radiotherapy",
             "rehabilitation",
             "surgery",
             "transplantation"]

funding_types = ["Research Support, American Recovery and Reinvestment Act",
                 "Research Support, N.I.H., Extramural",
                 "Research Support, N.I.H., Intramural",
                 "Research Support, Non-U.S. Gov't",
                 "Research Support, U.S. Gov't, Non-P.H.S.",
                 "Research Support, U.S. Gov't, P.H.S.",
                 "Research Support, U.S. Government"]

us_gov_funding = ["Research Support, American Recovery and Reinvestment Act",
                 "Research Support, N.I.H., Extramural",
                 "Research Support, N.I.H., Intramural",
                 "Research Support, U.S. Gov't, Non-P.H.S.",
                 "Research Support, U.S. Gov't, P.H.S.",
                 "Research Support, U.S. Government"]

add_cols = ['news_mention', 'news_count', 'tier1', 'tier2', 'tier3', 'tier4']

def load_pubmed(path):
    df = pd.read_json(path)
    df = df.set_index("pmid")
    df = df.replace("", np.nan)
    df['mesh_terms'] = df['mesh_terms'].map(lambda x: json.loads(x) if pd.notnull(x) else x)
    return df

# read in data
def load_altmetrics(path):
    df = pd.read_csv(path)
    df = df.set_index('pmid')
    df = df.replace(to_replace=['null', "None"], value=np.nan)
    df['am_resp'] = df['am_resp'].map(lambda x: json.loads(x) if pd.notnull(x) else np.nan)
    return df

def load_news_tiers(path):
    return pd.read_csv(path, index_col="altmetric_id")

def load_mesh(path):
    with open(str(path), mode='r') as file:
        mesh = file.readlines()
    return mesh

def create_mesh_hierarchy(mesh, mesh_terms, mesh_subterms):
    terms = {}
    numbers = {}

    for line in mesh:
        meshTerm = re.search('MH = (.+)$', line)
        if meshTerm:
            term = meshTerm.group(1)
        meshNumber = re.search('MN = (.+)$', line)
        if meshNumber:
            number = meshNumber.group(1)
            if number == None:
                print("yes")
            numbers[number] = term
            if term in terms:
                terms[term] = terms[term] + ' ' + number
            else:
                terms[term] = number
            
    # only use disease mesh terms
    c_keys = [key for key in sorted(list(numbers.keys())) if key[0] == "C"]

    # Create list of relevant meshterms for top 13 terms
    lookups = {}
    for t in mesh_terms:
        x = []
        for subnr in str.split(terms[t], " "):
            x.extend([numbers[key] for key in c_keys if subnr in key])
        lookups[t] = set(x)
    
    return lookups

def create_dummies(pubmed, altmetrics):
    out = pubmed[['doi','title','pub_year', 'mesh_terms', 'pub_types']]
    out = pd.concat([out,
                     altmetrics['am_resp'],
                     pd.DataFrame(np.zeros((len(out), len(mesh_top13)), dtype=bool), index=out.index, columns=mesh_top13, dtype=bool),
                     pd.DataFrame(np.zeros((len(out), len(mesh_qual)), dtype=bool), index=out.index, columns=mesh_qual, dtype=bool),
                     pd.DataFrame(np.zeros((len(out), len(funding_types)), dtype=bool), index=out.index, columns=funding_types, dtype=bool),
                     pd.DataFrame(np.zeros((len(out), len(add_cols))), index=out.index, columns=add_cols)
                    ],
                    axis=1, join_axes=[out.index])

    for row in tqdm(out.itertuples(), total=len(out), desc="Creating Dummy Variables"):
        # create dummies for mesh terms
        if pd.notnull(row.mesh_terms):
            for mt,mqs in row.mesh_terms.items():
                for topterm, subterms in mesh_term_lookups.items():
                    if mt in subterms:
                        out.loc[row.Index, topterm] = True
                    for mq in mqs:
                        if mq in mesh_qual:
                            out.loc[row.Index, mq] = True

        # create dummies for funding type
        if row.pub_types:
            for funding in funding_types:
                if funding in row.pub_types:
                    out.loc[row.Index, funding] = True

        # count news mentions
        try:
            out.loc[row.Index, 'news_count'] = row['am_resp']['counts']['news']['posts_count']
            out.loc[row.Index, 'news_mention'] = True

            res = [tiers.loc[i].tiers for i in row['am_resp']['counts']['news']['unique_users']]
            out.loc[row.Index, 'tier1'] = res.count("tier1")
            out.loc[row.Index, 'tier2'] = res.count("tier2")
            out.loc[row.Index, 'tier3'] = res.count("tier3")
            out.loc[row.Index, 'tier4'] = res.count("tier4")
        except:
            None

    # convert bool to float columns
    out['us_gov_funding'] = out[us_gov_funding].apply(lambda x: x.any(), axis=1).astype(float)
    out[mesh_qual+mesh_top13+funding_types+add_cols] = out[mesh_qual+mesh_top13+funding_types+add_cols].astype(float)
    
    return out

def create_news_details(altmetric):
    pmids = []
    news_mentions = []

    for pmid, row in altmetric[altmetric['am_resp'].notnull()].iterrows():
        try:
            news_mentions.append(row['am_resp']['posts']['news'])
            pmids.append(pmid)
        except:
            pass
        
    article_pmids = []
    venue_name = []
    venue_url = []
    date = []
    summary = []
    title = []
    url = []
    tier = []

    for pmid, nms in zip(tqdm(pmids, total=len(pmids), desc="Creating News Details"), news_mentions):
        for nm in nms:
            article_pmids.append(pmid)
            venue_name.append(nm['author']['name'])
            venue_url.append(nm['author']['url'])
            date.append(str(parse(nm['posted_on'])))
            try:
                tier.append(int(tiers[tiers.title == nm['author']['name']]['tiers'][0][4]))
            except:
                tier.append(None)
            try:
                summary.append(nm['summary'])
            except:
                summary.append(None)
            try:
                title.append(nm['title'])
            except:
                title.append(None)
            url.append(nm['url'])

    return pd.DataFrame({
        'pmid': article_pmids,
        'venue_name': venue_name,
        'venue_url': venue_url,
        'date': date,
        'summary': summary,
        'title': title,
        'url': url,
        'tier': tier
    })

def write_results(path, dummies, news_details):
    dummies[['doi', 'pub_year', 'title']].to_csv(path / "articles_metadata.csv")
    dummies[add_cols].to_csv(path / "articles_news_coverage.csv")
    dummies[mesh_top13].to_csv(path / "articles_mesh_term_dummies.csv")
    dummies[mesh_qual].to_csv(path / "articles_mesh_subterm_dummies.csv")
    dummies[funding_types + ['us_gov_funding']].to_csv(path / "articles_funding_dummies.csv")
    news_details.to_csv(path / "news_mentions_details.csv", index=False)

if __name__ == "__main__":
    
    print("Loading config")
    with open('../config.yml', 'r') as f:
        config = yaml.load(f)

    input_folder = Path("../input/")
    data_folder = Path("../data/") / config['general']['project']
    output_folder = data_folder / "output/"

    if not os.path.exists(str(output_folder)):
        os.makedirs(str(output_folder))


    # Load input files
    print("Loading input files")
    pubmed = load_pubmed(data_folder / "cancer_data.json")
    altmetrics = load_altmetrics(data_folder / "altmetrics.csv")
    tiers = load_news_tiers(input_folder / "news_outlets.csv")
    mesh = load_mesh(input_folder / "mesh_2018/d2018.bin")

    print("Processing")
    # Create dummies
    mesh_term_lookups = create_mesh_hierarchy(mesh, mesh_top13, mesh_qual)
    dummies = create_dummies(pubmed, altmetrics)

    # Create News Coverage
    news_details = create_news_details(altmetrics)
    
    print("Write output")
    # Write outputs
    write_results(output_folder, dummies, news_details)

