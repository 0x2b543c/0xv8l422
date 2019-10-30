from .TransformerABC import Transformer as tabc
import pandas as pd

class CastToInts(tabc):
    def __init__(self, input_columns:['str']='all'):
        self.input_columns = input_columns

    def implement_transformation(self, df):
        if self.input_columns == 'all':
            result = df.astype('float')
        return result