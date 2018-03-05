import datetime, os
import json
import yaml
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from ATB.ATB.Altmetric import Altmetric

with open('../config.yml', 'r') as f:
    config = yaml.load(f)
    
data_folder = Path("../data/") / config['general']['project']

ALTMETRIC_KEY = config['altmetric']['key']
altmetric = Altmetric(api_key = ALTMETRIC_KEY)

df = pd.read_json(data_folder / "cancer_data.json")
out = pd.DataFrame(index=df.pmid, columns=["am_resp", "am_err", "ts"])

for pmid in tqdm(out.index.tolist()):
    now = datetime.datetime.now()
        
    try:
        am_resp = altmetric.pmid(str(pmid), fetch=True)
        am_err = None
    except Exception as e:
        am_resp = None
        am_err = e
    
    out.loc[pmid, 'am_resp'] = json.dumps(am_resp)
    out.loc[pmid, 'am_err'] = str(am_err)
    out.loc[pmid, 'ts'] = str(now)
    
out.to_csv(data_folder / "altmetrics.csv")