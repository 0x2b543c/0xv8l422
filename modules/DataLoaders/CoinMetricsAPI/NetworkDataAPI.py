import os
import sys
import pandas as pd
import requests
import json
import pdb
from modules.DataLoaders.DataLoaderABC import DataLoader as DataLoader
from modules.Transformers.DateNormalizer import DateNormalizer
from modules.Transformers.CastToFloats import CastToFloats
from modules.DataLoaders.CoinMetricsAPI.DiscoveryAPI import DiscoveryAPI

dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '...'))
sys.path.append(dir_path)

class NetworkDataAPI(DataLoader):
    def __init__(self):
        super().__init__()
        self.network_data_asset_info = {}
        self.discovery_api = DiscoveryAPI()

    def create_network_data_asset_info_map(self, api_key):
        asset_info = self.discovery_api.get_coinmetrics_discovery_asset_info(api_key=api_key)
        asset_info = asset_info['assetsInfo']

        for asset in asset_info:
            asset_id = asset['id']
            asset_metrics = asset['metrics']
            self.network_data_asset_info[asset_id] = asset_metrics


    def clean_df(self, df):            
            df = CastToFloats().transform(df)
            df = DateNormalizer().transform(df)
            return df
            
    def get_coinmetrics_network_data(self, api_key:str, assets:[str], metrics:[str], start:str=None, end:str=None, staging:bool=False):
        if bool(self.network_data_asset_info) == False:
            self.create_network_data_asset_info_map(api_key)
        result = pd.DataFrame()
        for asset in assets:
            _metrics = []
            ### Check if we have coverage for each metric per each asset (for example, do we have CapRealUSD for each asset?)
            for metric in metrics:
                if metric in self.network_data_asset_info[asset]:
                    _metrics.append(metric)
            url_prefix = 'staging-' if staging == True else ''
            url = 'https://{url_prefix}api.coinmetrics.io/v3/assets/{asset}/metricdata'.format(url_prefix=url_prefix, asset=asset)
            params = {
                'metrics': ','.join(_metrics),
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
        result = self.clean_df(result)    
        return result

    def get_coinmetrics_realtime_network_data(self, api_key:str, assets:[str], metrics:[str], reference_time:str=None, reference_height:str=None, direction:str='forward', limit:int=100, staging:bool=False):
        result = pd.DataFrame()
        for asset in assets:
            url_prefix = 'staging-' if staging == True else ''
            url = 'https://{url_prefix}api.coinmetrics.io/v3/assets/{asset}/realtimemetricdata'.format(url_prefix=url_prefix, asset=asset)
            params = {
                'metrics': ','.join(metrics),
                'reference_time': reference_time,
                'reference_height': reference_height,
                'direction': direction,
                'limit': limit
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