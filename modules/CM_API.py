import pandas as pd
import requests
import json
from pandas.io.json import json_normalize

class CM_API():
    def __init__(self):
       self.df = pd.DataFrame()

    def call_coinmetrics_api(self, api_key, url, params):
        headers={'Authorization': api_key}
        result = requests.get(url, headers=headers, params=params)
        result = json.loads(result.content)
        return result

    def convert_coinmetrics_network_data_JSON_to_df(self, response):
        ### Sample response:
        # {'metricData': {'metrics': ['AdrActCnt', 'CapRealUSD', 'TxCnt'], 'series': [{'time': '2017-01-01T00:00:00.000Z', 'values': ['13946.0', '734673672.319139817831833516177060007323674', '38730.0']}, {'time': '2017-01-02T00:00:00.000Z', 'values': ['15232.0', '736035521.072371336253635824094185064179384', '39652.0']},
        ###
        series = response['metricData']['series']
        column_headers = list(series[0].keys())[:-1] + response['metricData']['metrics']
        flattened_series = [list(row.values())[:-1] + row['values'] for row in series]
        df = pd.DataFrame(flattened_series, columns=column_headers)
        return df

    def convert_coinmetrics_market_data_JSON_to_df(self, response):
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
        series_key = list(response.keys())[0]
        series = response[series_key]
        column_headers = series[0].keys()
        df = pd.DataFrame(series, columns=column_headers)
        return df

    def concat_dataframes(self, dfs:list):
        result = pd.DataFrame()
        for df in dfs:
            result = pd.concat([result, df], axis=1)
        return result    

    def get_coinmetrics_network_data(self, api_key:str, assets:[str], metrics:str, start:str=None, end:str=None):
        result = pd.DataFrame()
        for asset in assets:
            url = 'https://api.coinmetrics.io/v3/assets/{}/metricdata'.format(asset)
            params = {
                'metrics': metrics,
                'start': start,
                'end': end
            }      
            response = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
            df = self.convert_coinmetrics_network_data_JSON_to_df(response)
            df.set_index('time', inplace=True)
            df.columns = [asset + '.' + column for column in list(df.columns)]
            result = self.concat_dataframes(dfs=[result, df])     
        return result

    def get_coinmetrics_trades_data(self, api_key:str, market_id:str, reference_time:str=None, direction:str=None, limit:str=None, latest:bool=None):
        url = 'https://api.coinmetrics.io/v3/markets/{}/trades'.format(market_id)
        params = {
            'reference_time': reference_time,
            'direction': direction,
            'limit': limit,
            'latest': latest
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        df = self.convert_coinmetrics_market_data_JSON_to_df(result)
        return df 

    def get_coinmetrics_candles_data(self, api_key:str, market_id:str, reference_time:str=None, direction:str='forward', limit:int=100, time_aggregation:str='1d', latest:bool=None):
        url = 'https://api.coinmetrics.io/v3/markets/{}/candles'.format(market_id)
        params = {
            'reference_time': reference_time,
            'direction': direction,
            'limit': limit,
            'time_aggregation': time_aggregation,
            'latest': latest
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        df = self.convert_coinmetrics_market_data_JSON_to_df(result) 
        print('CANDLES DF', df)      
        return df 

    def get_coinmetrics_realtime_network_data(self, api_key:str, asset_id:str, metrics:str, reference_time:str=None, reference_height:str=None, direction:str=None, limit:str=None):
        url = 'https://api.coinmetrics.io/v3/assets/{}/realtimemetricdata'.format(asset_id)
        params = {
            'metrics': metrics,
            'reference_time': reference_time,
            'reference_height': reference_height,
            'direction': direction,
            'limit': limit
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        df = self.convert_coinmetrics_network_data_JSON_to_df(result)     
        return df 







