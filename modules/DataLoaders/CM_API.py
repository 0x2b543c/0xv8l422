import pandas as pd
import requests
import json
from pandas.io.json import json_normalize
from .DataLoaderABC import DataLoader as DataLoader

class CM_API(DataLoader):
    def __init__(self):
        super().__init__()

    def get_coinmetrics_network_data(self, api_key:str, assets:[str], metrics:[str], start:str=None, end:str=None, staging:bool=False):
        result = pd.DataFrame()
        for asset in assets:
            url_prefix = 'staging-' if staging == True else ''
            url = 'https://{url_prefix}api.coinmetrics.io/v3/assets/{asset}/metricdata'.format(url_prefix=url_prefix, asset=asset)
            params = {
                'metrics': ','.join(metrics),
                'start': start,
                'end': end
            }      
            response = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
            if 'error' in list(response.keys()):
                error_message = response['error']['description']
                print('Network Data API Error: {} for asset: {}'.format(error_message, asset))
            df = self.convert_coinmetrics_network_data_JSON_to_df(response)
            df.set_index('time', inplace=True)
            df.columns = [asset + '.' + column for column in list(df.columns)]
            result = self.concat_dataframes(dfs=[result, df])     
        return result

    def get_coinmetrics_aggregated_candles_data(self, api_key:str, assets:[str], currency:str='usd', start:str=None, end:str=None, limit:int=100, time_aggregation:str='1d', staging:bool=False):
        result = pd.DataFrame()
        for asset in assets:
            url = 'https://api.coinmetrics.io/v3/assets/{}/candles'.format(asset)
            params = {
                'currency': currency,
                'start': start,
                'end': end,
                'limit': limit,
                'time_aggregation': time_aggregation
            }      
            res = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
            print(res)
            df = self.convert_coinmetrics_market_data_JSON_to_df(res)
            result = pd.concat([result, self.df], axis=1, sort=True)    
        return result 


    def get_coinmetrics_candles_data(self, api_key:str, assets=[str], market_id:str=None, reference_time:str=None, direction:str='forward', limit:int=100, time_aggregation:str='1d', latest:bool=None):
        # TODO: 
        # - for asset in assets
        # - call discovery endpoint to get all markets
        # - and filter by usd + stablecoin spot markets
        # - get data 
        # - map column names to asset.market.candles
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
        df = self.convert_coinmetrics_market_data_JSON_to_df(result)
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

    def get_coinmetrics_discovery_assets(self, api_key:str):
        url = 'https://api.coinmetrics.io/v3/assets/'
        params = {
     
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        return result 

    def get_coinmetrics_discovery_asset_info(self, api_key:str):
        url = 'https://api.coinmetrics.io/v3/asset_info/'
        params = {
     
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        return result 

    def get_coinmetrics_discovery_market(self, api_key:str):
        url = 'https://api.coinmetrics.io/v3/markets/'
        params = {
     
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        return result 

    def get_coinmetrics_discovery_market_info(self, api_key:str):
        url = 'https://api.coinmetrics.io/v3/market_info/'
        params = {
     
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        return result 

    def get_coinmetrics_discovery_exchanges(self, api_key:str):
        url = 'https://api.coinmetrics.io/v3/exchanges/'
        params = {
     
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        return result 

    def get_coinmetrics_discovery_exchange_info(self, api_key:str):
        url = 'https://api.coinmetrics.io/v3/exchange_info/'
        params = {
     
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        return result

    def get_coinmetrics_discovery_metrics(self, api_key:str):
        url = 'https://api.coinmetrics.io/v3/metrics/'
        params = {
     
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        return result

    def get_coinmetrics_discovery_metrics_info(self, api_key:str):
        url = 'https://api.coinmetrics.io/v3/metric-info/'
        params = {
     
        }      
        result = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
        return result






