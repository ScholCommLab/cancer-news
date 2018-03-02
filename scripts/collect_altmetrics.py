import datetime, time, os, sys, re
import json
from pprint import pprint
from time import sleep
import pandas as pd
from tqdm import tqdm

from ATB.ATB.Altmetric import Altmetric

import argparse, configparser
Config = configparser.ConfigParser()
Config.read('config.cnf')

# Load config
ALTMETRIC_KEY = Config.get('altmetric', 'key')
altmetric = Altmetric(api_key = ALTMETRIC_KEY)

df = pd.read_csv("../pmid_ids.csv")
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
    
out.to_csv("altmetrics.csv")