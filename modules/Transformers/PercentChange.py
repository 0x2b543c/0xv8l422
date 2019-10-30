from .TransformerABC import Transformer as tabc
import pandas as pd

class PercentChange(tabc):
    def __init__(self, input_columns:['str']='all', number_of_days:int=1):
        self.input_columns = input_columns
        self.number_of_days = number_of_days

    def implement_transformation(self, df):
        if self.input_columns == 'all':
            result = df.pct_change(self.number_of_days)
        # for column in 
        # df[self.input_column] = pd.to_datetime(df[self.input_column]).dt.strftime('%Y-%m-%d')
        return result