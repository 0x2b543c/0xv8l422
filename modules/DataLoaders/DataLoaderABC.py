from abc import ABC, abstractmethod
import pandas as pd
import requests
import json

class DataLoader(ABC):
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
        if 'metricData' not in list(response.keys()):
            print('Network Data API Error', response['error']['description'])
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
            result = pd.concat([result, df], axis=1, sort=True)
        return result  
