from .TransformerABC import Transformer as tabc
import pandas as pd

class InitialValueExtractor(tabc):
    def __init__(self, new_column_name:str, column:str):
        self.new_column_name = new_column_name
        self.column = column

    def implement_transformation(self, df):
        df[self.new_column_name] = df[self.column].iloc[0]
        return df