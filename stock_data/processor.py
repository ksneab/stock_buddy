import os
import json
import numpy as np
import datetime

def split_train_val(full_json_path, ticker):
    val = {}
    train = {}
    with open(full_json_path, 'r') as infile:
        full_data = json.load(infile)
    for daily_log in full_data["Time Series (Daily)"].keys():
        if '2020' in daily_log:
            val[daily_log] = full_data["Time Series (Daily)"][daily_log]
        else:
            train[daily_log] = full_data["Time Series (Daily)"][daily_log]

    top_dir = os.path.dirname(full_json_path)
    val_dir = os.path.join(top_dir, ticker + '_val.json')
    train_dir = os.path.join(top_dir, ticker + '_train.json')

    with open(val_dir, 'w') as outfile:
        json.dump(val, outfile)
    with open(train_dir, 'w') as outfile:
        json.dump(train, outfile)

def convert_to_readable_data(json_path):
    with open(json_path, 'r') as infile:
        data = json.load(infile)
    high_price_arr = []
    dates = []
    for key in data.keys():
        high_price_arr.append(float(data[key]['2. high']))
        dates.append(key)

    np_hp_arry = np.array(high_price_arr)
    return np_hp_arry, dates

def create_inout_sequences(input_data, tw):
    inout_seq = []
    L = len(input_data)
    print('Creating inout sequences...')
    for i in range(L-tw):
        train_seq = input_data[i:i+tw]
        train_label = input_data[i+tw:i+tw+1]
        inout_seq.append((train_seq ,train_label))
    return inout_seq