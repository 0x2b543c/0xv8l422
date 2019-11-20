from .TransformerABC import Transformer as tabc
import pandas as pd

class PercentGrowthXoverX(tabc):
    def __init__(self, input_column:'str'='all', growth_period:int=7, new_column_name:str=None):
        self.input_column = input_column
        self.growth_period = growth_period
        self.new_column_name = new_column_name
        self.df = None

    def calculateXoverXGrowth(self, val):
        present_values = self.df.iloc[-self.growth_period:].sum()
        past_values = self.df.iloc[-(self.growth_period * 2):-self.growth_period].sum()


    def implement_transformation(self, df):
        self.df = df
        result = pd.DataFrame()
        if self.input_column == 'all':
            result = df.rolling(self.growth_period).sum().pct_change(periods=self.growth_period)
        else:
            result = df.copy()
            result[self.new_column_name] = df[column].rolling(self.growth_period).sum().pct_change(periods=self.growth_period)
        return result