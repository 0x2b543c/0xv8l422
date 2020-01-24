from .TransformerABC import Transformer as tabc
import pandas as pd

class DatePicker(tabc):
    def __init__(self, start:str=None, end:str=None, date_window:str=None):
        self.start = start
        self.end = end
        self.date_window = date_window

    def implement_transformation(self, df):
        df_slice = df.loc[self.start:self.end,:]
        return df_slice