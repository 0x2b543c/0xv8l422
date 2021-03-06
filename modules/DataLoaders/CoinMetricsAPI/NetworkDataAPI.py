import os
import sys
import pandas as pd
import requests
import json
import pdb
from modules.DataLoaders.DataLoaderABC import DataLoader as DataLoader
from modules.Transformers.DateNormalizer import DateNormalizer
from modules.Transformers.CastToFloats import CastToFloats
from modules.Transformers.AggregateColumnsByAssets import AggregateColumnsByAssets
from modules.Transformers.ResearchMetrics import ResearchMetrics
from modules.DataLoaders.CoinMetricsAPI.DiscoveryAPI import DiscoveryAPI
from modules.DataLoaders.CMDataGroups import CMDataGroups

dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '...'))
sys.path.append(dir_path)

class NetworkDataAPI(DataLoader):
    def __init__(self):
        super().__init__()
        self.discovery_api = DiscoveryAPI()
        self.asset_groups = CMDataGroups().asset_groups
        self.research_metrics = ResearchMetrics().research_metrics
        self.research_metric_prerequisites = ResearchMetrics().research_metric_prerequisites
        

    def clean_df(self, df):            
            df = CastToFloats().transform(df)
            df = DateNormalizer().transform(df)
            return df
            
    def get_coinmetrics_network_data(self, api_key:str, assets:[str], metrics:[str], start:str=None, end:str=None, staging:bool=False):
        if len(self.discovery_api.network_data_asset_info.keys()) == 0:
            self.discovery_api.create_network_data_asset_info_map(api_key)
        result = pd.DataFrame()
        _assets = assets
        ### Also keep track of the group-assets
        _asset_groups = []
        ### Check if asset is a custom asset group, e.g. ERC-20s or Stablecoins
        for asset in assets:
            if asset in self.asset_groups.keys():
                ### if it is, add it to our internal list of assets that we'll use to make the CM api call
                _assets = _assets + self.asset_groups[asset]
                _asset_groups.append(asset)
        ### Filter out any duplicates
        _assets = list(set(_assets))
        _metrics = []
        ### Also keep track of the research-metrics
        _research_metrics = []
        ### Check if metrc is a custom research metric, e.g. "ThermoToMarketCap"
        for metric in metrics:
            if metric in self.research_metrics.keys():
                ### if it is, add it to the list of research metrics that we'll compute after making the API call
                _research_metrics.append(metric)
                ### also add the research metric's prerequsite metrics to the list of _metrics to use in the API call
                _metrics = _metrics + self.research_metric_prerequisites[metric]
            else:
                ### if it's not a research metric, add it to the list of metric to use in the API call
                _metrics.append(metric)
        ### Filter out any duplicates
        _metrics = list(set(_metrics))
        for _asset in _assets:
            ### Filter out asset_groups from list of _assets before calling CM api - these asset groups will be added after calling the api
            if _asset in self.discovery_api.network_data_asset_info.keys():
                api_metrics = []
                for _metric in _metrics:
                    ### Check if we have coverage for each metric per each asset (for example, do we have CapRealUSD for each asset?)
                    if _metric in self.discovery_api.network_data_asset_info[_asset]:
                        api_metrics.append(_metric)
                ### Filter out any duplicates
                api_metrics = list(set(api_metrics))
                url_prefix = 'staging-' if staging == True else ''
                url = 'https://{url_prefix}api.coinmetrics.io/v3/assets/{asset}/metricdata'.format(url_prefix=url_prefix, asset=_asset)
                params = {
                    'metrics': ','.join(api_metrics),
                    'start': start,
                    'end': end
                } 
                response = self.call_coinmetrics_api(api_key=api_key, url=url, params=params)
                if 'error' in list(response.keys()):
                    error_message = response['error']['description']
                    print('Network Data API Error: {} for asset: {}'.format(error_message, _asset))
                df = self.convert_coinmetrics_network_data_JSON_to_df(response)
                df.set_index('time', inplace=True)
                df.columns = [_asset + '.' + column for column in list(df.columns)]
                result = self.concat_dataframes(dfs=[result, df]) 
        result = self.clean_df(result)
        ### If there any asset-groups (e.g. Stablecoins, ERC-20s, etc.) aggregate them together and add as columns for each metric (e.g. stablecoins.TxCnt)
        if len(_asset_groups) > 0:
            result = AggregateColumnsByAssets(aggregation_type='sum', asset_group_names=_asset_groups, metrics=metrics).transform(result)
        ### If there any research metrics (e.g. ThermoToMarketCap, etc.) calculate them and add them as columns
        if len(_research_metrics) > 0:
            result = ResearchMetrics(research_metric_names=_research_metrics, assets=assets, network_data_asset_info=self.discovery_api.network_data_asset_info).transform(result)
        return result
