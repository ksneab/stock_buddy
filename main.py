import os
from pprint import pprint
import numpy as np
import torch
from sklearn.preprocessing import MinMaxScaler

from model_code import experiments, models
from results_creation.plots import plot_stock_data
from stock_data import processor as stock_processor
from stock_data.portal import download_stock_data
from web_scraping import scraper
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')

##################### Command line params?
API_URL = "https://www.alphavantage.co/query"

data = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "AMD",
    "outputsize": "full",
    "datatype": "json",
    "apikey": "***",
    }

download_flag = True

search_sites =[
    # "Motley Fool",
    "Atom Finance",
    "Zacks Investment Research",
    "Stock Rover",
    "Morningstar",
    "TIM'S ALERTS",
    # "Trade Ideas",
    "Seeking Alpha",
    # "Yahoo! Finance",
    "The Wall Street Journal",
    # "Google Finance",
    "cnbc",
    "benzinga",
    "MarketWatch",
    "Reuters",
    "Barron's",
]
#######################

def main():
    # Get arguments from command line
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--api-key', type=str, help='Api key used to access alphavantage API')
    parser.add_argument('--ticker', type=str, help='Ticker that you wish to gather data on')
    parser.add_argument('--download-flag', dest='download_flag', action='store_true')
    args = parser.parse_args()
    data['apikey'] = args.api_key
    data['symbol'] = args.ticker
    download_flag = args.download_flag
    # Get data from internet
    
    if download_flag:
        if not os.path.exists(os.path.join('dataset_info', data['symbol'])):
            os.makedirs(os.path.join('dataset_info', data['symbol']))
            download_stock_data(API_URL, data) 
            stock_processor.split_train_val(os.path.join('dataset_info', data['symbol'], data['function'] + '_' + data['symbol'] + '_full' +'.json'), data['symbol'])
        else:
            print('Warning: Stock data already exists for', data['symbol'] ,'stock ticker.', 'Skipping stock price download...')
    scaler = MinMaxScaler(feature_range=(-1, 1))

    # Create train data
    np_hp_arry_train, train_dates = stock_processor.convert_to_readable_data(os.path.join('dataset_info', data['symbol'], data['symbol'] + '_train.json'))

    # Create stock news data train dates
    if not os.path.exists('output/searches/train'):
        os.makedirs('output/searches/train')
        scraper.create_stock_news_data(data['symbol'], 'output/searches/train', search_sites, train_dates)
    else:
        print('Warning: Data already exists at output/searches/train skipping stock news creation for training')
    
    train_data_normalized = scaler.fit_transform(np_hp_arry_train.reshape(-1, 1))
    train_data_normalized = torch.FloatTensor(train_data_normalized).view(-1)
    train_window = 185
    train_inout_seq = stock_processor.create_inout_sequences(train_data_normalized, train_window)

    # Create test data
    np_hp_arry_test, test_dates = stock_processor.convert_to_readable_data(os.path.join('dataset_info', data['symbol'], data['symbol'] + '_val.json'))

    # Create stock news data test dates
    if not os.path.exists('output/searches/test'):
        os.makedirs('output/searches/test')
        scraper.create_stock_news_data(data['symbol'], 'output/searches/test', search_sites, test_dates)
    else:
        print('Warning: Data already exists at output/searches/test skipping stock news creation for testing')

    test_data_normalized = scaler.fit_transform(np_hp_arry_test.reshape(-1, 1))
    test_data_normalized = torch.FloatTensor(test_data_normalized).view(-1)
    test_window = 185

    model = models.LSTM()
    loss_function = models.create_loss_object('MSE')
    optimizer = models.create_optimizer(model)

    epochs = 150
    experiments.run_LSTM_training(model, epochs, train_inout_seq, loss_function, optimizer)

    fut_pred = 185

    test_inputs = test_data_normalized.tolist()
    test_inputs = experiments.run_LSTM_eval(model, test_inputs, fut_pred, test_window)

    actual_predictions = scaler.inverse_transform(np.array(test_inputs[-train_window:]).reshape(-1, 1))
    # actual_prices = scaler.inverse_transform(np.array(test_inputs[:-train_window]).reshape(-1, 1))
    plot_stock_data([actual_predictions], [test_dates], 'experiment_results', ['predictions'])

if __name__ == "__main__":
    main()

#CODE USED LATER WHEN IMPLEMENTING LANGUAGE PARSER
    # test_date = '2019-12-31'
    # query_results = do_google_search(data['symbol'] + ' stock news', test_date)

    # google_output_file = os.path.join('dataset_info', data['symbol'], 'google_search' +'.txt')

    # with open(google_output_file, 'w') as outfile:
    #     pprint(query_results, stream=outfile)