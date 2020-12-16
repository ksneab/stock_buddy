import os
import requests
import json

def download_stock_data(url, query_settings):

    req = requests.get(url, query_settings)
    json_obj = req.json()
    if not os.path.isdir(os.path.join('dataset_info', query_settings['symbol'])):
        os.makedirs(os.path.join('dataset_info', query_settings['symbol']))

    with open(os.path.join('dataset_info', query_settings['symbol'], query_settings['function'] + '_'+ query_settings['symbol'] + '_full' +'.json'), 'w') as outfile:
        json.dump(json_obj, outfile)

