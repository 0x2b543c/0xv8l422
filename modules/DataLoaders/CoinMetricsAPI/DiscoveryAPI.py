import os
import sys
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '...'))
sys.path.append(dir_path)

import pdb
from modules.DataLoaders.DataLoaderABC import DataLoader as DataLoader

class DiscoveryAPI(DataLoader):
    def __init__(self):
        super().__init__()

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
