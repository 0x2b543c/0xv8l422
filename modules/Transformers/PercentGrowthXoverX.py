from .TransformerABC import Transformer as tabc
import pandas as pd

class PercentGrowthXoverX(tabc):
    def __init__(self, input_column:'str'='all', growth_period:int=7, new_column_name:str=None):
        self.input_column = input_column
        self.growth_period = growth_period
        self.new_column_name = new_column_name
        self.df = None


    # take the rolling sum of the growth period x (e.g. last 7 days)
    # then take the percent change of that number (i.e. the rolling sum) from x days prior
    def implement_transformation(self, df):
        self.df = df
        result = pd.DataFrame()
        if self.input_column == 'all':
            result = df.rolling(self.growth_period).sum().pct_change(periods=self.growth_period)
        else:
            result = df.copy()
            result[self.new_column_name] = df[self.input_column].rolling(self.growth_period).sum().pct_change(periods=self.growth_period)
        return result