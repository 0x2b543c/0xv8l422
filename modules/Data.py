import pandas as pd
import requests
import json
from pandas.io.json import json_normalize

class Data():
    def __init__(self):
       self.df = pd.DataFrame()

    def call_coinmetrics_api(self, api_key, url, params):
        headers={'Authorization': api_key}
        result = requests.get(url, headers=headers, params=params)
        result = json.loads(result.content)
        return result


    def get_coinmetrics_network_data(self, api_key:str, asset:str, metrics:str, start:str=None, end:str=None):
        url = 'https://api.coinmetrics.io/v3/assets/{}/metricdata'.format(asset)
        params = {
            'metrics': metrics,
            'start': start,
            'end': end
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        df = self.convert_coinmetrics_network_data_JSON_to_df(result)     
        print('RESULT', df)
        return df

    def convert_coinmetrics_network_data_JSON_to_df(self, response):
        ### Sample response:
        # {'metricData': {'metrics': ['AdrActCnt', 'CapRealUSD', 'TxCnt'], 'series': [{'time': '2017-01-01T00:00:00.000Z', 'values': ['13946.0', '734673672.319139817831833516177060007323674', '38730.0']}, {'time': '2017-01-02T00:00:00.000Z', 'values': ['15232.0', '736035521.072371336253635824094185064179384', '39652.0']},
        ###
        print('CCC', response)
        column_headers = ['time'] + response['metricData']['metrics']
        series = response['metricData']['series']
        flattened_series = [[row['time']] + row['values'] for row in series]
        df = pd.DataFrame(flattened_series, columns=column_headers)
        print('DF:', df)
        return df

    def get_coinmetrics_trades_data(self, api_key:str, market_id:str, reference_time:str=None, direction:str=None, limit:str=None, latest:bool=None):
        url = 'https://api.coinmetrics.io/v3/markets/{}/trades'.format(market_id)
        params = {
            'reference_time': reference_time,
            'direction': direction,
            'limit': limit,
            'latest': latest
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        df = self.convert_coinmetrics_trades_data_JSON_to_df(result)     
        print('RESULT', result)
        return df 

    def convert_coinmetrics_trades_data_JSON_to_df(self, response):
        ### Sample response:
        # {
        #     "tradesData": [
        #         {
        #             "time": "2019-01-01T00:00:03.247000Z",
        #             "timeMicros": 1546300803247000,
        #             "coinMetricsId": "57003012",
        #             "marketId": "coinbase-btc-usd-spot",
        #             "amount": "0.00215325",
        #             "price": "3691.87",
        #             "side": "buy"
        #         } ...,
        #     ]
        # }
        ###
        print('CCC', response)
        column_headers = response['tradesData'][0].keys()
        data = response['tradesData']
        df = pd.DataFrame(data, columns=column_headers)
        print('DF:', df)
        return df


