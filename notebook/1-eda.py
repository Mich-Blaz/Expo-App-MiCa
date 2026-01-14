# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %%
import pandas as pd 
import os 
from pathlib import Path
from datetime import datetime, timedelta
import requests
import urllib3
import sys 

sys.path.append(Path('.').absolute().parent.as_posix())

from dotenv import load_dotenv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ['HTTP_PROXY'] = "http://127.0.0.1:9000/localproxy-e60003fe.pac"
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:9000/localproxy-e60003fe.pac"
os.environ['HTTP_PROXY'.lower()] = "http://127.0.0.1:9000/localproxy-e60003fe.pac"
os.environ['HTTPS_PROXY'.lower()] = "http://127.0.0.1:9000/localproxy-e60003fe.pac"

# %%

# %%
load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']

# %%
print('hel')

# %%
from database.config import get_config
from expo_app_mica.apicaller import  build_params,calltheapi,get_multiple_pages
conf = get_config()

# %%
old_date = (datetime.now()-timedelta(weeks=10000)).isoformat()
params = build_params(limit=None,date_upload=old_date,cols=conf.columns_api)
params

# %%
res = get_multiple_pages(conf.url_api,params)

# %%
df = pd.DataFrame(res)

# %%
df.title_event
  

# %%
df.isna().sum()

# %%
['locations', 'address_name', 'address_street',
       'address_zipcode', 'address_city', 'lat_lon', 'access_link',
       'access_link_text',  'address_url', 'address_url_text',
       'address_text']

# %%
df.sample()

# %%
df.lat_lon.isna().sum()

# %%
filterrr = df[df.address_name.isna()].locations.dropna().apply(lambda x : len(x))==2

# %%
df[df.address_name.isna()].locations.dropna()[filterrr].iloc[2]

# %%
df[df.address_name.isna()].locations.dropna()[filterrr].iloc[0]

# %%
df.locations.iloc[6]

# %%
df.columns
