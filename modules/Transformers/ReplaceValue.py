from .TransformerABC import Transformer as tabc
import pandas as pd

class ReplaceValue(tabc):
    def __init__(self, new_column_name:str, column:str, value_index:int=0, new_value:int=0):
        self.new_column_name = new_column_name
        self.column = column
        self.value_index = value_index
        self.new_value = new_value


    def implement_transformation(self, df):
        df[self.new_column_name] = df[self.column]
        df[self.new_column_name].iloc[self.value_index] = self.new_value
        return df