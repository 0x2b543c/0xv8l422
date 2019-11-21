from .TransformerABC import Transformer as tabc
import pandas as pd

class PercentChange(tabc):
    def __init__(self, input_columns:['str']='all', number_of_days:int=1):
        self.input_columns = input_columns
        self.number_of_days = number_of_days

    def implement_transformation(self, df):
        if self.input_columns == 'all':
            result = df.copy()
            result = result.pct_change(self.number_of_days)
            result.columns = [str(column) + '.' + str(self.number_of_days) + 'dGrowth' for column in list(result.columns)]
        else:
            result = df.copy()
            for column in self.input_columns:
                result[column] = result[column].pct_change(self.number_of_days)
                new_column_name = str(column) + '.' + str(self.number_of_days) + 'dGrowth'
                result.rename(columns={column: new_column_name}, inplace=True)
        return result