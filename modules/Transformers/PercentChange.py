from .TransformerABC import Transformer as tabc
import pandas as pd

class PercentChange(tabc):
    def __init__(self, input_columns:['str']='all', number_of_days:int=1):
        self.input_columns = input_columns
        self.number_of_days = number_of_days

    def implement_transformation(self, df):
        if self.input_columns == 'all':
            result = df.pct_change(self.number_of_days)
        for column in self.input_columns:
            df[column] = df[column].pct_change(self.number_of_days)
        return result