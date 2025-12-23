import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def build_params(limit : int = 20 ,offset : int = 0  ,date_upload : str="2025-12-22T20:54:05.476662",cols = ['']):
    cols = ','.join(cols)
    params = {
    'where': f'updated_at >= "{date_upload}"',
    'limit': limit,
    'select': cols,
    "offset":offset}
    return params

def calltheapi(url,params):
    try:
        response = requests.get(url, params=params,verify=False)
        return response
    except Exception as e:
        print(e)
        return None
    
def get_multiple_pages(url :str ,params:dict):
    p_ = params.copy()
    p_['limit'] = 0
    p_["cols"] = ['']
    res_ = calltheapi(url,p_)
    if not res_:
        raise "Error in sql"
    metadata = res_.json()
    try:
        total_count = metadata['total_count']
    except:
        print(f'Result bad for  the query : {metadata}')
    print(total_count)
    all_records = []
    for offset in range(0, total_count, 100):
        p_ = params.copy()
        p_['limit'] = 100
        p_['offset'] = offset
        res_ = calltheapi(url,p_)
        data = res_.json()
        records = data['results']
        all_records.extend(records)
    return all_records


if __name__ == '__main__':
# be aware of https_proxy if you have one
    from pathlib import Path
    from datetime import datetime, timedelta
    import sys 
    import pandas as pd 


    sys.path.append(Path(__file__).absolute().parent.parent.as_posix())

    print(Path(__file__).absolute().parent.parent.as_posix())

    from database.config import get_config

    conf = get_config()
    old_date = (datetime.now()-timedelta(weeks=10000)).isoformat()
    params = build_params(limit=None,date_upload=old_date,cols=conf.columns_api)
    res = get_multiple_pages(conf.url_api,params)
    df = pd.DataFrame(res)
    print(df.head())

    