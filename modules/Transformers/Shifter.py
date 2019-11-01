from .TransformerABC import Transformer as tabc
import pandas as pd

class Shifter(tabc):
    def __init__(self, column:str, shift_amount:int=1, fill_value:int=0):
        self.column = column
        self.shift_amount = shift_amount
        self.fill_value = fill_value


    def implement_transformation(self, df):
        new_column_name = self.column + 'ShiftedBy' + str(self.shift_amount)
        df[new_column_name] = df[self.column].shift(periods=self.shift_amount, fill_value=self.fill_value)
        return df