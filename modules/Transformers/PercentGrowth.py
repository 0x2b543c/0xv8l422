from .TransformerABC import Transformer as tabc
import pandas as pd

class PercentGrowth(tabc):
    def __init__(self, growth_period:int=0, input_columns:['str']='all'):
        self.input_columns = input_columns

    def implement_transformation(self, df):
        if self.input_columns == 'all':
            result = df.apply(lambda val: (val - df.iloc[0]) / df.iloc[0], axis=1)
        return result