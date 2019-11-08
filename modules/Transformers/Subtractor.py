from .TransformerABC import Transformer as tabc
import pandas as pd

class Subtractor(tabc):
    def __init__(self, starting_column:str, subtractor_columns:[str], new_column_name:str=None):
        self.new_column_name = starting_column + ' - ' + subtractor_columns if new_column_name == None else new_column_name
        self.starting_column = starting_column
        self.subtractor_columns = subtractor_columns

    def implement_transformation(self, df):
        new_column = None
        for i, column in enumerate(self.subtractor_columns):
            if i == 0:
                new_column = df[self.starting_column] - df[column]
            else:
                new_column = new_column - df[column]
        df[self.new_column_name] = new_column
        return df