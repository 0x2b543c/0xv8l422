from .TransformerABC import Transformer as tabc
import pandas as pd

class Subtractor(tabc):
    def __init__(self, new_column_name:str, column_a:str, column_b:str, ):
        self.new_column_name = new_column_name
        self.column_a = column_a
        self.column_b = column_b

    def implement_transformation(self, df):
        new_column = df[self.column_a] - df[self.column_b]
        df[self.new_column_name] = new_column
        return df