from .TransformerABC import Transformer as tabc
import pandas as pd
import pdb

class DatePicker(tabc):
    def __init__(self, start:str=None, end:str=None):
        self.start = start
        self.end = end

    def implement_transformation(self, df):
        # pdb.set_trace()
        df_slice = df.loc[self.start:self.end,:]
        return df_slice