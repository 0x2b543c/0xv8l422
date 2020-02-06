from .TransformerABC import Transformer as tabc
from ..DataLoaders.CMDataGroups import CMDataGroups
import pandas as pd
import pdb

from enum import Enum
class MetricName(Enum):
    THERMOTOMARKETCAP = 'ThermoToMarketCap'

class ResearchMetrics(tabc):
    def __init__(self, research_metric_names:[MetricName]=None, assets:[str]=None, network_data_asset_info:dict=None):
        self.research_metric_names = research_metric_names
        self.assets = assets
        self.asset_groups = CMDataGroups().asset_groups
        self.network_data_asset_info = network_data_asset_info
        self.research_metrics = {
            'ThermoToMarketCap': self.thermo_to_market_cap,
            'ThermoToRealizedCap': self.thermo_to_realized_cap,
            'CostPerByte': self.cost_per_byte,
            'FeesToMarketCap': self.fees_to_market_cap,
            'TxToTfrCnt': self.transaction_to_transfers,
            'RealizedPrice': self.realized_price
        }
        self.research_metric_prerequisites = {
            'ThermoToMarketCap': ['RevAllTimeUSD', 'CapMrktCurUSD'],
            'ThermoToRealizedCap': ['RevAllTimeUSD', 'CapRealUSD'],
            'CostPerByte': ['BlkSizeByte', 'FeeTotUSD'],
            'FeesToMarketCap': ['FeeTotUSD', 'CapMrktCurUSD'],
            'TxToTfrCnt': ['TxCnt', 'TxTfrCnt'],
            'RealizedPrice': ['CapRealUSD', 'SplyCur'],
            
        }

    def thermo_to_market_cap(self, df, asset):
        new_column_name = f'{asset}.ThermoToMarketCap'
        df[new_column_name] = df[f'{asset}.RevAllTimeUSD'] / df[f'{asset}.CapMrktCurUSD']
        return df

    def thermo_to_realized_cap(self, df, asset):
        new_column_name = f'{asset}.ThermoToRealizedCap'
        df[new_column_name] = df[f'{asset}.RevAllTimeUSD'] / df[f'{asset}.CapRealUSD']
        return df

    def cost_per_byte(self, df, asset):
        new_column_name = f'{asset}.CostPerByte'
        df[new_column_name] = df[f'{asset}.FeeTotUSD'] / df[f'{asset}.BlkSizeByte']
        return df

    def fees_to_market_cap(self, df, asset):
        new_column_name = f'{asset}.FeesToMarketCap'
        df[new_column_name] = df[f'{asset}.FeeTotUSD'] / df[f'{asset}.CapMrktCurUSD']
        return df

    def transaction_to_transfers(self, df, asset):
        new_column_name = f'{asset}.TxToTfrCnt'
        df[new_column_name] = df[f'{asset}.TxCnt'] / df[f'{asset}.TxTfrCnt']
        return df

    def realized_price(self, df, asset):
        new_column_name = f'{asset}.RealizedPrice'
        df[new_column_name] = df[f'{asset}.CapRealUSD'] / df[f'{asset}.SplyCur']
        return df

    def check_prerequisities(self, asset, research_metric):
        
        ### check if asset is an asset group (e.g. tether, stablecoins, etc.)
        ### if it is, add all of its consituent assets (e.g. usdt_omni, usdt_eth, usdt_trx, etc.) to the list of _assets
        _assets = []
        if asset in self.asset_groups.keys():
            _assets = self.asset_groups[asset]
        ### if not, set the asset list as the single asset
        else:
            _assets = [asset]  
        prereqs = self.research_metric_prerequisites[research_metric]
        prereqs_flag = True
        for prereq in prereqs:
            if prereqs_flag == False:
                break
            for _asset in _assets:
                if prereq in self.network_data_asset_info[_asset]:
                    prereqs_flag = True
                else:
                    prereqs_flag = False
        return prereqs_flag

    def implement_transformation(self, df):
        for asset in self.assets:
            for research_metric in self.research_metric_names:
                if self.check_prerequisities(asset, research_metric) == True:
                    df = self.research_metrics[research_metric](df, asset)
        return df