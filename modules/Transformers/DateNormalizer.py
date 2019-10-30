from .TransformerABC import Transformer as tabc
import pandas as pd

class DateNormalizer(tabc):
    def __init__(self, input_column:str='time'):
        self.input_column = input_column

    def implement_transformation(self, df):
        df[self.input_column] = pd.to_datetime(df[self.input_column]).dt.strftime('%Y-%m-%d')
        df.set_index(self.input_column, inplace=True)
        return df