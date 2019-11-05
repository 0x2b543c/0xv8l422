from .TransformerABC import Transformer as tabc
import pandas as pd

class PercentChangeExchangeFlows(tabc):
    def __init__(self, asset:str, exchange:str):
        self.asset = asset
        self.exchange = exchange

    def implement_transformation(self, df):
        net_flows_change_column = self.asset + '.' + self.exchange + 'NetFlowNtvPercentChange'
        
        shifted_col = df[self.asset + '.' + 'Sply{}Ntv'.format(self.exchange)].shift(1)
        df[net_flows_change_column] = df[self.asset + '.' + self.exchange + 'NetFlowNtv'] / shifted_col

        sply_change_column = self.asset + '.' + 'Sply{}NtvPercentChange'.format(self.exchange)

        df[sply_change_column] = df[self.asset + '.' + 'Sply{}Ntv'.format(self.exchange)].pct_change(1)



        return df