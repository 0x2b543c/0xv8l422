import pandas as pd
import requests
import json
import pdb
from .DataLoaderABC import DataLoader as DataLoader
from ..Transformers.DateNormalizer import DateNormalizer
from ..Transformers.CastToFloats import CastToFloats

class CM_API(DataLoader):
    def __init__(self):
        super().__init__()

    def clean_df(self, df):            
            df = CastToFloats().transform(df)
            df = DateNormalizer().transform(df)
            return df
            
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