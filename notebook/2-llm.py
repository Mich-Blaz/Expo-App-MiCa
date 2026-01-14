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
load_dotenv()
SecretKey = os.environ['Secretkey_mai']
SecretKey

# %% [markdown]
# ## avec requests

# %%
import requests
url = "https://api.mammouth.ai/v1/chat/completions"
url_models = "https://api.mammouth.ai/v1/models"
headers = {
    "Authorization": f"Bearer {SecretKey}",
    "Content-Type": "application/json"
}

model_choice = 'mistral-small-3.2-24b-instruct'
data = {
    "model": model_choice,
    "max_tokens":20,
    "messages": [
        {
            "role": "user",
            "content": "Explique les bases de l'apprentissage automatique"
        }
    ]
}

# %%

# %%
response = requests.get(url_models,headers=headers,verify=False)
data = response.json()
data['data'][:]

# %%

response = requests.post(url, headers=headers, json=data,verify=False)
print(response.json())


# %% [markdown]
# ## Avec OpenAI

# %%
import openai 
import httpx

client = httpx.Client(verify=False)
openai.http_client = client
openai.api_base = "https://api.mammouth.ai/v1"
openai.api_key = SecretKey
openai.verify_ssl_certs = False



