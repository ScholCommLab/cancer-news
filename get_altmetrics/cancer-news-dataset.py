
# coding: utf-8

# In[2]:


import datetime, time, os, sys, re
import json
from pprint import pprint
from time import sleep
import pandas as pd

from ATB.Altmetric import Altmetric
from ATB.Facebook import Facebook
from ATB.DBConnection import DBConnection
from ATB.CrossRef import resolve_doi

import argparse, configparser
Config = configparser.ConfigParser()
Config.read('config.cnf')

# Load config
FACEBOOK_APP_ID = Config.get('facebook', 'app_id')
FACEBOOK_APP_SECRET = Config.get('facebook', 'app_secret')
ALTMETRIC_KEY = Config.get('altmetric', 'key')


# In[3]:


db_table = "pubmed"
db_unique = "pmid"
db_path = '../data/altmetrics/pubmed.db'
db_cols = "pmid TEXT, am_response TEXT, timestamp TEXT"

db_con = DBConnection(db_path=db_path, table=db_table, db_columns=db_cols, unique=db_unique)


# In[4]:


altmetric = Altmetric(api_key = ALTMETRIC_KEY)


# In[5]:


df = pd.read_csv("../data/output/2016_cancer_data.csv", encoding = 'utf8')
ids = df.pmid


# In[6]:


def parse_response(pmid, timestamp, altmetric_response, altmetric_error = None):
    try:
        am_posts_count = altmetric_response['counts']['facebook']['posts_count']
    except:
        am_posts_count = None

    row = (pmid, json.dumps(altmetric_response), str(timestamp))
    
    return row


# In[7]:


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


# In[8]:


input_list = list(map(str,ids))
i_max = len(input_list)
for i, pmid in enumerate(input_list, 1):
    now = datetime.datetime.now()
        
    try:
        am_response = altmetric.pmid(pmid, fetch=True)
    except:
        am_response = None

    row = parse_response(pmid, now, am_response)
    db_con.save_row(row)
    new = datetime.datetime.now()
    delta = new - now
    m, s = divmod(i_max-i, 60)
    h, m = divmod(m, 60)
    if delta.seconds < 1:
        time.sleep(1 - delta.total_seconds())
    
    printProgressBar(i, i_max, length=80, suffix="ETA {:d}:{:d}:{:d}".format(h, m, s))  

