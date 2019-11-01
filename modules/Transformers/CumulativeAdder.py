from .TransformerABC import Transformer as tabc
import pandas as pd

class CumulativeAdder(tabc):
    def __init__(self, new_column_name:str, column:str):
        self.new_column_name = new_column_name
        self.column = column

    def implement_transformation(self, df):
        new_column = df[self.column].cumsum()
        df[self.new_column_name] = new_column
        return df