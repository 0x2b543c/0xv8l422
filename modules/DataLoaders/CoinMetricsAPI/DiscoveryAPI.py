import os
import sys
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '...'))
sys.path.append(dir_path)

import pdb
from modules.DataLoaders.DataLoaderABC import DataLoader as DataLoader

class DiscoveryAPI(DataLoader):
    def __init__(self):
        super().__init__()
        self.network_data_asset_info = {}

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

    def create_network_data_asset_info_map(self, api_key):
        asset_info = self.get_coinmetrics_discovery_asset_info(api_key=api_key)
        asset_info = asset_info['assetsInfo']
        for asset in asset_info:
            asset_id = asset['id']
            asset_metrics = asset['metrics']
            self.network_data_asset_info[asset_id] = asset_metrics
    
    def filter_metrics_available_by_asset(self, asset:str, metrics:[str]):
        if len(self.network_data_asset_info.keys()) == 0:
            self.create_network_data_asset_info_map()
        _metrics = []
        for metric in metrics:
            if metric in self.network_data_asset_info[asset]:
                _metrics.append(metric)
        return _metrics
