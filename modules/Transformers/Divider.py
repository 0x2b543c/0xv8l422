from .TransformerABC import Transformer as tabc
import pandas as pd

class Divider(tabc):
    def __init__(self, column_a:str, column_b:str, new_column_name:str=None):
        self.new_column_name = column_a + '/' + column_b if new_column_name == None else new_column_name
        self.column_a = column_a
        self.column_b = column_b

    def implement_transformation(self, df):
        new_column = df[self.column_a] / df[self.column_b]
        df[self.new_column_name] = new_column
        return df