from .TransformerABC import Transformer as tabc
import pandas as pd
import pdb

from enum import Enum
class MetricName(Enum):
    THERMOTOMARKETCAP = 'ThermoToMarketCap'

class ResearchMetrics(tabc):
    def __init__(self, metric_name:MetricName, assets:[str], metrics:[str], network_data_asset_info:dict):
        self.metric_name = metric_name
        self.assets = assets
        self.metrics = metrics
        self.network_data_asset_info = network_data_asset_info
        self.research_metrics = {
            'ThermoToMarketCap': self.thermo_to_market_cap
        }
        self.metric_prerequisites = {
            'ThermoToMarketCap': ['RevAllTimeUSD', 'CapMrktCurUSD']
        }

    def thermo_to_market_cap(self, df, asset):
        new_column_name = f'{asset}.ThermoToMarketCap'
        df[new_column_name] = df[f'{asset}.RevAllTimeUSD'] / df[f'{asset}.CapMrktCurUSD']
        return df

    def check_prerequisities(self, asset):
        prereqs = self.metric_prerequisites[self.metric_name]
        prereqs_flag = True
        for prereq in prereqs:
            if prereqs_flag == False:
                break
            if prereq in self.network_data_asset_info[asset]:
                prereqs_flag = True
            else:
                prereqs_flag = False
        return prereqs_flag

    def implement_transformation(self, df):
        for asset in assets:
            if self.check_prerequisities(asset) == True:
                df = self.research_metrics[self.metric_name](df)
        return df