from .TransformerABC import Transformer as tabc
import pandas as pd

class NetCalculator(tabc):
    def __init__(self, new_column_name:str, positive_column:str, negative_column:str):
        self.new_column_name = new_column_name
        self.positive_column = positive_column
        self.negative_column = negative_column

    def implement_transformation(self, df):
        new_column = df[self.positive_column] - df[self.negative_column]
        df[self.new_column_name] = new_column
        return df